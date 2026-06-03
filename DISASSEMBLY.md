# Reproducing the disassembly

The `*.asm` disassembly files are **generated artifacts** and are not tracked in git.
Everything needed to recreate them lives in [`tools/`](tools/). All commands are run from
the repo root.

## What gets produced

| File | Origin | Source | Contents |
|------|--------|--------|----------|
| `banks/bank0.asm` | `$8000` | `banks/bank0.bin` (from the CRT) | cold-start loader + relocator |
| `seg_0800.asm` | `$0800` | `ramdump.bin` | RAM-resident loader + app dispatcher |
| `seg_0987.asm` | `$0987` | `ramdump.bin` | raster IRQ + direct keyboard-matrix scan |
| `seg_c000_menu.asm` | `$C000` | `ramdump.bin` | title/menu code + the pipe puzzle (resource 32) |
| `seg_app07.asm` | `$C000` | `ram_app07.bin` | the game |
| `seg_c800.asm` | `$C800` | `ram_app07.bin` | game tile-fetch / collision helpers |

The C64 program is a relocating loader: bank 0 is a small stub that copies the resident
code into RAM and decompresses each app into the `$C000` region at runtime. So most of the
interesting code is only visible in a **live RAM dump**, not in the static ROM banks —
hence the two-stage process below.

## Prerequisites

- `da65` (the [cc65](https://cc65.github.io/) disassembler) on `PATH`.
- `dubcrt.crt` in the repo root (not tracked — supply your own copy).
- For the RAM-derived segments: Docker with an `asid-vice:latest` image and the
  [`vice-driver`](https://github.com/anarkiwi/vice-driver) Python package importable
  (the harness `tools/drv.py` expects it next door, at `../vice-driver`).

## Steps

```sh
# 1. Extract the ROM banks from the cartridge (pure Python, no emulator).
python tools/extract_banks.py          # -> banks/bank{0..3}.bin

# 2. Boot the cartridge under asid-vice and snapshot live RAM.
python tools/dump_ram.py               # -> ramdump.bin, ram_app07.bin

# 3. Disassemble the banks and carve + disassemble the RAM segments.
tools/disasm.sh                        # -> banks/bank0.asm, seg_*.asm
```

Step 1 alone is enough for `banks/bank0.asm`. Steps 2–3 produce the RAM-resident
segments, which is where the dispatcher, keyboard scanner, menu/puzzle and game live.

`tools/disasm.sh` simply slices fixed byte ranges out of the two dumps (see the `carve`
table inside it) and runs `da65 --start-addr <origin>` on each. Adjust the ranges there if
you want to disassemble other regions.
