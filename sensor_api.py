from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
from typing import Optional

app = FastAPI(title="StockFlow Sensor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    temperatura: float
    humedad: float
    movimiento: bool
    alerta_temp: bool
    alerta_hum: bool
    timestamp: int

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="practica_db",
            port=3306
        )
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

@app.get("/")
async def root():
    return {
        "message": "StockFlow Sensor API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "sensor_data": "/api/sensor-data",
            "latest": "/api/sensor-data/latest",
            "history": "/api/sensor-data/history"
        }
    }

@app.post("/api/sensor-data")
async def receive_sensor_data(data: SensorData):
    print(f"\n📡 Datos recibidos del ESP32:")
    print(f"   🌡️  Temperatura: {data.temperatura}°C")
    print(f"   💧 Humedad: {data.humedad}%")
    print(f"   🚶 Movimiento: {'Detectado' if data.movimiento else 'No detectado'}")
    print(f"   ⚠️  Alerta Temp: {'SÍ' if data.alerta_temp else 'No'}")
    print(f"   ⚠️  Alerta Hum: {'SÍ' if data.alerta_hum else 'No'}")
    
    try:
        conn = get_db_connection()
        if conn is None:
            return {
                "status": "warning",
                "message": "Datos recibidos pero no guardados (BD no disponible)",
                "data": {
                    "temperatura": data.temperatura,
                    "humedad": data.humedad,
                    "movimiento": data.movimiento
                }
            }
        
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sensor_data 
            (temperatura, humedad, movimiento, alerta_temp, alerta_hum, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (
            data.temperatura,
            data.humedad,
            data.movimiento,
            data.alerta_temp,
            data.alerta_hum
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Datos guardados en BD correctamente\n")
        
        return {
            "status": "success",
            "message": "Datos guardados correctamente",
            "data": {
                "temperatura": data.temperatura,
                "humedad": data.humedad,
                "movimiento": data.movimiento,
                "alerta_temp": data.alerta_temp,
                "alerta_hum": data.alerta_hum
            }
        }
    
    except Exception as e:
        print(f"❌ Error guardando en BD: {e}\n")
        return {
            "status": "error",
            "message": str(e),
            "data": {
                "temperatura": data.temperatura,
                "humedad": data.humedad,
                "movimiento": data.movimiento
            }
        }

@app.get("/api/sensor-data/latest")
async def get_latest_data():
    try:
        conn = get_db_connection()
        if conn is None:
            return {"error": "Base de datos no disponible"}
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM sensor_data 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if data:
            return data
        else:
            return {"message": "No hay datos disponibles"}
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/sensor-data/history")
async def get_history(limit: int = 100):
    try:
        conn = get_db_connection()
        if conn is None:
            return {"error": "Base de datos no disponible"}
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(f"""
            SELECT * FROM sensor_data 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        """)
        
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"count": len(data), "data": data}
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/sensor-data/stats")
async def get_stats():
    try:
        conn = get_db_connection()
        if conn is None:
            return {"error": "Base de datos no disponible"}
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                AVG(temperatura) as temp_promedio,
                MIN(temperatura) as temp_minima,
                MAX(temperatura) as temp_maxima,
                AVG(humedad) as hum_promedio,
                MIN(humedad) as hum_minima,
                MAX(humedad) as hum_maxima,
                SUM(movimiento) as total_movimientos,
                COUNT(*) as total_registros
            FROM sensor_data
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return stats if stats else {}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 Iniciando StockFlow Sensor API...")
    print("="*50)
    print(f"📍 API corriendo en: http://0.0.0.0:8000")
    print(f"📚 Documentación: http://localhost:8000/docs")
    print(f"🔧 Panel interactivo: http://localhost:8000/redoc")
    print("="*50 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
