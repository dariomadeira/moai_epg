# moai_epg

Guía de programación para los canales de TV de [Moai](https://github.com/dariomadeira).

- `moai.channels.xml`: qué canales se bajan y de dónde (hoy todos de mi.tv). El `xmltv_id`
  es el id del canal en la extensión `moaiplug_ar`.
- `canales.json`: la misma tabla, con el nombre en la extensión y en la fuente, y cómo se
  armó el par (`exacto`, `parecido` o `manual`).
- `.github/workflows/guia.yml`: todos los días a las 05:00 (Argentina) corre el lector de
  [iptv-org/epg](https://github.com/iptv-org/epg) y publica en la rama **`guia`**:
  - `guia.xml.gz`: XMLTV de hoy y mañana.
  - `estado.json`: cuándo se actualizó, cuántos canales y programas.

Link fijo de la guía:
`https://raw.githubusercontent.com/dariomadeira/moai_epg/guia/guia.xml.gz`

Si un día falla (por ejemplo, mi.tv cambió su página), GitHub manda un mail y Moai sigue
andando: sólo deja de mostrar la programación.

`tools/`: scripts para volver a armar la tabla cuando cambien los canales de la extensión.
