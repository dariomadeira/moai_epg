import json, re, sys, unicodedata, difflib, xml.etree.ElementTree as ET
manifest, mitv, dtv, out = sys.argv[1:5]
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\((arg|ar|argentina|latam|latinoamerica|hd|sd)\)', ' ', s)
    s = re.sub(r'\b(hd|sd|fhd|4k|canal|tv|television|arg|argentina|en vivo)\b', ' ', s)
    s = s.replace('&', 'y').replace('+', 'mas')
    return re.sub(r'[^a-z0-9]', '', s)
def load(path):
    rows = []
    for c in ET.parse(path).getroot().findall('channel'):
        rows.append({'site': c.get('site'), 'site_id': c.get('site_id'), 'lang': c.get('lang'), 'name': c.text or ''})
    return rows
src = load(mitv) + load(dtv)
idx = {}
for r in src:
    idx.setdefault(norm(r['name']), []).append(r)
keys = list(idx)
canales = json.load(open(manifest, encoding='utf-8'))['canales']
res = {'exacto': [], 'sugerido': [], 'sin': []}
for c in canales:
    k = norm(c['nombre'])
    cands = idx.get(k) or idx.get(norm(c['id']))
    if cands:
        # prefer mi.tv, then directv
        cands = sorted(cands, key=lambda r: r['site'] != 'mi.tv')
        res['exacto'].append({'id': c['id'], 'nombre': c['nombre'], 'categoria': c.get('categoria'), 'fuente': cands[0]})
        continue
    close = difflib.get_close_matches(k, keys, n=1, cutoff=0.82) if k else []
    if close:
        r = sorted(idx[close[0]], key=lambda r: r['site'] != 'mi.tv')[0]
        res['sugerido'].append({'id': c['id'], 'nombre': c['nombre'], 'categoria': c.get('categoria'), 'fuente': r})
    else:
        res['sin'].append({'id': c['id'], 'nombre': c['nombre'], 'categoria': c.get('categoria')})
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
print('exacto', len(res['exacto']), '| sugerido', len(res['sugerido']), '| sin', len(res['sin']))
for k in ('exacto', 'sin'):
    print(k, 'por categoría:', collections.Counter(x['categoria'] for x in res[k]).most_common())
