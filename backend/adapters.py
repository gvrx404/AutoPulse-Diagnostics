"""Inventory Windows devices only; never opens a port or sends vehicle commands."""
import json
import platform
import re
import subprocess

SCRIPT = r'''$ErrorActionPreference = 'Stop'
Get-PnpDevice -PresentOnly | Where-Object { $_.Class -in @('Bluetooth','Ports') } | Select-Object FriendlyName,Class,Status,InstanceId | ConvertTo-Json -Compress
'''
MARKERS = re.compile(r'elm\s*327|obd\s*[- ]?\s*(?:ii|2|link)?|vlinker|veepeak|vgate|carista|icar\s*pro', re.I)

def classify(rows):
    devices = []
    for row in rows:
        name = str(row.get('FriendlyName') or 'Unnamed device')
        kind = str(row.get('Class') or '')
        instance = str(row.get('InstanceId') or '')
        if kind.lower() not in ('bluetooth', 'ports'):
            continue
        port = re.search(r'\bCOM\d+\b', name, re.I)
        candidate = bool(MARKERS.search(name))
        devices.append({'name': name, 'category': kind, 'os_status': str(row.get('Status') or 'Unknown'), 'port': port.group().upper() if port else None, 'obd_candidate': candidate, 'bluetooth_serial': kind.lower() == 'ports' and instance.upper().startswith('BTHENUM')})
    return sorted(devices, key=lambda d: (not d['obd_candidate'], d['name'].lower()))

def discover():
    if platform.system() != 'Windows':
        return {'status': 'unsupported', 'devices': [], 'message': 'Windows device inventory is available on Windows only.'}
    try:
        result = subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command', '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; '+SCRIPT], capture_output=True, encoding='utf-8', errors='replace', timeout=15, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0), check=True)
        rows = json.loads(result.stdout.strip() or '[]')
        if isinstance(rows, dict): rows = [rows]
        return {'status': 'ok', 'devices': classify(rows), 'message': 'Windows device inventory only. ECU connection not verified.'}
    except (OSError, ValueError, subprocess.SubprocessError):
        return {'status': 'error', 'devices': [], 'message': 'Windows device inventory failed. Check Windows Bluetooth settings and try again.'}
