import drv, time, sys

c = drv.make_container()
c.start()
print("started", c.container_id[:12])
try:
    bm = drv.connect()
    bm.exit()
    time.sleep(4)
    for t in range(6):
        s = drv.screen(bm)
        codes = s.screen
        # show unique non-space screencodes histogram and any ASCII-ish runs
        print(f"--- t={t} d018={s.d018:#x} screen_addr={s.screen_addr:#x} charset_addr={s.charset_addr:#x} border={s.border_color} ---")
        print(s.text())
        time.sleep(1.5)
    bm.close()
finally:
    c.stop()
