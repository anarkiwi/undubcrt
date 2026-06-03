import drv, time, hashlib
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED

def hold(bm, name, frames=25):
    bm.keymatrix_tap([lookup(name)], mode=TAP_MODE_FIXED, frames=frames)

c = drv.make_container(); c.start()
print("started", c.container_id[:12])
try:
    bm = drv.connect(); bm.exit(); time.sleep(4)
    def info():
        app=bm.mem_get(0x0bf2,0x0bf2)[0]
        bf3=bm.mem_get(0x0bf3,0x0bf3)[0]
        ae=bm.mem_get(0x0cae,0x0cae)[0]
        return app,bf3,ae
    for k in ["1","2","3","4","5","6","7","8","9"]:
        hold(bm,k,25); time.sleep(1.5)
        app,bf3,ae=info()
        s=drv.screen(bm)
        print(f"\n===== KEY {k} => app=${app:02x} $0BF3(type)=${bf3:02x} secret=${ae:02x} d018={hex(s.d018)} border={s.border_color} =====")
        print(s.text())
        hold(bm,"SPACE",25); time.sleep(1.5)  # back to menu
    bm.close()
finally:
    c.stop()
