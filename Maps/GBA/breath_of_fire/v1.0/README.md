# Breath of Fire v1.0 map pack

This directory is the staging area for the downloadable Game Boy Advance map
pack used by PixelNavigator.

## Directories

- `reference_snes/` contains the complete 69-entry public atlas used as a
  location, dimension, and story-state checklist. These files are references
  only and are never loaded by the Android app.
- `maps/` is reserved for verified renders extracted from the GBA ROM.
- `objects/` is reserved for static and animated object metadata.

The GBA pack is not considered publishable until every manifest entry points
to a verified GBA render. The live VRAM renderer remains the fallback for maps
that have not yet been converted.

## Rebuilding the reference catalog

Run:

```powershell
& '<bundled-python-path>' tools/breath_of_fire/scrape_reference_maps.py
```

The scraper is resumable and writes source attribution into
`reference_manifest.json`.
