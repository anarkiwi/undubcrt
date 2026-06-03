# dubcrt — control map

`dubcrt.crt` is a 4-bank
[Magic Desk](https://sourceforge.net/p/vice-emu/code/HEAD/tree/trunk/vice/src/c64/cart/magicdesk.c)
C64 cartridge holding several music visualizers, a game, and a hidden remix tool. This
documents the controls for each app and how to reach the hidden mode. Findings were
verified under [asid-vice](https://github.com/anarkiwi/asid-vice) via
[vice-driver](https://github.com/anarkiwi/vice-driver); the screengrabs are VICE's own
rendered frames.

## Menu

![title screen](img/01_title.png)

Boot drops you on the title screen. Number keys launch apps; **SPACE** always returns:

| Key | App |
|-----|-----|
| **1**–**7** | music visualizers |
| **8** | the game (collect the `$` pickups) |
| **9** | secret **defMON** remix tool — *locked until the puzzle is solved* |
| **SPACE** | back to the title |

## Controls

**Visualizers (1–7) and the secret tool (9)** expose 9 live parameters (colours, speeds,
waveforms…); each key cycles one:

| Key | Param | Key | Param |
|-----|-------|-----|-------|
| **F1** | 0 | **CRSR ←→** | 5 |
| **F3** | 1 | **Left&nbsp;Shift** | 6 |
| **F5** | 2 | **Right&nbsp;Shift** | 7 |
| **F7** | 3 | **C=** (Commodore) | 8 |
| **CRSR ↑↓** | 4 | **SPACE** | exit |

**The game (8)** uses **joystick port 2**:

![the game](img/02_game.png)

| Input | Effect |
|-------|--------|
| Joystick **↑ ↓ ← →** | move |
| **Fire** | action |
| **SPACE** | exit to title |

The `$` symbols are the collectibles that arm the hidden mode.

## Secret remix mode

Solving the title-screen pipe puzzle unlocks the hidden **defMON** music tool on key
**9**. Full walkthrough: **[SECRET.md](SECRET.md)**.

![secret defMON tool](img/06_secret.png)

## Repo contents

| Path | Purpose |
|------|---------|
| `README.md`, `SECRET.md` | controls and the secret walkthrough |
| `img/` | VICE screengrabs |
| `drv.py`, `capture.py` | boot harness; screengrab driver (uses `vice_driver.display` for the framebuffer grab) |
| `nav.py`, `apps.py`, `dumpall.py`, `verify.py`, `secret.py` | probing / verification scripts |
| `tools/`, `DISASSEMBLY.md` | regenerate the disassembly (see the guide) |

The cartridge image (`dubcrt.crt`), binary dumps (`*.bin`) and generated disassembly
(`*.asm`) are intentionally **not** tracked — see `.gitignore` and `DISASSEMBLY.md`.
