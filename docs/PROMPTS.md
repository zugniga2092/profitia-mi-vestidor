# Prompts para crear tus fotos con IA

Probado con **ChatGPT (generación de imágenes)**. Copia cada prompt tal cual y cambia solo lo que va entre [corchetes].

## Antes de empezar: cómo no perder tu cara
Lo que más falla es que la IA **se invente otra cara**. Lo que funcionó:
1. **No le pidas que te «genere»: dale tus fotos.** Sube siempre **3 imágenes**: (1) una foto tuya de cuerpo entero, nítida y con buena luz; (2) la foto del outfit (de una tienda, de tu armario o de Pinterest); (3) la primera foto de la serie que ya te haya salido bien, como referencia de cara, tamaño y pose.
2. **Fija el encuadre en el prompt** (lienzo, márgenes, pies, pose). Así todas salen iguales; aun así, `construir.py` las iguala.
3. Si la cara cambia, **no corrijas a medias**: vuelve a empezar el chat con las 3 imágenes. Algunas IA (en nuestras pruebas, Gemini al generar desde cero) cambian la cara aunque se lo prohíbas.

---

## 1 · Tú con cada look → `look1.png`, `look2.png`…
Sube: tu foto · la foto del outfit · tu mejor look ya hecho (desde el segundo).

```
Usa la persona de la imagen 1 EXACTAMENTE como es: misma cara, mismos rasgos, mismo tono de piel, mismo pelo,
misma complexión. No cambies nada de su cara ni de su cuerpo.
Vístela con el outfit de la imagen 2: [describe el outfit: p. ej. blazer gris oversize, top blanco, vaquero ancho
y mocasines negros].
Copia de la imagen 3 el encuadre, el tamaño de la persona y la pose (si no hay imagen 3: de pie, de frente,
relajada, brazos a los lados).
Encuadre: lienzo vertical 1024×1536, cuerpo ENTERO de la cabeza a los pies, pies visibles, 5 % de margen arriba
y abajo, persona centrada.
Fondo TRANSPARENTE (PNG). Luz suave de estudio, foto realista, nada de ilustración.
```

## 2 · La prenda colgada en una percha → `outfit1.png`… (opcional)
Si no la haces, la página usa un recorte del look.

```
Foto realista de producto: [la prenda principal del look, p. ej. un blazer gris oversize] colgado en una percha
de madera clara, de frente, centrado, visto entero.
La percha arriba y la prenda cayendo de forma natural, como en un armario.
Lienzo cuadrado 1024×1024, 6 % de margen. Fondo TRANSPARENTE (PNG). Sin personas, sin maniquí, sin texto.
```

## 3 · El fondo → `fondo.png` (opcional)

```
Vestidor de ensueño, amplio y luminoso, en tonos [rosa empolvado y marfil]. Percheros con ropa a los lados,
un espejo grande al fondo, suelo de madera clara, luz cálida y suave. Sin personas.
Formato horizontal 1800×1200, fotografía realista con poca profundidad de campo (fondo algo desenfocado).
```

---

## Consejos
- **Mismo orden en todo:** `look3.png`, `outfit3.png` y el tercer look de `vestidor.config.json` son el mismo look.
- **Fondo transparente:** si tu IA no lo da, `pip install rembg` y `construir.py` lo quita solo.
- **La protagonista manda:** que en la foto se vea de cuerpo entero y grande; la página pone los paneles a los lados.
- **Privacidad:** son fotos de una persona real. Por defecto no se suben al repo (`.gitignore`).
