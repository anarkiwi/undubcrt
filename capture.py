import drv, time, os
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED
from vgrab import grab
os.makedirs("img", exist_ok=True)
def hold(bm,n,f=30): bm.keymatrix_tap([lookup(n)],mode=TAP_MODE_FIXED,frames=f)
def shot(bm,name,settle=0.0,crop=True):
    if settle: time.sleep(settle)
    grab(bm, f"img/{name}.png", crop_border=crop)
    print(f"saved img/{name}.png  app={bm.mem_get(0xbf2,0xbf2)[0]} FFE={bm.mem_get(0xffe,0xffe)[0]} FFD={bm.mem_get(0xffd,0xffd)[0]}")

c=drv.make_container(); c.start(); print("started",c.container_id[:12])
try:
    bm=drv.connect(); bm.exit(); time.sleep(4)
    shot(bm,"01_title")                                  # boot title (dormant puzzle)
    # arm + shuffle so the puzzle is live
    hold(bm,"8",30); shot(bm,"02_game",2.0)              # the game
    bm.mem_set(0xffb, bytes([0x40]))                     # simulate having eaten $24 pickups
    hold(bm,"SPACE",30); shot(bm,"03_puzzle",2.0)        # armed + shuffled pipe grid
    hold(bm,"1",30); time.sleep(0.6)
    hold(bm,"SPACE",30); shot(bm,"03b_puzzle_rot",2.0)   # after rotating cell 0 (key 1)
    # solved -> remix
    bm.mem_set(0xff0, bytes([0x07,0x0b,0x04,0x09,0x03,0x08,0x06,0x0a,0x05]))
    bm.mem_set(0xffe, bytes([0x02]))
    shot(bm,"04_remix",2.0)                              # credits / remix reveal
    hold(bm,"9",30); shot(bm,"06_secret",2.5)            # secret defMON tool
    bm.close()
finally:
    c.stop()
