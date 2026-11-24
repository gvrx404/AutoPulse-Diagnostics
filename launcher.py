import threading, socket, time
import uvicorn
import webview
from backend.main import app

if __name__ == '__main__':
    sock=socket.socket(); sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]; sock.listen(128)
    server=uvicorn.Server(uvicorn.Config(app,log_level='warning'))
    thread=threading.Thread(target=lambda:server.run(sockets=[sock]),daemon=True); thread.start()
    for _ in range(100):
        if server.started: break
        time.sleep(.05)
    else: raise RuntimeError('Backend failed to start')
    webview.create_window('AutoPulse Diagnostics',f'http://127.0.0.1:{port}',width=1250,height=850,min_size=(850,650))
    webview.start(gui='edgechromium')
    server.should_exit=True
    thread.join(timeout=3)
