"""Screengrab the secret remix unlock, solving the title-screen pipe puzzle
for real -- every tile rotation is a genuine keypress driven through the CIA
keyboard matrix (the cartridge scans $DC00/$DC01 directly; the KERNAL is never
involved), and the gate ($0FFE: 0 -> 1 -> 2) is advanced by the cartridge's own
code, not poked. The only shortcut is arming: instead of grabbing $24 pickups in
the game we set the arm counter ($0FFB) and rotation range ($0FFD) directly."""
import drv, time, os
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED
from vice_driver.display import parse_display_response, parse_palette_response
os.makedirs("img", exist_ok=True)

def tap(bm, n, f=12):
    bm.keymatrix_tap([lookup(n)], mode=TAP_MODE_FIXED, frames=f); time.sleep(0.2)
def grid(bm):  return list(bm.mem_get(0xff0, 0xff8))
def ffe(bm):   return bm.mem_get(0xffe, 0xffe)[0]
def app(bm):   return bm.mem_get(0xbf2, 0xbf2)[0]
def shot(bm, name, settle=0.0, crop=True):
    if settle: time.sleep(settle)
    snap = parse_display_response(bm.display_get())
    pal = parse_palette_response(bm.palette_get())
    snap.save_png(f"img/{name}.png", pal, crop_inner=crop)
    print(f"saved img/{name}.png  app={app(bm)} FFE={ffe(bm)} grid={bm.mem_get(0xff0,0xff8).hex()}")

# Which number key rotates which grid cell (centre cell 4 is set automatically).
KEY = {0: "1", 1: "2", 2: "3", 3: "4", 5: "5", 6: "6", 7: "7", 8: "8"}
# A visibly-busy, unsolved arrangement to photograph as the puzzle-to-solve.
SCR = {0: 0x07, 1: 0x0a, 2: 0x03, 3: 0x09, 5: 0x0b, 6: 0x05, 7: 0x08, 8: 0x06}
# The two solved patterns, cell order 0..8 (centre omitted -- the cartridge fills it).
S1 = {0: 0x07, 1: 0x02, 2: 0x04, 3: 0x01, 5: 0x01, 6: 0x06, 7: 0x02, 8: 0x05}
S2 = {0: 0x07, 1: 0x0b, 2: 0x04, 3: 0x09, 5: 0x08, 6: 0x06, 7: 0x0a, 8: 0x05}

def to_menu(bm):
    for _ in range(8):
        if app(bm) == 9: return
        tap(bm, "SPACE")
def rotate_once(bm, cell):
    """Tap the cell's key (enter app -> rotate) and SPACE back, until it moves."""
    before = grid(bm)[cell]
    for _ in range(8):
        to_menu(bm); tap(bm, KEY[cell]); to_menu(bm)
        if grid(bm)[cell] != before: return
def solve(bm, target):
    for cell, want in target.items():
        for _ in range(14):
            if grid(bm)[cell] == want: break
            rotate_once(bm, cell)
    to_menu(bm)

c = drv.make_container(); c.start(); print("started", c.container_id[:12])
try:
    bm = drv.connect(); bm.exit(); time.sleep(4)
    shot(bm, "01_title")                       # boot title (puzzle dormant)

    tap(bm, "8", 30); shot(bm, "02_game", 2.0)  # key 8 -> the game ($ pickups arm it)
    to_menu(bm)

    bm.mem_set(0xffb, bytes([0x40]))            # armed (= having eaten the $24 pickups)
    bm.mem_set(0xffd, bytes([0x0c]))            # rotation range unlocked (= fully shuffled)
    solve(bm, SCR); shot(bm, "03_scrambled", 1.5)  # live puzzle, shuffled but not solved

    solve(bm, S1); shot(bm, "04_stage1", 1.5)   # first network -> $0FFE 0->1, centre lights
    solve(bm, S2); shot(bm, "05_reveal", 2.5)   # second network -> $0FFE 1->2 -> remix bursts in

    tap(bm, "9", 30); shot(bm, "06_secret", 2.5)  # key 9 now live -> secret defMON tool
    bm.close()
finally:
    c.stop()
