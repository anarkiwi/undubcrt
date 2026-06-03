import drv, time, hashlib
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED

def fp(s):
    return hashlib.md5(s.screen+s.color).hexdigest()[:8]

def hold(bm, name, frames=25):
    bm.keymatrix_tap([lookup(name)], mode=TAP_MODE_FIXED, frames=frames)

c = drv.make_container(); c.start()
print("started", c.container_id[:12])
try:
    bm = drv.connect(); bm.exit(); time.sleep(4)
    def st():
        m=bm.mem_get(0x0bf2,0x0bf3); fff=bm.mem_get(0x0fff,0x0fff)[0]; ae=bm.mem_get(0x0cae,0x0cae)[0]
        s=drv.screen(bm)
        return f"app=${m[0]:02x} $0FFF={fff} $0CAE={ae} fp={fp(s)}"
    print("boot:", st())
    for k in ["1","2","3","4","5","6","7","8","9","SPACE"]:
        hold(bm, k, 25)
        time.sleep(1.2)
        print(f"press {k:5s} ->", st())
    bm.close()
finally:
    c.stop()
