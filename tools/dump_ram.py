#!/usr/bin/env python3
"""Boot dubcrt.crt under asid-vice and dump live RAM for disassembly.

Produces (in the repo root):
  ramdump.bin    - full 64 KB RAM at the title screen (menu/app 9 resident)
  ram_app07.bin  - full 64 KB RAM while the game (app 7) is running

These are the inputs the disassembly carve in tools/disasm.sh slices from.
Run from the repo root:  python tools/dump_ram.py
Requires Docker + an `asid-vice:latest` image (see vice-driver).
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root; dumps are written here
sys.path.insert(0, HERE)  # so `import drv` (the sibling harness) resolves

import drv  # noqa: E402
from vice_driver.keys import lookup  # noqa: E402
from vice_driver.binmon import TAP_MODE_FIXED  # noqa: E402


def full_dump(bm, path):
    mem = bytearray(0x10000)
    for base in range(0, 0x10000, 0x1000):
        mem[base : base + 0x1000] = bm.mem_get(base, base + 0xFFF)
    open(os.path.join(ROOT, path), "wb").write(mem)
    print(f"wrote {path} (app={bm.mem_get(0x0BF2, 0x0BF2)[0]:#04x})")


def main():
    c = drv.make_container()
    c.start()
    try:
        bm = drv.connect()
        bm.exit()
        time.sleep(4)
        full_dump(bm, "ramdump.bin")  # title screen / menu
        # key "8" launches the game (app 7); hold a fixed number of frames
        bm.keymatrix_tap([lookup("8")], mode=TAP_MODE_FIXED, frames=30)
        time.sleep(3)
        full_dump(bm, "ram_app07.bin")  # the game
        bm.close()
    finally:
        c.stop()


if __name__ == "__main__":
    main()
