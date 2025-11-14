import argparse
import socketserver
from socketserver import ThreadingMixIn
from concurrent.futures import ProcessPoolExecutor
import traceback
import base64

from common.protocol import send_message, receive_message
from processor.screenshot import generate_screenshot_placeholder
from processor.performance import analyze_performance
from processor.image_processor import generate_thumbnails_from_bytes

def process_task(data):
    url = data["url"]
    html = data["html"]
    load = data["load_time_ms"]
    reqs = data["num_requests"]
    imgs = [base64.b64decode(x) for x in data["images_bytes"]]

    screenshot = generate_screenshot_placeholder(url)
    perf = analyze_performance(html, load, reqs)
    thumbs = generate_thumbnails_from_bytes(imgs)

    return {
        "screenshot": screenshot,
        "performance": perf,
        "thumbnails": thumbs
    }

class Server(ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class Handler(socketserver.BaseRequestHandler):
    executor = None
    def handle(self):
        try:
            data = receive_message(self.request)
            res = Handler.executor.submit(process_task, data).result()
            send_message(self.request, {"status":"ok","processing_data":res})
        except Exception as e:
            traceback.print_exc()
            send_message(self.request, {"status":"error","error":str(e)})

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i","--ip",required=True)
    p.add_argument("-p","--port",required=True,type=int)
    p.add_argument("-n","--processes",default=4,type=int)
    a=p.parse_args()

    with ProcessPoolExecutor(a.processes) as ex:
        Handler.executor = ex
        with Server((a.ip,a.port), Handler) as s:
            print(f"[processing] escuchando en {a.ip}:{a.port}")
            s.serve_forever()

if __name__=="__main__":
    main()
