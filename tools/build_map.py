import json, sys
from xml.sax.saxutils import escape
match, manifest, out_json, out_xml = sys.argv[1:5]
r = json.load(open(match, encoding='utf-8'))
canales = {c['id']: c for c in json.load(open(manifest, encoding='utf-8'))['canales']}
# Pares exactos equivocados (otro canal con nombre parecido).
quitar = {'Argentina 12', 'Canal E', 'Dsports 🇨🇱', 'Dsports 🇨🇴'}
# De los parecidos, sólo los que son el mismo canal.
aceptar = {'Garage TV', 'E-Entertaiment', '3 TV Pública Pampeana', '7 Jujuy',
           '8 Telefe Córdoba', 'France 24 Español'}
# Agregados a mano (nombre en la extensión → fuente).
manual = {
    'elnueve': ('mi.tv', 'ar#canal-9', 'Canal 9'),
    'Warner TV': ('mi.tv', 'ar#warner-channel', 'Warner Channel'),
    'KZO Entertaiment': ('directv.com.ar', '4997#KZO', 'KZO'),
}
rows = []
for x in r['exacto']:
    if x['nombre'] in quitar: continue
    rows.append((x['id'], x['nombre'], x['fuente'], 'exacto'))
for x in r['sugerido']:
    if x['nombre'] in aceptar:
        rows.append((x['id'], x['nombre'], x['fuente'], 'parecido'))
for x in r['sin'] + [s for s in r['sugerido'] if s['nombre'] not in aceptar]:
    if x['nombre'] in manual:
        site, sid, name = manual[x['nombre']]
        rows.append((x['id'], x['nombre'], {'site': site, 'site_id': sid, 'lang': 'es', 'name': name}, 'manual'))
tabla = [{'moai_id': i, 'nombre': n, 'site': f['site'], 'site_id': f['site_id'],
          'nombre_fuente': f['name'], 'como': como} for i, n, f, como in rows]
tabla.sort(key=lambda t: t['nombre'].lower())
json.dump(tabla, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(out_xml, 'w', encoding='utf-8') as fx:
    fx.write('<?xml version="1.0" encoding="UTF-8"?>\n<channels>\n')
    for t in tabla:
        fx.write(f'  <channel site="{t["site"]}" site_id="{escape(t["site_id"])}" lang="es" '
                 f'xmltv_id="{escape(t["moai_id"])}">{escape(t["nombre"])}</channel>\n')
    fx.write('</channels>\n')
import collections
print(len(tabla), 'canales con guía', dict(collections.Counter(t['site'] for t in tabla)),
      dict(collections.Counter(t['como'] for t in tabla)))
ids = [t['moai_id'] for t in tabla]
print('ids repetidos:', [i for i, n in collections.Counter(ids).items() if n > 1])

# --- Segunda pasada: DirecTV no contesta (2026-11-22); lo que tiene par en mi.tv
# pasa a mi.tv y el resto de DirecTV se saca.
a_mitv = {
    'el_trece': ('ar#el-trece', 'Canal 13'), 'baby_tv': ('ar#babytv', 'BabyTV'),
    'canal_de_las_estrellas': ('ar#canal-de-las-estrellas', 'Las Estrellas'),
    'cnn_international': ('ar#cnn', 'CNN'), 'discovery_id': ('ar#investigation-discovery', 'Investigation Discovery'),
    'disney': ('ar#disney', 'Disney Channel'), 'e_entertaiment': ('ar#entertainment', 'E!'),
    'hbo_plus': ('ar#hbo-plus-pan-regional', 'HBO Plus Panregional'), 'nickelodeon': ('ar#nickelodeon', 'Nick'),
}
nueva = []
for t in tabla:
    if t['moai_id'] in a_mitv:
        sid, nom = a_mitv[t['moai_id']]
        t.update(site='mi.tv', site_id=sid, nombre_fuente=nom, como='manual')
    if t['site'] == 'mi.tv':
        nueva.append(t)
tabla = nueva
json.dump(tabla, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(out_xml, 'w', encoding='utf-8') as fx:
    fx.write('<?xml version="1.0" encoding="UTF-8"?>\n<channels>\n')
    for t in tabla:
        fx.write(f'  <channel site="{t["site"]}" site_id="{escape(t["site_id"])}" lang="es" '
                 f'xmltv_id="{escape(t["moai_id"])}">{escape(t["nombre"])}</channel>\n')
    fx.write('</channels>\n')
print('después de la segunda pasada:', len(tabla), 'canales, todos de mi.tv')
