import json
import requests
from pytrends.request import TrendReq
from datetime import datetime

# Configuración específica para el HOME (Negocios y Estrategia)
monitor_config = {
    "Poco Tráfico": {"terms": ["posicionamiento marca google", "seo para empresas"], "sub": "marketing"},
    "Baja Conversión": {"terms": ["inteligencia artificial negocios", "marketing automation"], "sub": "contentmarketing"},
    "Competencia": {"terms": ["branding strategy", "ventaja competitiva"], "sub": "branding"},
    "Técnico": {"terms": ["digital transformation", "operaciones eficientes"], "sub": "business"}
}

pytrends = TrendReq(hl='es-ES', tz=360)
brain_update = {"last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "insights": {}}

def get_reddit_voice(subreddit):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=5"
        headers = {'User-agent': 'NomosHomeBot 1.0'}
        res = requests.get(url, headers=headers, timeout=10).json()
        return res['data']['children'][0]['data']['title']
    except:
        return "El mercado está demandando nuevas estructuras de marca hoy."

print("🚀 NOMOS-Home: Capturando pulso estratégico...")

for category, config in monitor_config.items():
    try:
        pytrends.build_payload(config["terms"], timeframe='now 1-d')
        data = pytrends.interest_over_time()
        avg_score = int(data.iloc[-1].drop('isPartial', errors='ignore').mean()) if not data.empty else 25
    except:
        avg_score = 15
    
    brain_update["insights"][category] = {
        "status": "ALTA" if avg_score > 50 else "ESTABLE",
        "score": avg_score,
        "reddit_voice": get_reddit_voice(config["sub"])
    }

with open('nomos_home_intelligence.json', 'w', encoding='utf-8') as f:
    json.dump(brain_update, f, indent=4, ensure_ascii=False)

print("✅ Cerebro NOMOS-Home actualizado.")
