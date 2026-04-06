import requests
import json
import os

API_KEY = os.environ.get('REDASH_API_KEY')
BASE = 'https://redash.rappi.com'

QUERIES = {
    'dr_counter':     130989,
    'dr_picker':      130990,
    'dr_pie':         130991,
    'dr_hora':        130992,
    'dr_detalle':     130995,
    'so_counter':     130925,
    'so_tienda':      130922,
    'so_tipo':        130923,
    'so_productos':   130924,
    'so_pickers':     130934,
}

def fetch(query_id, warehouse='Todos'):
    res = requests.post(
        f'{BASE}/api/queries/{query_id}/results',
        headers={
            'Authorization': f'Key {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={'parameters': {'warehouse': warehouse}}
    )
    data = res.json()
    return data.get('query_result', {}).get('data', {}).get('rows', [])

print('Fetching data from Redash...')
result = {}
for name, qid in QUERIES.items():
    print(f'  {name}...')
    result[name] = fetch(qid)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, default=str)

print('data.json updated!')
