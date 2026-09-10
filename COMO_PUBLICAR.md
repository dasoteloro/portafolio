# Cómo publicar el portafolio en GitHub Pages

El sitio en vivo (https://dasoteloro.github.io/portafolio/) se sirve del repositorio
**`dasoteloro/portafolio`**, rama `main`. Lo que hay en esa rama es exactamente lo que
se ve publicado: no hay proceso de compilación de por medio.

Esta carpeta (`web_portafolio/`) es la **copia de trabajo**: se prepara aquí y se sube tal cual.

## Lo que va al repositorio

```
index.html                     la landing
README.md                      la portada del repositorio
assets/<caso>_cover.png        la miniatura de cada caso
<caso>/index.html              la PÁGINA DE CASO (ligera, ~9 KB)
<caso>/dashboard.html          el dashboard autocontenido (10 MB)
<caso>/informe.pdf             el informe en PDF
_generar_paginas_caso.py       genera las páginas de caso
```

### Por qué el dashboard no es el `index.html`

Al principio lo era, y por eso LinkedIn no conseguía generar la vista previa del
enlace: el rastreador se rinde antes de descargar diez megas, y el archivo tampoco
trae las etiquetas **Open Graph** (`og:title`, `og:description`, `og:image`) que son
las que arman la tarjeta del enlace.

Ahora `/<caso>/` es una página ligera con esas etiquetas y con los dos botones, y el
dashboard vive en `/<caso>/dashboard.html`. La URL pública del caso **no cambió**, así
que los enlaces ya publicados siguen funcionando — y ahora sí generan vista previa.

De paso se abre más rápido: antes el visitante veía una pantalla en blanco mientras
bajaban diez megas sin saber qué estaba esperando.

Las páginas de caso **no se editan a mano**: se generan con

```bash
python _generar_paginas_caso.py
```

que además mueve el dashboard a `dashboard.html` la primera vez. El texto de cada
caso está en la lista `CASOS` de ese archivo.

Y una convención que la landing asume: el informe se llama **`informe.pdf`**, no con
su nombre largo. Si subes el nombre largo, el botón «Informe (PDF)» queda roto.

## Publicar (la forma corta)

Con Git ya configurado en este equipo —lo está: usuario `dasoteloro` y Git Credential
Manager—, desde una terminal:

```bash
# 1. Traer el repositorio a una carpeta temporal
cd %TEMP%
git clone https://github.com/dasoteloro/portafolio.git
cd portafolio

# 2. Copiar encima lo que cambió (ajusta las rutas al caso que toque)
W="/c/Users/danie/Streaming de Google Drive/Mi unidad/Documentos/Portafolio/web_portafolio"
cp "$W/index.html" .
cp "$W/README.md" .
cp -r "$W/assets" .
cp -r "$W/vertice" .
cp "$W/fiduciatrust/index.html" fiduciatrust/

# 3. Ver qué va a subir ANTES de subirlo
git add -A
git status --short

# 4. Subir
git commit -m "Actualizar el portafolio"
git push origin main
```

## Después de subir

GitHub Pages tarda **entre uno y tres minutos** en reconstruir. Hasta entonces el sitio
sigue mostrando la versión anterior, y una URL nueva devuelve 404 aunque el archivo ya
esté en el repositorio. No es un error: hay que esperar y recargar.

Para comprobar que quedó publicado, sin abrir el navegador:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -L https://dasoteloro.github.io/portafolio/vertice/
```

`200` es publicado; `404` es que todavía no ha reconstruido.

Y en el navegador conviene recargar con **Ctrl+F5**: el dashboard pesa 10 MB y el
navegador lo tiene cacheado, así que una recarga normal puede seguir mostrando el viejo.

## Si algo sale mal

El repositorio guarda todo el historial, así que nada se pierde: en
https://github.com/dasoteloro/portafolio/commits/main está cada versión y se puede
volver a cualquiera. Un `git revert <hash>` seguido de `git push` deshace una subida.

## Estado actual

Publicado el 2026-09-10 con los dos casos:

| Caso | Página de caso (la que se comparte) | Dashboard | Informe |
|---|---|---|---|
| FiduciaTrust | `/portafolio/fiduciatrust/` | `…/dashboard.html` | `…/informe.pdf` |
| Óptica Vértice | `/portafolio/vertice/` | `…/dashboard.html` | `…/informe.pdf` |

**Para compartir en LinkedIn usa la página de caso**, no el `dashboard.html`: es la
que lleva las etiquetas Open Graph y la que genera la vista previa con imagen.

### Si LinkedIn no actualiza la vista previa

LinkedIn cachea lo que leyó de una URL. Si ya intentaste añadir el enlace antes de
este arreglo, puede seguir mostrando el resultado viejo: pásalo por el
[Post Inspector](https://www.linkedin.com/post-inspector/) de LinkedIn, que vuelve a
leer la página y refresca su caché.
