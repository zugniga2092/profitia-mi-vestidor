"""Construye tu vestidor.

Uso:  python construir.py              → dist/ (para publicar en Vercel u otro hosting estático)
      python construir.py --un-archivo → además vestidor.html, una sola página con las imágenes dentro

Imágenes (en fotos/, cualquier formato: png, jpg, webp):
  look1..N   la persona con cada look, de cuerpo entero (mejor con fondo transparente)
  outfit1..N la prenda sola colgada en una percha (opcional)
  fondo      el vestidor de fondo (opcional)
Si falta una, se usa la de ejemplo/ (dibujada por generar_ejemplo.py).
Los textos de cada look (nombre, ocasiones, temporadas, consejos, colores) están en vestidor.config.json,
en el MISMO orden que look1, look2…
"""
import base64
import hashlib
import html as html_mod
import io
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).parent
FOTOS, EJEMPLO, LISTO, DIST = AQUI / "fotos", AQUI / "ejemplo", AQUI / ".listo", AQUI / "dist"
LOOK_W, LOOK_H = 800, 1200      # lienzo de cada look (2:3): todas iguales, pies abajo
LOOK_MARGEN = 24
OUTFIT_LADO = 600
EXT = ("png", "webp", "jpg", "jpeg", "PNG", "JPG", "JPEG", "WEBP")


def buscar(carpeta, nombre):
    for ext in EXT:
        p = carpeta / f"{nombre}.{ext}"
        if p.exists():
            return p
    return None


def sin_fondo(img):
    """Si la foto no trae fondo transparente, se lo quita con rembg (opcional: pip install rembg)."""
    img = img.convert("RGBA")
    a, (w, h) = img.getchannel("A"), img.size
    if max(a.getpixel((0, 0)), a.getpixel((w - 1, 0)), a.getpixel((0, h - 1)), a.getpixel((w - 1, h - 1))) < 20:
        return img
    try:
        from rembg import remove
    except ImportError:
        print("  aviso: la foto tiene fondo y rembg no está instalado (pip install rembg). Se usa tal cual.")
        return img
    return remove(img)


def recortar(img):
    caja = img.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    return img.crop(caja) if caja else img


def encajar(img, ancho, alto):
    s = min(ancho / img.width, alto / img.height)
    return img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS)


def preparar_look(p):
    fig = encajar(recortar(sin_fondo(Image.open(p))), LOOK_W - 40, LOOK_H - 2 * LOOK_MARGEN)
    lienzo = Image.new("RGBA", (LOOK_W, LOOK_H), (0, 0, 0, 0))
    lienzo.paste(fig, ((LOOK_W - fig.width) // 2, LOOK_H - LOOK_MARGEN - fig.height), fig)
    return lienzo


def preparar_prenda(img):
    img = recortar(img)
    pad = round(OUTFIT_LADO * .06)
    img = encajar(img, OUTFIT_LADO - 2 * pad, OUTFIT_LADO - 2 * pad)
    lienzo = Image.new("RGBA", (OUTFIT_LADO, OUTFIT_LADO), (0, 0, 0, 0))
    lienzo.paste(img, ((OUTFIT_LADO - img.width) // 2, pad), img)   # colgada desde arriba
    return lienzo


def prenda_de_look(look):
    """Sin foto de la prenda: el tronco del look (sin la cara)."""
    fig = recortar(look)
    w, h = fig.size
    return preparar_prenda(fig.crop((round(w * .06), round(h * .17), round(w * .94), round(h * .60))))


def data_uri(img, calidad=84):
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=calidad, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # tildes bien en la consola de Windows
    conf = json.loads((AQUI / "vestidor.config.json").read_text(encoding="utf-8"))
    looks_conf = conf["looks"]
    n = len(looks_conf)
    if n < 2:
        sys.exit("vestidor.config.json necesita al menos 2 looks.")
    if not buscar(EJEMPLO, "look1"):
        import generar_ejemplo
        generar_ejemplo.main()
    if LISTO.exists():
        shutil.rmtree(LISTO)
    LISTO.mkdir()

    usa_ejemplo, tipos = False, set()
    for i in range(n):
        p = buscar(FOTOS, f"look{i + 1}")
        img = preparar_look(p) if p else preparar_look(buscar(EJEMPLO, f"look{i + 1}"))
        usa_ejemplo |= p is None
        img.save(LISTO / f"look{i + 1}.webp", "WEBP", quality=86)
        q = buscar(FOTOS, f"outfit{i + 1}")
        if q:
            o, tipo = preparar_prenda(sin_fondo(Image.open(q))), "percha"
        elif p:
            o, tipo = prenda_de_look(img), "recorte"
        else:
            o, tipo = preparar_prenda(Image.open(buscar(EJEMPLO, f"outfit{i + 1}")).convert("RGBA")), "prueba"
        tipos.add(tipo)
        o.save(LISTO / f"outfit{i + 1}.webp", "WEBP", quality=84)
        print(f"look {i + 1}: {('tu foto ' + p.name) if p else 'ejemplo'} · prenda: {tipo}")

    f = buscar(FOTOS, "fondo") or buscar(EJEMPLO, "fondo")
    fondo = Image.open(f).convert("RGB")
    fondo.thumbnail((1800, 1800))
    fondo.save(LISTO / "fondo.webp", "WEBP", quality=78)

    # «percha»: fotos de prendas colgadas · «recorte»: tronco del look · «prueba»: percha dibujada por la página
    outfit_tipo = "percha" if tipos == {"percha"} else "recorte" if "recorte" in tipos else "prueba"
    looks_js = [{k: l[k] for k in ("n", "occ", "temp", "por", "frio", "calor", "q", "c")} for l in looks_conf]
    marcas = {
        "{{NOMBRE}}": html_mod.escape(conf.get("nombre", "Mi Vestidor")),
        "{{SUBTITULO}}": html_mod.escape(conf.get("subtitulo", "Asesora de estilo")),
        "{{PRUEBA}}": "true" if usa_ejemplo else "false",
        "{{OUTFIT_TIPO}}": json.dumps(outfit_tipo),
        "{{LOOKS}}": json.dumps(looks_js, ensure_ascii=False),
        "{{TIENDAS}}": json.dumps(conf.get("tiendas", []), ensure_ascii=False),
        "{{BUSQUEDA_EXTRA}}": json.dumps(conf.get("busqueda_extra", ""), ensure_ascii=False),
    }
    plantilla = (AQUI / "plantilla.html").read_text(encoding="utf-8")

    def rellenar(m):
        h = plantilla
        for k, v in m.items():
            h = h.replace(k, v)
        return h

    # dist/: imágenes como archivos con huella en el nombre (caché de un año) y un HTML ligero
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "img").mkdir(parents=True)

    def publicar(origen, nombre):
        h = hashlib.sha1(origen.read_bytes()).hexdigest()[:8]
        destino = DIST / "img" / f"{nombre}-{h}.webp"
        shutil.copy(origen, destino)
        return f"img/{destino.name}"

    fondo_url = publicar(LISTO / "fondo.webp", "fondo")
    look_urls = [publicar(LISTO / f"look{i + 1}.webp", f"look{i + 1}") for i in range(n)]
    outfit_urls = [publicar(LISTO / f"outfit{i + 1}.webp", f"outfit{i + 1}") for i in range(n)]
    cuerpo = rellenar(dict(marcas, **{"{{FONDO}}": fondo_url, "{{LOOK_IMGS}}": json.dumps(look_urls), "{{OUTFIT_IMGS}}": json.dumps(outfit_urls)}))
    precarga = (f'<link rel="preload" as="image" href="{fondo_url}" fetchpriority="high">\n'
                f'<link rel="preload" as="image" href="{look_urls[0]}" fetchpriority="high">\n')
    pagina = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
              f'<meta name="description" content="{marcas["{{NOMBRE}}"]}: looks según la ocasión y la temporada.">\n'
              + precarga + cuerpo.replace("<style>", "<style>\n[hidden]{display:none!important}", 1)
              .replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
    (DIST / "index.html").write_text(pagina, encoding="utf-8")
    peso = sum(x.stat().st_size for x in DIST.rglob("*") if x.is_file())
    print(f"dist/: listo para publicar · {peso / 1024:.0f} KB · {'imágenes de EJEMPLO' if usa_ejemplo else 'tus fotos'}")

    if "--un-archivo" in sys.argv:
        uno = rellenar(dict(marcas, **{
            "{{FONDO}}": data_uri(fondo, 78),
            "{{LOOK_IMGS}}": json.dumps([data_uri(Image.open(LISTO / f"look{i + 1}.webp"), 86) for i in range(n)]),
            "{{OUTFIT_IMGS}}": json.dumps([data_uri(Image.open(LISTO / f"outfit{i + 1}.webp")) for i in range(n)]),
        }))
        (AQUI / "vestidor.html").write_text(uno, encoding="utf-8")
        print(f"vestidor.html: {len(uno) / 1024:.0f} KB (una sola página)")


if __name__ == "__main__":
    main()
