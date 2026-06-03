import drv, time

def fingerprint(s):
    # compact signature of screen: screen_addr, d018, and hash of screen+color
    import hashlib
    h = hashlib.md5(s.screen + s.color + bytes([s.d018, s.border_color, s.screen_addr & 0xff, s.screen_addr>>8])).hexdigest()[:8]
    return h

c = drv.make_container()
c.start()
print("started", c.container_id[:12])
try:
    bm = drv.connect()
    bm.exit()
    time.sleep(4)
    base = drv.screen(bm)
    print("base fp", fingerprint(base), "screen_addr",hex(base.screen_addr),"d018",hex(base.d018))
    keys = ["1","2","3","4","5","6","7","8","9","0",
            "F1","F3","F5","F7","SPACE","RETURN","RUNSTOP",
            "Q","W","E","R","T","Y","M","S","D","C","P","A","Z","X"]
    for k in keys:
        drv.tap(bm, k, frames=10)
        time.sleep(1.0)
        s = drv.screen(bm)
        fp = fingerprint(s)
        print(f"key {k:8s} -> fp {fp} screen_addr={hex(s.screen_addr)} d018={hex(s.d018)} border={s.border_color}")
    bm.close()
finally:
    c.stop()
