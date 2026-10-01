===============================================================================
 BREATH OF FIRE III - 32,767 DAMAGE LIMIT
===============================================================================

Version:  1.0
Date:     September 22, 2026
Author:   97Tur
Platform: Sony PlayStation
Game:     Breath of Fire III
Region:   USA
Revision: v1.1
Disc ID:  SLUS-00422
Category: Improvement


-------------------------------------------------------------------------------
 DESCRIPTION
-------------------------------------------------------------------------------

This patch raises the maximum battle damage from 9,999 to 32,767.

Damage is still calculated normally. Attacks below the original limit are
unchanged. Attacks that calculate more than 9,999 can now deal and display
their actual damage, up to 32,767.

The patch does not force maximum damage. The temporary test modification used
during development is not included.


-------------------------------------------------------------------------------
 CONTENTS
-------------------------------------------------------------------------------

Breath of Fire III - 32767 Damage Limit v1.0.ppf
    PPF 3.0 patch for the original Track 1 BIN.

README.txt
    Instructions, compatibility information, and checksums.

FILE_ID.DIZ
    Short release identification text embedded in the PPF file.

source\patch_bof3_max_damage.py
    Source code for the guarded patch builder. This is provided for technical
    reference and is not required when applying the PPF patch.


-------------------------------------------------------------------------------
 REQUIRED DISC IMAGE
-------------------------------------------------------------------------------

Apply the patch to Track 1 of the USA v1.1 BIN/CUE release. The Track 1 image
must use raw 2,352-byte sectors. Do not apply the patch directly to a CHD, ISO,
PBP, or Track 2 audio file.

Original Track 1 size:    442,938,048 bytes
Original Track 1 CRC32:   4D5B0D4B
Original Track 1 MD5:     9DD9A7C934B8B59D0CE76B0F25D18176
Original Track 1 SHA-1:   5745D9DDE965ED0EC673BA071DEB762355FA3E1A
Original Track 1 SHA-256: 94835D58C8B19C39B551039010EE9669861F1421958002B2F6927BB2D50F2F55

The PPF contains an enabled validation block. A checksum utility should still
be used to confirm the source image before patching.


-------------------------------------------------------------------------------
 PATCHING INSTRUCTIONS
-------------------------------------------------------------------------------

1. Make a backup of the original BIN/CUE files.
2. Open PPF-O-Matic 3.0 or another PPF 3.0-compatible patcher.
3. Select the original Track 1 BIN as the disc image.
4. Select "Breath of Fire III - 32767 Damage Limit v1.0.ppf".
5. Apply the patch.
6. Keep the original Track 2 audio BIN and CUE sheet with the patched Track 1.

PPF-O-Matic patches the selected image in place. Work on a copy if the original
disc image should remain unchanged.

If the Track 1 filename is changed after patching, update the first FILE line
in the CUE sheet to match it exactly.


-------------------------------------------------------------------------------
 PATCHED IMAGE CHECKSUMS
-------------------------------------------------------------------------------

Patched Track 1 size:    442,938,048 bytes
Patched Track 1 CRC32:   2EED8DB9
Patched Track 1 MD5:     2B2D519C4FE4742D4BC22C5E629AF379
Patched Track 1 SHA-1:   AA2915807D170615D578E978BE3492DC7D797569
Patched Track 1 SHA-256: 90AA5CC17D39A9B5CF191B1B54024410EE3D03B2105337153B5E15733F71EAF7


-------------------------------------------------------------------------------
 CHD USERS
-------------------------------------------------------------------------------

Extract the CHD to BIN/CUE before applying the patch. Apply the PPF to the
resulting Track 1 BIN, then rebuild the CHD from the updated CUE sheet.

Example commands:

chdman extractcd -i "Breath of Fire III (v1.1).chd" -o "Breath of Fire III (v1.1).cue"

chdman createcd -i "Breath of Fire III (v1.1) (32767 Damage).cue" -o "Breath of Fire III (v1.1) (32767 Damage).chd"

chdman verify -i "Breath of Fire III (v1.1) (32767 Damage).chd"


-------------------------------------------------------------------------------
 TECHNICAL INFORMATION
-------------------------------------------------------------------------------

The battle code is stored in BATTLE.EMI and in the identical BATTLE2.EMI copy.
Both copies are patched.

The original routine converts the final damage to a signed 16-bit value and
clamps it to 9,999. The replacement compares the full positive result first,
clamps it to 32,767, and then performs the original signed-halfword conversion.

The modified Mode 2 Form 1 sectors have valid regenerated EDC and ECC data.
32,767 is the largest safe value for this small patch because battle damage is
passed through signed 16-bit fields. Values of 32,768 and above would otherwise
be interpreted as negative.


-------------------------------------------------------------------------------
 TESTING
-------------------------------------------------------------------------------

Tested with the USA v1.1 release in SwanStation.

Verified behavior:

- Normal damage below 9,999 is unchanged.
- Calculated damage above 9,999 is no longer reduced to 9,999.
- Five-digit damage is displayed correctly.
- The maximum result is 32,767.
- Enemy HP is reduced by the displayed damage.

The generated PPF was independently applied with ApplyPPF 3.0. The resulting
Track 1 matched the verified patched-image SHA-256 listed above.


-------------------------------------------------------------------------------
 SAVE DATA
-------------------------------------------------------------------------------

The patch does not change save data. Some emulators name memory-card files or
save states after the disc filename. If the patched image is renamed, an
existing emulator save may also need to be copied or renamed.


-------------------------------------------------------------------------------
 DISTRIBUTION
-------------------------------------------------------------------------------

This archive contains patch data and source code only. It does not contain the
game, executable, battle overlays, artwork, audio, or any other copyrighted
disc content. A legally obtained copy of the supported game is required.
