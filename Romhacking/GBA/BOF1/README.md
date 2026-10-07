# Breath of Fire GBA DrWarp

Experimental patch for the unmodified USA GBA cartridge, ABFE revision 0.
Requires Pixel Navigator 0.4.4 with the matching DrWarp controls running alongside the game.

Create a separate ROM copy through Pixel Navigator's Breath of Fire Settings,
or apply `bof1_drwarp_044.ips` to a copy of your own cartridge dump.
The Python alternative is:

```
python patch_bof1_drwarp.py original.gba drwarp.gba
```

Select the patched copy in Pixel Navigator and enable DrWarp in Settings.
A free inventory slot is required. Use DrWarp from the game's item menu to
request the Pixel Navigator destination picker. The game menu closes before
the picker opens. Select a map, optionally enter custom coordinates, and tap
Warp. Cancel leaves the game in its current location.

Map 390 at X 520, Y 9244 is the ruined shrine exterior verified against the
[Flying Omelette reference](https://flyingomelette.com/oddities/oddities26.html).
The article's SNES warp number 71 does not identify the same place on GBA.
Other destinations and unused interiors remain experimental.

The [map catalog](MAPS.md) lists all 496 GBA map IDs using the game's own
location-name table. The destination picker can search those labels.
Map 103 at X 632, Y 28796 matches the large purple face in the reference;
map 102 shows a muted palette version. Both are cutscene resources. Their
presence does not establish that the artwork was unused in the main game.
All eight cutscene-bank entries were inspected on the device.

Pixel Navigator saves a state before a requested warp. Return restores that
state, including the inventory and progress from before exploration.
Keep a separate normal save. This patch does not repair unfinished areas.

Original ROM SHA256:
`3289aec193497c86c3c769b42c1024a1d491d48f15b90fcb58910dca0a79647a`

No cartridge image is included. The item-to-picker handler has been checked
with CPU emulation; its live device interaction still needs verification.
