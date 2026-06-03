"""Interactive harness to drive dubcrt.crt under asid-vice."""
import sys, time, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (tools/..)
sys.path.insert(0, os.path.join(ROOT, "..", "vice-driver"))  # sibling checkout
from vice_driver import BinMon, DiskMount, ViceContainer
from vice_driver.keys import lookup
from vice_driver.screen import parse_screen_response

CRT = os.path.join(ROOT, "dubcrt.crt")
PORT = int(os.environ.get("DUBCRT_PORT", "6555"))  # host port, avoid 6502 (other container)

def make_container(**kw):
    return ViceContainer(
        autostart=None,
        binmon_port=PORT,
        container_binmon_port=6502,
        mounts=[DiskMount(CRT, "/work/dubcrt.crt", read_only=True)],
        extra_args=["-cartcrt", "/work/dubcrt.crt"],
        warp=True, silent=True,
        **kw,
    )

def connect():
    bm = BinMon("127.0.0.1", PORT)
    bm.connect(timeout=15.0, attempts=120, retry_delay=0.25)
    return bm

def screen(bm):
    return parse_screen_response(bm.screen_get())

def show(bm):
    s = screen(bm)
    print(s.text())
    return s

def tap(bm, *names, frames=15):
    keys = [lookup(n) for n in names]
    bm.keymatrix_tap(keys, frames=frames)

def keystr(bm, text, frames=8, delay=0.15):
    from vice_driver.keys import text_to_chords
    for chord in text_to_chords(text):
        bm.keymatrix_tap([lookup(n) for n in chord], frames=frames)
        time.sleep(delay)
