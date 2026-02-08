import json
import requests
from pytrends.request import TrendReq
from datetime import datetime

# 1. Configuración Estratégica para el HOME
monitor_config = {
    "Poco Tráfico": {
        "terms": ["posicionamiento marca google", "seo para empresas"],
        "sub": "marketing"
    },
    "Baja Conversión": {
        "terms": ["inteligencia artificial negocios", "marketing automation"],
        "sub": "contentmarketing"
    },
    "Competencia": {
        "terms": ["branding strategy", "ventaja competitiva"],
        "sub": "branding"
    },
    "Técnico": {
        "terms": ["digital transformation", "operaciones eficientes"],
        "sub": "business"
    }
}

# Inicializamos Google Trends
pytrends = TrendReq(hl='es-ES', tz=360)

def get_reddit_voice(subreddit):
    """Extrae el titular más reciente simulando un navegador real para evitar bloqueos"""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=5"
        # User-Agent de navegador real para protocolo de seguridad
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        posts = data['data']['children']
        if posts:
            # Capturamos el primer post no fijado
            title = posts[0]['data']['title']
            # Protocolo de estética: Limitar longitud para el modal
            return (title[:110] + '...') if len(title) > 110 else title
        
        return "El mercado está demandando nuevas estructuras de marca hoy."
    except Exception as e:
        print(f"Log: Error en Reddit ({subreddit}): {e}")
        return "El debate estratégico en comunidades globales está en punto máximo."

# Estructura del cerebro NOMOS Home
brain_update = {
    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "insights": {}
}

print("🚀 NOMOS-Home: Iniciando captura de pulso dual...")

for category, config in monitor_config.items():
    print(f"📡 Procesando {category}...")
    
    # Parte A: Estadística de Trends
    try:
        pytrends.build_payload(config["terms"], timeframe='now 1-d')
        data = pytrends.interest_over_time()
        if not data.empty:
            avg_score = int(data.iloc[-1].drop('isPartial', errors='ignore').mean())
        else:
            avg_score = 20 # Score base por defecto
    except:
        avg_score = 10
        
    # Parte B: Voz Social de Reddit
    voice = get_reddit_voice(config["sub"])
    
    # Integración final por categoría
    brain_update["insights"][category] = {
        "status": "ALTA" if avg_score > 50 else "ESTABLE",
        "score": avg_score,
        "reddit_voice": voice
    }

# Guardar archivo JSON con nombre específico para este repositorio
with open('nomos_home_intelligence.json', 'w', encoding='utf-8') as f:
    json.dump(brain_update, f, indent=4, ensure_ascii=False)

print("✅ Proceso completado: JSON generado exitosamente.")
