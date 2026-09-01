# Current Progres:
- GBA EXPOSED!
<img width="988" height="1039" alt="image" src="https://github.com/user-attachments/assets/9fe51261-a4bd-47d5-bacf-80a419ed3a1f" />
<img width="932" height="943" alt="image" src="https://github.com/user-attachments/assets/e407a723-0658-41df-8afa-9f933c187f9b" />
<img width="1009" height="1010" alt="image" src="https://github.com/user-attachments/assets/c59e1e96-ba1a-4937-ba1b-b23f5e42955f" />
<img width="808" height="851" alt="image" src="https://github.com/user-attachments/assets/9ab01091-01bd-4b70-9e26-ba325966c16e" />





# Pixel Navigator

[![Release v0](https://img.shields.io/badge/release-v0-8957e5?style=for-the-badge&logo=github)](https://github.com/ChimeraGaming/PixelNavigator/releases)
![Android](https://img.shields.io/badge/Android-compatible-3DDC84?style=for-the-badge&logo=android&logoColor=white)
[![Star this repository](https://img.shields.io/github/stars/ChimeraGaming/PixelNavigator?style=for-the-badge&logo=github&label=STAR%20THIS%20REPOSITORY&color=f5c542)](https://github.com/ChimeraGaming/PixelNavigator)

**Pixel Navigator** is a concept for an Android map companion for emulated games.

The project is based on ideas developed for [Fanmake Pokémon Maps](https://github.com/ChimeraGaming/FanmakePokemonMaps_Android), with the goal of expanding the same general map and player tracking concept beyond RPG Maker XP games and into ROMs and other emulated games.

> [!IMPORTANT]
> Pixel Navigator is currently a concept. Development has not started and emulator support, tracking methods, and game compatibility have not been determined.

## Concept

Pixel Navigator would organize maps around the emulator being used, followed by the game and its available map folders.

```text
Pixel Navigator
  Emulator
    Game
      Map Folder
        Maps
```

For example:

```text
Pixel Navigator
  GBA Emulator
    Game
      World Map
      Towns
      Dungeons

  PSP Emulator
    Game
      Areas
      Dungeons

  Switch Emulator
    Game
      Regions
      Interiors
```

Each game would be able to use its own map folder structure instead of requiring every game to organize maps the same way.

## Main Goal

The main goal is to display game maps while tracking the player's current location when technically possible.

Potential functionality includes:

- Multiple emulator support
- Multiple games per emulator
- Map folders for organizing different areas
- High-resolution maps
- Player position tracking
- Automatic map switching
- Support for different game and map coordinate systems
- Expandable emulator and game support

## Potential Systems

Pixel Navigator could potentially support emulators for systems such as:

- Game Boy
- Game Boy Color
- Game Boy Advance
- Nintendo DS
- PlayStation
- PlayStation 2
- PSP
- GameCube
- Wii
- Nintendo Switch

Support would depend on what information can be obtained from each emulator and game.

## Player Tracking

Player tracking is one of the main concepts being explored.

Different emulators and systems may require completely different tracking methods. Pixel Navigator would need a way to determine information such as:

```text
Game
Map or Area
Player X Position
Player Y Position
Floor or Room
```

How this information would be obtained has not yet been determined and may vary between emulators and individual games.

## Fanmake Pokémon Maps

Pixel Navigator is inspired by my existing project, [Fanmake Pokémon Maps](https://github.com/ChimeraGaming/FanmakePokemonMaps_Android).

Fanmake Pokémon Maps provides maps for Pokémon fangames and can track player movement in supported RPG Maker XP games.

Pixel Navigator explores whether a similar concept could be expanded to emulated games across multiple systems.

## Project Status

**Concept Stage**

There are currently no supported emulators or games.

The purpose of this repository is to document the idea, research possible tracking methods, and determine whether the project is practical before development begins.

## Disclaimer

Pixel Navigator is an independent project.

It is not affiliated with or endorsed by Nintendo, Sony, Pokémon, emulator developers, game developers, publishers, or other rights holders.

Game names, trademarks, and other intellectual property belong to their respective owners.
