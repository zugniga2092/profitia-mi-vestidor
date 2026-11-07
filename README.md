# Mi Vestidor · tu asesora de estilo con IA · por Profitia

Una página donde **tú (o quien quieras) eres la protagonista**: de cuerpo entero dentro de un vestidor, con tus looks girando en un arco de tarjetas de vidrio. Eliges la **ocasión** (día a día, trabajo, cita, viaje, evento) y la **temporada**, y la asesora te **recomienda el mejor look y te explica por qué**. Al elegir uno, una línea de luz baja y te «viste» con él. Las prendas cuelgan en perchas y se mecen al moverlas.

Sin servidores, sin base de datos y sin claves: es una página estática que se publica gratis en Vercel.

> Hecho por [Profitia](https://profitia.digital) — IA para negocios. Si te sirve, deja una ⭐ en el repo.

---

## Qué incluye

| | |
|---|---|
| 🪞 **La protagonista** | Tu foto de cuerpo entero en el centro. Todas las fotos se igualan solas (mismo tamaño, pies abajo). |
| 👗 **Arco de looks** | Tarjetas de vidrio que giran con el ratón, el dedo, la rueda o las flechas. Cada prenda cuelga de su percha y se balancea como un péndulo. |
| ✨ **Probar el look** | Una línea de luz baja y cambia el look; nunca se ven dos a la vez. |
| 🧠 **La asesora** | Puntúa cada look según la ocasión (2 puntos) y la temporada (1 punto), elige el mejor, lo marca como «Recomendada» y explica por qué: «Ideal», «Funciona» o «Hay algo mejor», con consejo para frío o calor. |
| 🎨 **Paleta y tiendas** | Los colores de cada look y, en modo Tiendas, enlaces a buscar algo parecido en las tiendas que elijas. Sin precios inventados. |
| 📱 **Móvil y ordenador** | Diseñado para las dos. Respeta «reducir movimiento». |

Viene con **imágenes de ejemplo dibujadas por código** (un maniquí sin cara), para que funcione nada más clonarlo. Cuando pongas tus fotos, se usan las tuyas.

---

## Paso a paso

### 1 · Haz tu copia
Pulsa **Use this template → Create a new repository** (arriba a la derecha en GitHub).

### 2 · Crea tus fotos con IA
Necesitas, para cada look: **tú con el look puesto, de cuerpo entero** (`look1.png`, `look2.png`…) y, si quieres, **la prenda sola colgada en una percha** (`outfit1.png`…). Y un **fondo** de vestidor (`fondo.png`).

Los prompts completos, listos para copiar, están en **[docs/PROMPTS.md](docs/PROMPTS.md)**. El truco para que la IA **no te cambie la cara** también está ahí.

### 3 · Ponlas en `fotos/`
Súbelas a la carpeta `fotos/` con esos nombres (png, jpg o webp). Mejor con **fondo transparente**; si no, el script se lo quita (necesita `rembg`, ver abajo).

### 4 · Escribe tus looks
Abre **`vestidor.config.json`** y, en el mismo orden que tus fotos, cambia cada look:

```jsonc
{
  "n": "Blazer gris oversize",             // nombre
  "occ": ["trabajo", "diario"],            // diario · trabajo · cita · viaje · evento
  "temp": ["otono", "primavera"],          // otono · invierno · primavera · verano
  "por": "Por qué funciona (1 frase).",
  "frio": "Consejo si hace frío.",
  "calor": "Consejo si hace calor.",
  "q": "blazer gris oversize",             // lo que se busca en las tiendas
  "c": [["Gris marengo", "#4a4a4e"], ["Blanco", "#f3f1ec"]]   // paleta
}
```
Arriba del archivo cambias el nombre de la página, las tiendas y la palabra que se añade a la búsqueda (`"mujer"`, `"hombre"` o vacío). El bloque `"ejemplo"` solo sirve para dibujar el maniquí de ejemplo: cuando tengas tus fotos, puedes borrarlo.

### 5 · Publica
Entra en **[vercel.com/new](https://vercel.com/new)**, elige tu repositorio y pulsa **Deploy**. Vercel construye la página solo (está en `vercel.json`). Cada cambio que subas a GitHub la actualiza.

---

## En tu ordenador (opcional)

Necesitas **[Python 3.10+](https://www.python.org/downloads/)**.

```bash
pip install -r requirements.txt     # Pillow
pip install rembg                   # opcional: quita el fondo a fotos que no sean transparentes
python construir.py                 # → dist/ (la web)
python -m http.server 8000 --directory dist    # ábrela en http://localhost:8000
python construir.py --un-archivo    # además, vestidor.html: una sola página con todo dentro
```

| Archivo | Qué es |
|---|---|
| `vestidor.config.json` | Tus looks, textos, tiendas y nombre. **Lo único que tienes que tocar.** |
| `fotos/` | Tus fotos (`look1..N`, `outfit1..N`, `fondo`). No se suben al repo si no quieres (ver `.gitignore`). |
| `plantilla.html` | Diseño, animaciones y lógica de la asesora. |
| `construir.py` | Iguala las fotos y genera `dist/`. |
| `generar_ejemplo.py` | Dibuja el maniquí, las prendas y el fondo de ejemplo. |

### ¿Fotos privadas?
Por defecto `fotos/` **no se sube** a GitHub (está en `.gitignore`), para que tu cara no quede en un repositorio público. Si quieres publicar la web con tus fotos, tienes dos caminos: hacer el repo **privado** y quitar `fotos/` del `.gitignore`, o construir en tu ordenador y subir solo `dist/` con `npx vercel deploy dist --prod`.

---

## Cómo se hizo
Esta plantilla salió de un proyecto real montado con **Claude Code**: un vestidor personal con looks hechos con IA. Lo que aprendimos (cómo mantener la cara, cómo igualar las fotos, cómo hacer que las prendas cuelguen) está en [docs/PROMPTS.md](docs/PROMPTS.md).

## Licencia
[MIT](LICENSE). Úsala, cámbiala y véndela si quieres; mantén el aviso de copyright.
