import drv, time
from vice_driver.keys import lookup
from vice_driver.binmon import TAP_MODE_FIXED

def hold(bm,name,frames=25):
    bm.keymatrix_tap([lookup(name)],mode=TAP_MODE_FIXED,frames=frames)
def dump(bm,path):
    mem=bytearray(0x10000)
    for b in range(0,0x10000,0x1000):
        mem[b:b+0x1000]=bm.mem_get(b,b+0xfff)
    open(path,'wb').write(mem)

c=drv.make_container(); c.start()
print("started",c.container_id[:12])
try:
    bm=drv.connect(); bm.exit(); time.sleep(4)
    dump(bm,'ram_menu.bin'); print("menu dumped, app",bm.mem_get(0x0bf2,0x0bf2)[0])
    for i,k in enumerate(["1","2","3","4","5","6","7","8"]):
        hold(bm,k,25); time.sleep(1.8)
        app=bm.mem_get(0x0bf2,0x0bf2)[0]
        dump(bm,f'ram_app{app:02x}.bin')
        print(f"key {k} app=${app:02x} dumped")
        hold(bm,"SPACE",25); time.sleep(1.8)
    bm.close()
finally:
    c.stop()
