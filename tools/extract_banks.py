#!/usr/bin/env python3
"""Parse dubcrt.crt (Magic Desk CRT) and write each 8 KB bank to banks/bankN.bin.

Run from the repo root:  python tools/extract_banks.py
"""
import os
import struct

CRT = "dubcrt.crt"
OUT = "banks"


def main():
    data = open(CRT, "rb").read()
    assert data[:16].startswith(b"C64 CARTRIDGE"), "not a C64 CRT"
    hdr_len = struct.unpack(">I", data[0x10:0x14])[0]
    os.makedirs(OUT, exist_ok=True)
    off = hdr_len
    n = 0
    while off < len(data):
        assert data[off : off + 4] == b"CHIP", f"bad CHIP packet at {off:#x}"
        plen = struct.unpack(">I", data[off + 4 : off + 8])[0]
        bank = struct.unpack(">H", data[off + 10 : off + 12])[0]
        load = struct.unpack(">H", data[off + 12 : off + 14])[0]
        size = struct.unpack(">H", data[off + 14 : off + 16])[0]
        chip = data[off + 16 : off + 16 + size]
        path = os.path.join(OUT, f"bank{bank}.bin")
        open(path, "wb").write(chip)
        print(f"bank {bank}: load={load:#06x} size={size:#06x} -> {path}")
        off += plen
        n += 1
    print(f"wrote {n} banks to {OUT}/")


if __name__ == "__main__":
    main()
