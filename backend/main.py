import asyncio, math, random, time, json, sys
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.adapters import discover

app = FastAPI(title='AutoPulse Diagnostics')

@app.get('/api/adapters')
def adapters():
    return discover()
CODES = {'P0300':'Random/multiple cylinder misfire detected','P0420':'Catalyst system efficiency below threshold','P0128':'Coolant thermostat temperature below regulating temperature','P0171':'System too lean (bank 1)'}

@app.get('/api/codes')
def codes(): return CODES

@app.websocket('/ws')
async def telemetry(ws: WebSocket):
    await ws.accept()
    start = time.monotonic()
    try:
        while True:
            t = time.monotonic()-start
            speed = max(0, 45+40*math.sin(t/22))
            rpm = 780+speed*27+random.uniform(-45,45)
            data = {'time': round(t,1),'speed':round(speed,1),'rpm':round(rpm),'coolant':round(22+67*(1-math.exp(-t/35)),1),'voltage':round(14.1+random.uniform(-.15,.15),2),'load':round(20+speed*.65,1),'throttle':round(12+speed*.55,1),'fuel':round(max(0,76-t/3600),1),'mode':'SIMULATED','faults':['P0420'] if int(t//60)%2==1 else []}
            await ws.send_json(data)
            await asyncio.sleep(.5)
    except (WebSocketDisconnect, RuntimeError): pass

root = Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[1]))
web = root/'frontend'/'dist'
if web.exists(): app.mount('/', StaticFiles(directory=web,html=True),name='frontend')
else:
    @app.get('/')
    def index(): return JSONResponse({'message':'Build frontend with npm run build first.'})
