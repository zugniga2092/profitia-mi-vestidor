"""Dibuja las imágenes de EJEMPLO (sin fotos de nadie): un maniquí sin cara con cada look, la prenda principal
de cada look y un vestidor de fondo. Así el proyecto funciona nada más clonarlo.

Uso:  python generar_ejemplo.py      → ejemplo/look1..N.png, ejemplo/outfit1..N.png, ejemplo/fondo.png

Los colores y la forma salen de vestidor.config.json → looks[i].ejemplo:
  "capa": "chaqueta" | "corta" | "abrigo" | "ninguna"     "abajo": "pantalon" | "falda"
  "colores": {"capa", "arriba", "abajo", "zapatos"}
Cuando pongas tus fotos en fotos/, estas imágenes dejan de usarse.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

AQUI = Path(__file__).parent
SALIDA = AQUI / "ejemplo"
K = 3                                   # se dibuja 3 veces más grande y se reduce: bordes suaves
MANIQUI = "#e8dccd"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tono(h, f):
    """f < 1 oscurece, f > 1 aclara."""
    r, g, b = rgb(h)
    if f < 1:
        return tuple(round(c * f) for c in (r, g, b))
    return tuple(round(c + (255 - c) * (f - 1)) for c in (r, g, b))


def poli(d, puntos, color, borde=True):
    pts = [(x * K, y * K) for x, y in puntos]
    d.polygon(pts, fill=rgb(color) if isinstance(color, str) else color)
    if borde:
        d.line(pts + [pts[0]], fill=tono(color, .82) if isinstance(color, str) else color, width=2 * K, joint="curve")


def elipse(d, cx, cy, rx, ry, color):
    d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=rgb(color))


def espejo(puntos, eje=400):
    return [(2 * eje - x, y) for x, y in puntos]


def look(e):
    """Maniquí 800×1200 con el look (pies abajo, fondo transparente)."""
    col, capa, abajo = e["colores"], e.get("capa", "ninguna"), e.get("abajo", "pantalon")
    im = Image.new("RGBA", (800 * K, 1200 * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # piernas / falda
    if abajo == "falda":
        for lado in (lambda p: p, espejo):
            poli(d, lado([(338, 790), (392, 790), (386, 1112), (352, 1112)]), MANIQUI, False)
            poli(d, lado([(334, 905), (392, 905), (388, 1118), (346, 1118)]), col["zapatos"])          # botas
        poli(d, [(312, 585), (488, 585), (512, 800), (288, 800)], col["abajo"])
    else:
        poli(d, [(306, 590), (398, 590), (390, 1112), (326, 1112)], col["abajo"])
        poli(d, espejo([(306, 590), (398, 590), (390, 1112), (326, 1112)]), col["abajo"])
    # zapatos
    for lado in (lambda p: p, espejo):
        poli(d, lado([(318, 1108), (392, 1108), (394, 1146), (310, 1146)]), col["zapatos"])
    # torso (lo de arriba)
    poli(d, [(298, 212), (502, 212), (472, 520), (480, 605), (320, 605), (328, 520)], col["arriba"])
    # cuello y cabeza (maniquí sin cara)
    poli(d, [(384, 150), (416, 150), (420, 214), (380, 214)], MANIQUI, False)
    elipse(d, 400, 108, 46, 58, MANIQUI)
    # mangas y manos
    manga = col["capa"] if capa != "ninguna" and col.get("capa") else col["arriba"]
    for lado in (lambda p: p, espejo):
        poli(d, lado([(298, 212), (336, 246), (306, 565), (264, 558)]), manga)
    elipse(d, 284, 586, 19, 24, MANIQUI)
    elipse(d, 516, 586, 19, 24, MANIQUI)
    # la capa (chaqueta, abrigo o chaqueta corta), abierta para que se vea lo de debajo
    if capa != "ninguna" and col.get("capa"):
        bajo = {"chaqueta": 640, "corta": 470, "abrigo": 905}.get(capa, 640)
        for lado in (lambda p: p, espejo):
            poli(d, lado([(292, 206), (384, 214), (372, bajo), (298, bajo + 4)]), col["capa"])
            poli(d, lado([(384, 214), (360, 330), (372, 214)]), tono(col["capa"], .9))                # solapa
    im = im.resize((800, 1200), Image.LANCZOS)
    return im


def prenda(e):
    """La prenda principal sola, 600×600, colgada desde arriba (la percha la dibuja la página)."""
    col, capa = e["colores"], e.get("capa", "ninguna")
    color = col["capa"] if capa != "ninguna" and col.get("capa") else col["arriba"]
    largo = {"chaqueta": 430, "corta": 330, "abrigo": 560, "ninguna": 380}.get(capa, 430)
    im = Image.new("RGBA", (600 * K, 600 * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for lado in (lambda p: p, lambda p: espejo(p, 300)):
        poli(d, lado([(182, 40), (236, 30), (226, 300), (150, 290)]), tono(color, .94))                 # manga
    poli(d, [(196, 30), (404, 30), (412, largo), (188, largo)], color)                                  # cuerpo
    if capa != "ninguna":
        poli(d, [(296, 30), (304, 30), (304, largo), (296, largo)], tono(color, .8), False)             # abertura
        for lado in (lambda p: p, lambda p: espejo(p, 300)):
            poli(d, lado([(250, 30), (296, 30), (296, 150)]), tono(color, .9))                         # solapa
    im = im.resize((600, 600), Image.LANCZOS)
    return im.filter(ImageFilter.GaussianBlur(.3))


def fondo(looks):
    """Vestidor suave rosa y marfil, 1800×1200 (la página lo desenfoca un poco)."""
    W, H = 1800, 1200
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    a, b = rgb("#f4e3df"), rgb("#efe4d8")
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    d.rectangle([0, 930, W, H], fill=rgb("#d9c4b0"))
    d.rectangle([0, 930, W, 940], fill=rgb("#cbb39d"))
    d.ellipse([700, 120, 1100, 820], fill=rgb("#f8efe9"), outline=rgb("#e2cfc4"), width=10)           # espejo
    colores = [l["ejemplo"]["colores"].get("capa") or l["ejemplo"]["colores"]["arriba"] for l in looks] or ["#d6c3a5"]
    for x0, x1 in ((90, 620), (1180, 1710)):                                                            # percheros
        d.line([(x0, 300), (x1, 300)], fill=rgb("#c9b29a"), width=8)
        n = 7
        for i in range(n):
            cx = x0 + 40 + i * (x1 - x0 - 80) / (n - 1)
            c = colores[(i + (x0 > 600) * 3) % len(colores)]
            d.line([(cx, 300), (cx, 330)], fill=rgb("#b9a58f"), width=4)
            d.rounded_rectangle([cx - 30, 330, cx + 30, 560 + (i % 3) * 40], radius=14, fill=tono(c, 1.15))
    d.rectangle([90, 760, 620, 772], fill=rgb("#e6d6c8"))
    d.rectangle([1180, 760, 1710, 772], fill=rgb("#e6d6c8"))
    return im.filter(ImageFilter.GaussianBlur(2))


def main():
    conf = json.loads((AQUI / "vestidor.config.json").read_text(encoding="utf-8"))
    SALIDA.mkdir(exist_ok=True)
    for i, l in enumerate(conf["looks"]):
        e = l.get("ejemplo") or {"capa": "ninguna", "abajo": "pantalon",
                                 "colores": {"capa": "", "arriba": l["c"][0][1], "abajo": "#3a3f4a", "zapatos": "#1d1d20"}}
        look(e).save(SALIDA / f"look{i + 1}.png")
        prenda(e).save(SALIDA / f"outfit{i + 1}.png")
    fondo(conf["looks"]).save(SALIDA / "fondo.png")
    print(f"ejemplo/: {len(conf['looks'])} looks + prendas + fondo")


if __name__ == "__main__":
    main()
