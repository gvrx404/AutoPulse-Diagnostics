# AutoPulse Diagnostics

A local automotive telemetry and diagnostic workbench for educational vehicle simulation. No vehicle or adapter is required. All readings and fault events are synthetic; this is not a validated diagnostic or safety tool.

## Features
- Seven live synthetic telemetry channels, updated twice per second
- Rolling 60-second charts, searchable sample DTC library and simulated fault events
- JSON session snapshot export
- React desktop dashboard and local FastAPI WebSocket backend

## Windows quick start
Install Python 3.11 or 3.12, Node.js 22 and Microsoft Edge WebView2 Runtime.

```bat
py -m pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
py launcher.py
```

For browser mode: `py -m uvicorn backend.main:app --host 127.0.0.1 --port 8765`, then visit http://127.0.0.1:8765.

For development, start that backend and run `npm run dev` inside frontend.

## Windows executable
Run `build.bat` to create an application directory under `dist/AutoPulse`. Keep all files in that directory together. This is a portable build, not an installer. No administrator privileges are required. The Windows packaging path has not been validated on Windows.

## Architecture
The backend generates an independent synthetic driving session for each WebSocket connection. The frontend retains up to 120 samples in memory. Reconnecting resets the simulation. The fault library is illustrative and contains four generic codes; it is not comprehensive. The report is a snapshot, not a certified diagnostic report.

## GitHub topics
`automotive`, `vehicle-diagnostics`, `telemetry`, `python`, `react`, `fastapi`, `websocket`, `simulation`, `automobile-engineering`

## v0.2.0 — Windows adapter inventory
The Connections tab refreshes the Windows Plug and Play inventory every eight seconds. It lists present Bluetooth and serial devices, COM labels when available, OS-reported status and possible OBD adapter names (heuristic only). A generic adapter may appear as an ordinary Bluetooth or serial device. Presence does not prove pairing, an active Bluetooth link, adapter authenticity or ECU communication. No ports are opened and no commands are sent. Windows PowerShell and its Get-PnpDevice cmdlet are required. The rest of the dashboard remains synthetic. Windows hardware and executable builds have not been tested.
