# Auditoría SEO – corporacionyanayacu.com

Fecha: 2026-11-20 · Sitio estático (clon de WordPress/Elementor) · Idioma: es · Mercado: Perú
Leyenda: ✅ ok · ⚠️ mejorar · ❌ falla · 👤 requiere iniciar sesión (manual) · P1 bloquea / P2 alto impacto / P3 mejora

## Resumen

El sitio es rastreable (robots.txt abierto, HTTPS activo, `lang="es"`), pero está casi sin SEO on-page: ninguna página tiene meta description, canonical, Open Graph ni datos estructurados, y 6 de 8 páginas no tienen H1. No hay sitemap, no hay analítica y los títulos llevan un error ortográfico ("Corporaración"). Además, el servidor expone copias del código fuente (`/src/`, `/dist/`, `build.mjs`), lo que crea contenido duplicado indexable, y las versiones `http://` y `www` responden 200 sin redirigir. El bloqueo principal es la duplicación (P1); el resto es trabajo de bajo costo y alto impacto.

## Tabla por fase

| Fase | Elemento | Estado | Evidencia | Acción | Prior. |
|---|---|---|---|---|---|
| F1 | Analítica GA4 | ⚠️ | El código está listo pero apagado | 👤 Crear la propiedad GA4 y poner el ID en `ga4_id` de `src/site.json` | P2 |
| F1 | Eventos clave | ❌ | No existen | Medir clic en WhatsApp, envío de formularios, clic en Intranet | P2 |
| F2 | Search Console | 👤 | No verificable desde aquí | Verificar propiedad de dominio (DNS) y enviar sitemap | P1 |
| F2 | Google Business Profile | 👤 | No verificable | Ficha como oficina/servicio en Av. Arenales 480, Lima; NAP idéntico al sitio | P2 |
| F3 | robots.txt | ✅ | `Allow: /` + línea `Sitemap:` | — | — |
| F3 | Sitemap | ✅ | El build genera `dist/sitemap.xml` con 8 URLs y `lastmod` | 👤 Enviarlo en Search Console | P1 |
| F3 | Duplicados por código fuente | ⚠️ | `.htaccess` devuelve 404 para `/src`, `/dist`, `/tools`, `build.mjs`, `package.json`, `*.md`, `*.py` | Aplicar con el próximo deploy; lo ideal es clonar el repo fuera de `public_html` | P1 |
| F3 | Versiones de dominio | ⚠️ | `.htaccess` redirige con un solo 301 a `https://corporacionyanayacu.com` (excepto `/.well-known/`) | Verificar tras el deploy | P1 |
| F3 | noindex heredado | ✅ | Sin `meta robots` ni `X-Robots-Tag` | — | — |
| F4 | `<title>` | ✅ | Únicos, entre 45 y 63 caracteres, sin errores, palabra clave + marca | — | — |
| F4 | Meta description | ✅ | Única en las 8 páginas (124–147 caracteres) | — | — |
| F4 | Canonical | ✅ | Presente en las 8 páginas; `url` rellenado | — | — |
| F4 | H1 | ✅ | Exactamente un H1 por página (el título del banner pasó de H2 a H1 sin cambiar el estilo) | — | — |
| F4 | Open Graph / Twitter | ✅ | `og:*` y `twitter:card`; imagen 1200×630 de 112 KB | — | — |
| F4 | `alt` en imágenes | ✅ | Todas las imágenes tienen `alt` en español | — | — |
| F4 | Enlaces del footer | ✅ | Apuntan a las páginas reales; también las tarjetas y botones de Servicios del inicio | Quedan `#` en Ssoma/Sumak (marcas) y en los íconos del equipo | P3 |
| F5 | Palabras clave | ⚠️ | Títulos y descripciones ya incluyen Lima y los servicios; falta ampliar los textos | Tabla página → palabra clave (abajo) | P2 |
| F6 | Datos estructurados | ✅ | `Organization` + `LocalBusiness` en el inicio (JSON-LD válido) | 👤 Validar en la Prueba de resultados enriquecidos | P2 |
| F6 | Peso de imágenes | ✅ | 20 imágenes pesadas pasaron a WebP (≈3,3 MB menos); `lazy` y dimensiones añadidas | Medir con PageSpeed Insights | P2 |
| F6 | Solicitudes por página | ⚠️ | ~30 CSS y ~24 JS por página (Elementor) | Combinar/diferir; medir con PageSpeed Insights | P3 |
| F6 | Video | ✅ | `preload="none"`, 13 MB solo al pulsar | Considerar comprimir a ~4 MB | P3 |
| F6 | Página 404 | ✅ | `404.html` con la marca, `noindex` y `ErrorDocument 404` | — | — |
| F6 | HTTPS | ✅ | Certificado activo | — | — |
| F6 | Viewport / `lang` | ✅ | Presentes | — | — |
| F7 | Búsqueda con IA | ✅ | Aplican F3–F6; no hace falta `llms.txt` | — | — |

## Palabras clave sugeridas (a validar en Search Console)

| Página | Palabra clave principal | Intención | Estado |
|---|---|---|---|
| Inicio | corporación servicios agro construcción Lima | comercial | mejorar |
| Agro | asistencia técnica agrícola / insumos agrícolas Lima | comercial | mejorar |
| Construcción | consultoría proyectos de inversión pública Perú | comercial | mejorar |
| Servicios Generales | mantenimiento de bienes e intermediación laboral Lima | comercial | mejorar |
| Marcas | unidades de negocio Corporación Yanayacu | navegacional | mejorar |
| Contacto | Corporación Yanayacu contacto Lima | navegacional | mejorar |

## Pendientes manuales 👤

1. **Search Console:** crear propiedad de dominio → verificar con registro TXT en el DNS → Sitemaps → enviar `https://corporacionyanayacu.com/sitemap.xml`.
2. **GA4:** crear propiedad y flujo web → copiar el ID `G-XXXXXXX` → vincular con Search Console (Admin → Product links).
3. **Google Business Profile:** crear una sola ficha, verificar (puede pedir video del local), categoría principal, servicios, horario Lun–Sáb 9–18 h, enlace al sitio.
4. **Bing Webmaster Tools** (opcional): importar el sitio desde Search Console.

## Qué hacer primero (orden recomendado)

1. P1 técnico: redirecciones 301, bloqueo de `/src` `/dist` `/tools`, sitemap.
2. P1 on-page: títulos corregidos, meta descriptions, canonical, un H1 por página.
3. P2: Open Graph, JSON-LD, `alt`, imágenes a WebP, GA4.
4. 👤 Search Console y ficha de Google.

## Cuándo volver a medir

A las 2–4 semanas de publicar: páginas indexadas, consultas y clics en Search Console, Core Web Vitals con datos de campo (LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1). Indexar puede tardar días o semanas y no está garantizado.

## Cambios aplicados al código

Aplicados tras la confirmación del usuario: títulos, descripciones, canonical, Open Graph, H1, JSON-LD, `alt`, enlaces del footer, WebP, sitemap, `robots.txt`, `.htaccess` (redirecciones y bloqueos), página 404 y revisión de ortografía en todo el proyecto.

No se hizo: combinar o diferir los ~30 CSS y ~24 JS de Elementor, comprimir el video del aniversario (13 MB, solo carga al pulsar), URLs de Ssoma y Sumak y GA4 (necesitan datos del cliente).


---

## Auditoría final (2 rondas de verificación)

Ronda 1: el agente de implementación aplicó los cambios y se verificó por separado con un script sobre `dist/`. Ronda 2: revisión ortográfica independiente (otro agente, solo lectura) + segunda auditoría técnica tras corregir lo que quedó suelto. Resultado: **0 páginas con fallos** en las 9 salidas (8 páginas + 404), `npm run check` sin archivos faltantes (1184 referencias) y sin enlaces internos rotos.

### Corregido en el código (100 % de lo que se puede hacer desde el repo)

| Punto | Estado |
|---|---|
| Títulos únicos, sin "Corporaración" | ✅ |
| Meta description única (100–165 car.) | ✅ |
| Canonical (coincide con sitemap) | ✅ |
| Open Graph / Twitter + `og:image` existente | ✅ |
| Un solo H1 por página | ✅ |
| JSON-LD Organization + LocalBusiness en la home (válido) | ✅ |
| `alt` en todas las imágenes, `lazy` + dimensiones | ✅ |
| `sitemap.xml` (8 URLs) y línea `Sitemap:` en robots | ✅ |
| 301 `http` y `www` → `https://corporacionyanayacu.com` | ✅ (en `.htaccess`, ver nota) |
| Bloqueo de `/src`, `/dist`, `/tools`, `build.mjs`, `*.md` | ✅ (en `.htaccess`, ver nota) |
| Página 404 de marca con `noindex` | ✅ |
| Imágenes pesadas a WebP (-3,3 MB) | ✅ |
| Enlaces del footer y botones de servicios a páginas reales | ✅ |
| Botones Ssoma y Sumak (`ssomasafe.com`, `agrosumak.com`) | ✅ (tomados de tus otros proyectos; confirmar) |
| Iconos de redes del equipo sin destino | ✅ eliminados |
| Soporte GA4 (`ga4_id` en `src/site.json`) | ✅ listo, inactivo hasta poner el ID |
| Contador "0+" muestra su valor final sin JavaScript (500) | ✅ |
| Ortografía y redacción (tildes, comas, ÁNCASH, `S/`, "Nuestro equipo", etc.) | ✅ |
| Mayúsculas en títulos (sentence case) y mayúsculas indebidas en el texto | ✅ |
| Formularios: contacto → WhatsApp; libro → aviso con `reclamaciones@` | ✅ |

> Nota: los redireccionamientos y bloqueos viven en `.htaccess` y solo actúan cuando el despliegue en cPanel copia `dist/` a `public_html`. Verifica con `curl -I http://corporacionyanayacu.com` tras desplegar.

### Pendiente: requiere tu cuenta o tu decisión 👤

1. **Deploy en cPanel** (Update from Remote → Deploy HEAD Commit). Hasta entonces el dominio sigue mostrando la versión anterior.
2. **Google Search Console:** verificar dominio (DNS) y enviar `https://corporacionyanayacu.com/sitemap.xml`.
3. **Google Analytics 4:** crear la propiedad y pegar el ID `G-XXXXXXX` en `src/site.json` (`ga4_id`); luego `npm run build`.
4. **Google Business Profile:** ficha con la dirección y el teléfono idénticos a los del sitio.
5. **Formularios:** para recibir el contacto por correo, crear un endpoint (Formspree) y pegarlo en `src/site.json` (`forms.contact`, `forms.libro`).
6. **Decisiones de marca/redacción que no tomé por ti:**
   - Grafía "Yana Yacu" (logo, titulares) frente a "Yanayacu" (dominio, metadatos): mezcladas en el texto original; se mantuvo cada una como estaba.
   - "Jose Larios": confirma si lleva tilde (José).
   - Cargos en inglés ("CEO", "Gerente de Compliance").
   - Confirmar que `ssomasafe.com` y `agrosumak.com` son los sitios correctos de Ssoma y Sumak, y que `quantukperu.com` tiene HTTPS (hoy el enlace usa `http://`).

### No hecho a propósito (riesgo mayor que el beneficio)

- Unir/diferir los ~30 CSS y ~24 JS de Elementor: puede romper el diseño. Medir primero con PageSpeed Insights.
- Comprimir el video del aniversario (13 MB): solo carga al pulsar "Ver video" (`preload="none"`).
- `dist/` pesa ~105 MB por los archivos de los plugins de Elementor; depurarlos sin romper scripts diferidos requiere pruebas visuales.

### Cuándo volver a medir

A las 2–4 semanas de publicado: páginas indexadas, consultas y clics en Search Console, y Core Web Vitals con datos de campo (LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1).
