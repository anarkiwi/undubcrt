#!/usr/bin/env bash
# Regenerate every *.asm disassembly file from the cartridge + RAM dumps.
#
# Prereqs (run from the repo root):
#   - da65 on PATH (cc65 suite)
#   - dubcrt.crt present
#   - ramdump.bin and ram_app07.bin present (produce them with
#     `python tools/dump_ram.py`)
#
# Usage:  tools/disasm.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# 1) ROM banks straight from the cartridge.
python3 tools/extract_banks.py
da65 --start-addr 0x8000 banks/bank0.bin -o banks/bank0.asm
echo "wrote banks/bank0.asm"

# 2) RAM-resident code carved from live dumps. Args: src skip count origin out
carve() {
  local src=$1 skip=$2 count=$3 origin=$4 out=$5
  dd if="$src" of="/tmp/_seg.bin" bs=1 skip="$skip" count="$count" status=none
  da65 --start-addr "$origin" /tmp/_seg.bin -o "$out"
  echo "wrote $out  (from $src @ $(printf 0x%x "$skip"), origin $origin)"
}

#       source         skip    count   origin    output
carve ramdump.bin      2048    1024    0x0800    seg_0800.asm       # loader + dispatcher
carve ramdump.bin      2439     633    0x0987    seg_0987.asm       # raster IRQ + key scan
carve ramdump.bin     49152    1024    0xc000    seg_c000_menu.asm  # title/menu + puzzle (resource 32)
carve ram_app07.bin   49152    1792    0xc000    seg_app07.asm      # the game
carve ram_app07.bin   51200     576    0xc800    seg_c800.asm       # game tile-fetch helpers

rm -f /tmp/_seg.bin
echo "done."
