# Breath of Fire III - 32,767 Damage Limit

This patch raises the maximum damage in the North American PlayStation release
of Breath of Fire III from 9,999 to 32,767.

Damage is still calculated normally. Weak attacks are unchanged, while attacks
that would have stopped at 9,999 can now deal and display their actual damage up
to 32,767. Healing and other battle behavior are left unchanged.

## Supported game

- Breath of Fire III, USA v1.1
- Disc ID: SLUS-00422
- Input format: raw Track 1 BIN with 2,352-byte sectors
- Track 1 SHA-256:
  `94835d58c8b19c39b551039010ee9669861f1421958002b2f6927bb2d50f2f55`

The patcher rejects an incorrect disc image instead of attempting a blind
patch. It always creates a new file and never modifies the original in place.

## Requirements

- Python 3.10 or newer
- A legally obtained copy of the supported disc
- `chdman` only if a CHD output is wanted

## Applying the patch

Extract or obtain the original raw Track 1 BIN, then run:

```text
python patch_bof3_max_damage.py "Breath of Fire III (v1.1) (Track 1).bin" "Breath of Fire III (v1.1) (32767 Damage) (Track 1).bin"
```

Keep the original Track 2 audio BIN. Update a copy of the CUE sheet so its first
`FILE` line names the patched Track 1 file. The patched BIN/CUE can be played
directly or converted back to CHD:

```text
chdman createcd -i "Breath of Fire III (v1.1) (32767 Damage).cue" -o "Breath of Fire III (v1.1) (32767 Damage).chd"
chdman verify -i "Breath of Fire III (v1.1) (32767 Damage).chd"
```

Expected patched Track 1 SHA-256:
`90aa5cc17d39a9b5cf191b1b54024410ee3d03b2105337153b5e15733f71eaf7`

## Technical notes

The damage calculation is in `BATTLE.EMI`, which appears twice on the disc as
`BATTLE.EMI` and `BATTLE2.EMI`. Both copies are patched. The original routine
converts the final result to a signed 16-bit value and clamps it to 9,999. The
replacement compares the full positive result first, clamps it to 32,767, and
then performs the original signed-halfword conversion.

The patcher updates the affected Mode 2 Form 1 sectors and regenerates their
EDC and ECC data. The two modified raw sectors are LBAs 392 and 734.

32,767 is the safe maximum for this small patch because the battle result is
passed through signed 16-bit fields. Values from 32,768 through 65,535 would be
interpreted as negative without a much larger rewrite of the battle system.

## Optional test build

The source includes a debug option that forces the value immediately before
the final clamp. This is useful for testing the five-digit display:

```text
python patch_bof3_max_damage.py original.bin test.bin --force-damage 32767
```

Do not use a forced-damage image for normal play. The option affects actions
routed through the shared physical-damage routine. A normal release should be
created without `--force-damage`.

## Save files

The patch does not change save data. Emulators that name memory cards or save
states after the disc filename may require the existing save file to be copied
or renamed for the patched image.

