# -*- coding: utf-8 -*-
"""Genera la página de caso de cada proyecto del portafolio.

**Por qué existe.** El dashboard de cada caso es un HTML autocontenido de más de
diez megas. Eso está muy bien para abrirlo con doble clic, pero cuando se pega
el enlace en LinkedIn el rastreador no llega a descargarlo —se rinde antes— y
la publicación queda sin vista previa. Y aunque llegara, el archivo no trae
etiquetas Open Graph, que son las que LinkedIn lee para armar la tarjeta.

La solución es separar las dos cosas:

    <caso>/index.html      esta página: unos pocos KB, con las etiquetas
                           Open Graph y los botones. Es la que se comparte.
    <caso>/dashboard.html  el dashboard pesado, que se abre desde aquí.

De paso mejora la experiencia: hoy, quien abre el enlace se queda mirando una
pantalla en blanco mientras bajan diez megas sin saber qué está esperando.

La URL pública de cada caso —`/portafolio/<caso>/`— **no cambia**, así que los
enlaces que ya estén publicados en LinkedIn siguen funcionando.

Uso::

    python _generar_paginas_caso.py
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SITIO = "https://dasoteloro.github.io/portafolio"

CASOS = [
    {
        "slug": "vertice",
        "titulo": "Estudio CX — Óptica Vértice",
        "kicker": "Demo · Experiencia de cliente",
        "og_titulo": "Cadena de valor y dashboard CX — Óptica Vértice (demo)",
        "og_desc": (
            "Estudio de experiencia de cliente de una cadena de ópticas: 820 encuestas, "
            "dos mediciones y cinco regionales. Empresa y datos 100% ficticios. "
            "Dashboard web interactivo e informe ejecutivo de 103 láminas."
        ),
        "cover": "assets/vertice_cover.png",
        "lead": (
            "Estudio de experiencia de cliente para una cadena de ópticas: "
            "<b>820 encuestas</b>, dos mediciones y cinco regionales. La empresa y los "
            "datos son ficticios; el estudio es real de principio a fin."
        ),
        "destacado": {
            "titulo": "La cadena de valor",
            "texto": (
                "Una matriz de <b>importancia contra calificación</b> que ordena por cuál "
                "atributo conviene empezar. La importancia no la infiere un modelo: el "
                "cliente menciona sus tres factores decisivos, los ordena y los califica, y "
                "la gráfica cruza ese peso con la nota que le da a la marca. Los cuatro "
                "cuadrantes dicen dónde invertir y dónde ya está resuelto."
            ),
        },
        "bullets": [
            "<b>Pipeline en Python</b> que procesa la encuesta y calcula NPS, medias 0–100, "
            "voz del cliente y la matriz de importancia/calificación, con el cruce por "
            "segmento de negocio y por regional.",
            "<b>Dashboard web autocontenido</b>: un solo archivo, sin licencias ni servidor, "
            "con filtros, segmentación dinámica y comparativo 2025 vs. 2026. Las tablas se "
            "copian directo a Excel o PowerPoint.",
            "<b>Informe ejecutivo de 103 láminas</b> con gráficas nativas editables: "
            "hallazgos por módulo, conclusiones y focos de acción, con cada afirmación "
            "anclada a la lámina que la respalda.",
            "<b>Control de calidad automatizado</b>: 25 comprobaciones que recalculan cada "
            "cifra del informe desde la microdata.",
        ],
        "tags": ["Cadena de valor", "NPS", "Python", "Dashboard HTML", "YoY", "IA"],
    },
    {
        "slug": "fiduciatrust",
        "titulo": "Estudio CX Relacional — FiduciaTrust",
        "kicker": "Demo · Experiencia de cliente",
        "og_titulo": "Dashboard interactivo y análisis CX — FiduciaTrust (demo)",
        "og_desc": (
            "Estudio de experiencia de cliente de una fiduciaria: NPS, CSAT y voz del "
            "cliente, con comparativo interanual. Empresa y datos 100% ficticios. "
            "Dashboard web interactivo e informe ejecutivo de 73 láminas."
        ),
        "cover": "assets/fiduciatrust_cover.png",
        "lead": (
            "Estudio de experiencia de cliente para una fiduciaria colombiana: "
            "<b>790 encuestas</b> en dos mediciones y cuatro líneas de negocio. La empresa y "
            "los datos son ficticios; el estudio es real de principio a fin."
        ),
        "destacado": {
            "titulo": "De la data cruda a la decisión",
            "texto": (
                "El caso muestra la cadena completa: se genera y procesa la encuesta, se "
                "calculan los indicadores, se construye la herramienta con la que el equipo "
                "explora los resultados y se escribe el informe que ordena la acción. Todo "
                "con un pipeline propio, no con una plantilla."
            ),
        },
        "bullets": [
            "<b>Pipeline en Python</b> que procesa las encuestas y calcula <b>NPS</b>, "
            "<b>CSAT</b> y voz del cliente, con comparativo interanual y segmentación por "
            "línea de negocio.",
            "<b>Dashboard web autocontenido</b>: un solo archivo HTML, sin licencias ni "
            "servidor, con tema claro/oscuro, filtros y eje dinámico.",
            "<b>Informe ejecutivo de 73 láminas</b> con evolución de indicadores, contrastes "
            "entre segmentos, voz del cliente y recomendaciones accionables.",
        ],
        "tags": ["NPS/CSAT", "Python", "Dashboard HTML", "YoY", "IA"],
    },
]

PLANTILLA = """<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{titulo} · Daniel Sotelo</title>
<meta name="description" content="{og_desc}" />

<!-- Open Graph: es lo que LinkedIn, WhatsApp y Slack leen para armar la tarjeta
     del enlace. Sin esto no hay vista previa, y la publicación se ve pelada. -->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Portafolio de Daniel Sotelo" />
<meta property="og:locale" content="es_CO" />
<meta property="og:url" content="{sitio}/{slug}/" />
<meta property="og:title" content="{og_titulo}" />
<meta property="og:description" content="{og_desc}" />
<meta property="og:image" content="{sitio}/{cover}" />
<meta property="og:image:width" content="1920" />
<meta property="og:image:height" content="1080" />
<meta property="og:image:alt" content="{cover_alt}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{og_titulo}" />
<meta name="twitter:description" content="{og_desc}" />
<meta name="twitter:image" content="{sitio}/{cover}" />

<link rel="canonical" href="{sitio}/{slug}/" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg:#0b1016; --surface:#121824; --panel:#141c2a;
    --line:#243144; --line-soft:#1b2534;
    --ink:#eef2f7; --muted:#9aa8bd; --faint:#6d7c92;
    --accent:#4f93de; --accent-ink:#06101d;
    --shadow:0 20px 60px rgba(0,0,0,.5);
  }}
  *{{box-sizing:border-box}}
  body{{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:'Instrument Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    line-height:1.65; -webkit-font-smoothing:antialiased;
  }}
  a{{color:inherit}}
  .grid-bg{{
    position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.5;
    background-image:linear-gradient(var(--line-soft) 1px,transparent 1px),
                     linear-gradient(90deg,var(--line-soft) 1px,transparent 1px);
    background-size:56px 56px;
    mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,#000 40%,transparent 100%);
  }}
  .wrap{{position:relative; z-index:1; max-width:920px; margin:0 auto; padding:28px 22px 64px}}
  .topbar{{display:flex; align-items:center; justify-content:space-between; gap:16px;
    padding-bottom:22px; border-bottom:1px solid var(--line-soft)}}
  .wordmark{{font-weight:600; font-size:16px; letter-spacing:-.01em; text-decoration:none}}
  .wordmark b{{color:var(--accent)}}
  .back{{font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--muted);
    text-decoration:none; letter-spacing:.04em}}
  .back:hover{{color:var(--accent)}}
  .eyebrow{{font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:.2em;
    text-transform:uppercase; color:var(--accent); margin:40px 0 10px}}
  h1{{font-family:'Fraunces',Georgia,serif; font-weight:500; font-size:clamp(30px,5vw,46px);
    line-height:1.12; margin:0 0 16px; letter-spacing:-.015em}}
  .lead{{font-size:17px; color:var(--muted); margin:0 0 26px; max-width:62ch}}
  .lead b{{color:var(--ink); font-weight:600}}
  .shot{{display:block; width:100%; height:auto; border:1px solid var(--line);
    border-radius:12px; box-shadow:var(--shadow); margin:0 0 30px}}
  .destacado{{background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--accent);
    border-radius:10px; padding:20px 22px; margin:0 0 30px}}
  .destacado h2{{font-family:'Fraunces',Georgia,serif; font-weight:500; font-size:20px;
    margin:0 0 8px}}
  .destacado p{{margin:0; color:var(--muted); font-size:15.5px}}
  .destacado b{{color:var(--ink); font-weight:600}}
  ul{{list-style:none; padding:0; margin:0 0 30px; display:grid; gap:13px}}
  li{{position:relative; padding-left:20px; color:var(--muted); font-size:15.5px; max-width:70ch}}
  li::before{{content:""; position:absolute; left:0; top:.62em; width:7px; height:7px;
    border-radius:2px; background:var(--accent)}}
  li b{{color:var(--ink); font-weight:600}}
  .tags{{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 32px}}
  .tags span{{font-family:'JetBrains Mono',monospace; font-size:11.5px; color:var(--faint);
    border:1px solid var(--line); border-radius:999px; padding:4px 11px}}
  .actions{{display:flex; flex-wrap:wrap; gap:12px; margin:0 0 34px}}
  .btn{{display:inline-flex; align-items:center; gap:8px; padding:13px 22px; border-radius:9px;
    font-weight:600; font-size:15px; text-decoration:none; border:1px solid var(--accent);
    transition:transform .15s ease, opacity .15s ease}}
  .btn:hover{{transform:translateY(-1px)}}
  .btn-solid{{background:var(--accent); color:var(--accent-ink)}}
  .btn-line{{color:var(--ink)}}
  .aviso{{display:flex; gap:11px; align-items:flex-start; background:var(--surface);
    border:1px solid var(--line); border-radius:10px; padding:15px 17px;
    font-size:14px; color:var(--muted)}}
  .aviso b{{color:var(--ink)}}
  .aviso svg{{flex:none; width:17px; height:17px; margin-top:2px; color:var(--accent)}}
  footer{{margin-top:44px; padding-top:20px; border-top:1px solid var(--line-soft);
    display:flex; flex-wrap:wrap; gap:10px; justify-content:space-between;
    font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--faint)}}
  @media (max-width:520px){{ .btn{{width:100%; justify-content:center}} }}
</style>
</head>
<body>
<div class="grid-bg"></div>
<div class="wrap">

  <div class="topbar">
    <a class="wordmark" href="../">Daniel Sotelo<b>.</b></a>
    <a class="back" href="../">← Volver al portafolio</a>
  </div>

  <p class="eyebrow">{kicker}</p>
  <h1>{titulo}</h1>
  <p class="lead">{lead}</p>

  <img class="shot" src="../{cover}" alt="{cover_alt}" loading="lazy" />

  <div class="destacado">
    <h2>{destacado_titulo}</h2>
    <p>{destacado_texto}</p>
  </div>

  <ul>
{bullets}
  </ul>

  <div class="tags">{tags}</div>

  <div class="actions">
    <a class="btn btn-solid" href="dashboard.html">Abrir el dashboard →</a>
    <a class="btn btn-line" href="informe.pdf">Informe ejecutivo (PDF)</a>
  </div>

  <div class="aviso">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
    <span>Este proyecto es una <b>demo</b>: la empresa y los datos son <b>100% ficticios</b>,
      creados solo para mostrar el alcance del trabajo. No contiene información de clientes
      reales.</span>
  </div>

  <footer>
    <span>© <span id="y"></span> Daniel Sotelo Rodríguez</span>
    <span>Estadístico · BI · Experiencia de cliente</span>
  </footer>

</div>
<script>document.getElementById("y").textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def construir(caso: dict) -> str:
    bullets = "\n".join(f"    <li>{b}</li>" for b in caso["bullets"])
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in caso["tags"])
    return PLANTILLA.format(
        sitio=SITIO,
        slug=caso["slug"],
        titulo=html.escape(caso["titulo"]),
        kicker=html.escape(caso["kicker"]),
        og_titulo=html.escape(caso["og_titulo"]),
        og_desc=html.escape(caso["og_desc"]),
        cover=caso["cover"],
        cover_alt=html.escape(f"Vista del dashboard de {caso['titulo']}"),
        lead=caso["lead"],
        destacado_titulo=html.escape(caso["destacado"]["titulo"]),
        destacado_texto=caso["destacado"]["texto"],
        bullets=bullets,
        tags=tags,
    )


def main() -> int:
    for caso in CASOS:
        carpeta = RAIZ / caso["slug"]
        if not carpeta.is_dir():
            print(f"  ! falta la carpeta {carpeta}", file=sys.stderr)
            return 1

        indice, dashboard = carpeta / "index.html", carpeta / "dashboard.html"

        # El dashboard pesado se mueve a dashboard.html, y solo la primera vez:
        # si ya está movido, index.html es la página de caso y no hay que tocarlo.
        if not dashboard.exists():
            if not indice.exists():
                print(f"  ! no encuentro el dashboard de {caso['slug']}", file=sys.stderr)
                return 1
            shutil.move(str(indice), str(dashboard))
            print(f"  · {caso['slug']}: dashboard movido a dashboard.html "
                  f"({dashboard.stat().st_size / 1048576:.1f} MB)")

        indice.write_text(construir(caso), encoding="utf-8")
        print(f"  + {caso['slug']}/index.html — página de caso "
              f"({indice.stat().st_size / 1024:.1f} KB, con Open Graph)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
