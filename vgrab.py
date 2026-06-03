"""Grab VICE's own rendered framebuffer via DISPLAY_GET + PALETTE_GET."""
import struct
from PIL import Image
from vice_driver.binmon import OPCODE

def palette(bm):
    resp = bm.call(OPCODE.PALETTE_GET, bytes([0x00]))
    b = resp.body
    n = struct.unpack("<H", b[0:2])[0]
    pal, off = [], 2
    for _ in range(n):
        sz = b[off]; off += 1
        r, g, bl = b[off], b[off+1], b[off+2]
        pal.append((r, g, bl)); off += sz
    return pal

def display(bm, use_vic=1):
    resp = bm.call(OPCODE.DISPLAY_GET, bytes([use_vic, 0x00]))
    b = resp.body
    info_len = struct.unpack("<I", b[0:4])[0]
    dw, dh, xo, yo, iw, ih = struct.unpack("<HHHHHH", b[4:16])
    bpp = b[16]
    blen = struct.unpack("<I", b[17:21])[0]
    data = b[4 + info_len: 4 + info_len + blen]
    return dict(dw=dw, dh=dh, xo=xo, yo=yo, iw=iw, ih=ih, bpp=bpp, blen=blen, data=data)

def grab(bm, path, crop_border=False):
    pal = palette(bm)
    d = display(bm)
    img = Image.new("RGB", (d["dw"], d["dh"]))
    px = img.load()
    data = d["data"]
    for y in range(d["dh"]):
        row = y * d["dw"]
        for x in range(d["dw"]):
            idx = data[row + x]
            px[x, y] = pal[idx] if idx < len(pal) else (0, 0, 0)
    if crop_border:
        img = img.crop((d["xo"], d["yo"], d["xo"] + d["iw"], d["yo"] + d["ih"]))
    img.save(path)
    return d
