import drv, time
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED
def hold(bm,name,frames=25): bm.keymatrix_tap([lookup(name)],mode=TAP_MODE_FIXED,frames=frames)
def g(bm,a,n=1): return bm.mem_get(a,a+n-1)
def pv(bm):
    return (f"FFB={g(bm,0xffb)[0]:02x} FFC={g(bm,0xffc)[0]:02x} FFD={g(bm,0xffd)[0]:02x} "
            f"FFE={g(bm,0xffe)[0]:02x} FFF={g(bm,0xfff)[0]:02x} grid={g(bm,0xff0,9).hex()} app={g(bm,0xbf2)[0]:02x}")

c=drv.make_container(); c.start(); print("started",c.container_id[:12])
try:
    bm=drv.connect(); bm.exit()
    print("== boot watch ==")
    for i in range(8):
        time.sleep(0.7); print(f" t={i}:", pv(bm))
    # Experiment A: force shuffle by setting FFB nonzero then re-enter menu
    print("\n== set $0FFB=$40, re-enter menu (1 then SPACE) ==")
    hold(bm,"1",25); time.sleep(1.2)
    bm.mem_set(0xffb, bytes([0x40]))
    hold(bm,"SPACE",25); time.sleep(2.0)
    print(" after:", pv(bm))
    s=drv.screen(bm)
    bm.close()
finally:
    c.stop()
