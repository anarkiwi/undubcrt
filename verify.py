import drv, time
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED
def hold(bm,name,frames=30): bm.keymatrix_tap([lookup(name)],mode=TAP_MODE_FIXED,frames=frames)
def g(bm,a,n): return bm.mem_get(a,a+n-1)

c=drv.make_container(); c.start(); print("started",c.container_id[:12])
try:
    bm=drv.connect(); bm.exit(); time.sleep(4)

    # ---- (1) parameter system on app0 (key "1") ----
    hold(bm,"1",30); time.sleep(1.5)
    print("\n== app0 parameter test ==")
    print(" params $0FA0 before:", g(bm,0xfa0,8).hex())
    for k in ["F1","F3","F5","F7","CRSRUD","CRSRLR","LSHIFT","CBM"]:
        for _ in range(8):
            hold(bm,k,8);
        time.sleep(0.3)
        print(f"  after spamming {k:7s}: $0FA0 =", g(bm,0xfa0,8).hex())
    hold(bm,"SPACE",30); time.sleep(1.5)

    # ---- (2) force $0FFE=2 in menu, observe remix ----
    print("\n== secret remix: poke $0FFE=2 in menu ==")
    print(" app now:", g(bm,0xbf2,1)[0])
    s0=drv.screen(bm)
    # poke grid to stage2 target and FFE=2
    bm.mem_set(0xff0, bytes([0x07,0x0b,0x04,0x09,0x03,0x08,0x06,0x0a,0x05]))
    bm.mem_set(0xffe, bytes([0x02]))
    time.sleep(2.0)
    s1=drv.screen(bm)
    print(" $0FFE now:", g(bm,0xffe,1)[0], " border:", s1.border_color)
    print(" screen BEFORE poke:\n"+s0.text())
    print(" screen AFTER  poke (FFE=2 remix):\n"+s1.text())
    bm.close()
finally:
    c.stop()
