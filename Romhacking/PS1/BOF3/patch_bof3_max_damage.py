#!/usr/bin/env python3
"""Create a BOF3 USA v1.1 raw data track with a 32,767 damage ceiling.

The input must be Track 1 from SLUS-00422 v1.1 in raw 2352-byte-sector
BIN form.  The source is copied; it is never edited in place.  Both identical
BATTLE.EMI copies are changed and Mode 2 Form 1 EDC/ECC is regenerated for the
two affected sectors.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import struct
from pathlib import Path


SECTOR_SIZE = 2352
USER_DATA_OFFSET = 24
USER_DATA_SIZE = 2048
SOURCE_SHA256 = "94835d58c8b19c39b551039010ee9669861f1421958002b2f6927bb2d50f2f55"
BATTLE_COPIES = ((235, "BATTLE.EMI"), (577, "BATTLE2.EMI"))
PATCH_FILE_OFFSET = 0x4EADC

# Runtime 0x801DC6DC.  The original truncates to signed 16-bit before comparing
# with 10,000.  The replacement compares the full positive result with 32,767,
# clamps it, and only then performs the existing signed-halfword conversion.
ORIGINAL_WORDS = (
    0x00111400,  # sll   v0,s1,16
    0x00021403,  # sra   v0,v0,16
    0x28422710,  # slti  v0,v0,10000
    0x14400003,  # bnez  v0,0x801dc6f8
    0x00111400,  #  sll  v0,s1,16
    0x2411270F,  # addiu s1,zero,9999
    0x00111400,  # sll   v0,s1,16
)
PATCHED_WORDS = (
    0x34027FFF,  # ori   v0,zero,32767
    0x0051102A,  # slt   v0,v0,s1
    0x10400004,  # beqz  v0,0x801dc6f8
    0x00111400,  #  sll  v0,s1,16
    0x34117FFF,  # ori   s1,zero,32767
    0x00111400,  # sll   v0,s1,16
    0x00000000,  # nop
)


def build_tables() -> tuple[list[int], list[int], list[int]]:
    ecc_f = [0] * 256
    ecc_b = [0] * 256
    edc = [0] * 256
    for i in range(256):
        value = (i << 1) ^ (0x11D if i & 0x80 else 0)
        ecc_f[i] = value & 0xFF
        ecc_b[(i ^ value) & 0xFF] = i
        value = i
        for _ in range(8):
            value = (value >> 1) ^ (0xD8018001 if value & 1 else 0)
        edc[i] = value
    return ecc_f, ecc_b, edc


ECC_F, ECC_B, EDC = build_tables()


def edc_block(data: bytes | bytearray) -> int:
    value = 0
    for byte in data:
        value = (value >> 8) ^ EDC[(value ^ byte) & 0xFF]
    return value


def ecc_block(source: bytearray, major_count: int, minor_count: int,
              major_mult: int, minor_inc: int) -> bytes:
    size = major_count * minor_count
    result = bytearray(major_count * 2)
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        ecc_a = 0
        ecc_b = 0
        for _ in range(minor_count):
            value = source[index]
            index = (index + minor_inc) % size
            ecc_a ^= value
            ecc_b ^= value
            ecc_a = ECC_F[ecc_a]
        ecc_a = ECC_B[ECC_F[ecc_a] ^ ecc_b]
        result[major] = ecc_a
        result[major + major_count] = ecc_a ^ ecc_b
    return bytes(result)


def regenerate_mode2_form1(sector: bytearray) -> None:
    if len(sector) != SECTOR_SIZE or sector[15] != 2 or sector[16:20] != sector[20:24]:
        raise ValueError("affected sector is not Mode 2 with a duplicated XA subheader")
    if sector[18] & 0x20:
        raise ValueError("affected sector is Mode 2 Form 2, not Form 1")
    struct.pack_into("<I", sector, 0x818, edc_block(sector[0x10:0x818]))
    address = sector[12:16]
    sector[12:16] = b"\0" * 4
    sector[0x81C:0x8C8] = ecc_block(sector[0x0C:0x81C], 86, 24, 2, 86)
    sector[0x8C8:0x930] = ecc_block(sector[0x0C:0x8C8], 52, 43, 86, 88)
    sector[12:16] = address


def patch_copy(track, base_lba: int, name: str) -> int:
    sector_lba = base_lba + PATCH_FILE_OFFSET // USER_DATA_SIZE
    in_sector = PATCH_FILE_OFFSET % USER_DATA_SIZE
    raw_offset = sector_lba * SECTOR_SIZE
    track.seek(raw_offset)
    original_sector = bytearray(track.read(SECTOR_SIZE))
    if len(original_sector) != SECTOR_SIZE:
        raise ValueError(f"short read in {name} at LBA {sector_lba}")

    verified = bytearray(original_sector)
    regenerate_mode2_form1(verified)
    if verified != original_sector:
        raise ValueError(f"source EDC/ECC check failed for {name} at LBA {sector_lba}")

    patch_at = USER_DATA_OFFSET + in_sector
    original = struct.pack("<7I", *ORIGINAL_WORDS)
    found = original_sector[patch_at:patch_at + len(original)]
    if found != original:
        raise ValueError(
            f"{name} does not contain the verified cap sequence at 0x{PATCH_FILE_OFFSET:X}: "
            f"{found.hex()}"
        )
    original_sector[patch_at:patch_at + len(original)] = struct.pack("<7I", *PATCHED_WORDS)
    regenerate_mode2_form1(original_sector)
    track.seek(raw_offset)
    track.write(original_sector)
    return sector_lba


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="original USA v1.1 Track 1 BIN")
    parser.add_argument("output", type=Path, help="new patched Track 1 BIN")
    parser.add_argument("--skip-full-hash", action="store_true", help="use only byte/ECC guards")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        raise SystemExit("refusing to patch the source in place")
    if not args.source.is_file():
        raise SystemExit(f"source not found: {args.source}")
    if args.output.exists():
        raise SystemExit(f"output already exists: {args.output}")
    if not args.skip_full_hash:
        actual = sha256(args.source)
        if actual != SOURCE_SHA256:
            raise SystemExit(f"wrong source SHA-256: {actual}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copyfile(args.source, args.output)
        with args.output.open("r+b") as track:
            sectors = [patch_copy(track, lba, name) for lba, name in BATTLE_COPIES]
    except Exception:
        args.output.unlink(missing_ok=True)
        raise
    print(f"Patched {args.output}")
    print(f"Updated Mode 2 Form 1 sectors: {', '.join(map(str, sectors))}")
    print(f"Output SHA-256: {sha256(args.output)}")


if __name__ == "__main__":
    main()
