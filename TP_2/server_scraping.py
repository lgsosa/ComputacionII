import argparse
import asyncio
from datetime import datetime, timedelta
import socket
import time
import base64
from urllib.parse import urlparse, urljoin

import aiohttp
from aiohttp import web, ClientError

from scraper.async_http import fetch_html
from scraper.html_parser import parse_structure, extract_title_and_links
from scraper.metadata_extractor import extract_meta
from common.protocol import send_message, receive_message

PROCESSING_IP = "127.0.0.1"
PROCESSING_PORT = 9000

CACHE = {}
CACHE_TTL = 3600

RATE = {}
RATE_LIMIT = 5

def check_rate(url):
    domain = urlparse(url).netloc
    now = time.time()
    RATE.setdefault(domain, [])
    RATE[domain] = [t for t in RATE[domain] if t > now-60]
    if len(RATE[domain]) >= RATE_LIMIT:
        return False
    RATE[domain].append(now)
    return True

def get_cache(url):
    item = CACHE.get(url)
    if not item:
        return None
    ts = datetime.fromisoformat(item["timestamp"].replace("Z",""))
    if datetime.utcnow() - ts > timedelta(seconds=CACHE_TTL):
        CACHE.pop(url,None)
        return None
    return item

def save_cache(url, data):
    CACHE[url] = data

async def download_images(url, list_src, maxx=3):
    if not list_src:
        return []
    imgs=[]
    async with aiohttp.ClientSession() as s:
        for src in list_src[:maxx]:
            try:
                full=urljoin(url,src)
                async with s.get(full) as r:
                    if r.status==200:
                        imgs.append(await r.read())
            except:
                continue
    return imgs

async def call_processor(payload):
    loop=asyncio.get_event_loop()

    def sync():
        with socket.create_connection((PROCESSING_IP,PROCESSING_PORT),timeout=10) as sock:
            send_message(sock,payload)
            return receive_message(sock)

    return await loop.run_in_executor(None,sync)

async def handle(request):
    url=request.rel_url.query.get("url")
    if not url:
        return web.json_response({"status":"error","error":"falta url"},status=400)

    if not check_rate(url):
        return web.json_response({"status":"error","error":"muchas requests a este dominio"},status=429)

    c=get_cache(url)
    if c:
        return web.json_response(c)

    try:
        html,load=await fetch_html(url)
    except asyncio.TimeoutError:
        return web.json_response({"status":"error","error":"timeout"},status=504)
    except ClientError as e:
        return web.json_response({"status":"error","error":str(e)},status=502)
    except Exception as e:
        return web.json_response({"status":"error","error":str(e)},status=502)

    structure=parse_structure(html)
    basic=extract_title_and_links(html)
    meta=extract_meta(html)

    images_bytes=await download_images(url,basic["images"])
    imgs_b64=[base64.b64encode(x).decode("ascii") for x in images_bytes]

    payload={
        "url":url,
        "html":html,
        "load_time_ms":load,
        "num_requests":1,
        "images_bytes":imgs_b64
    }

    try:
        p=await call_processor(payload)
    except Exception as e:
        result={
            "url":url,
            "timestamp":datetime.utcnow().isoformat()+"Z",
            "scraping_data":{
                "title":basic["title"],
                "links":basic["links"],
                "meta_tags":meta,
                "structure":structure,
                "images_count":basic["images_count"]
            },
            "processing_data":{},
            "status":"error_processing",
            "error":str(e)
        }
        save_cache(url,result)
        return web.json_response(result,status=500)

    result={
        "url":url,
        "timestamp":datetime.utcnow().isoformat()+"Z",
        "scraping_data":{
            "title":basic["title"],
            "links":basic["links"],
            "meta_tags":meta,
            "structure":structure,
            "images_count":basic["images_count"]
        },
        "processing_data":p.get("processing_data",{}),
        "status":"success"
    }
    save_cache(url,result)
    return web.json_response(result)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("-i","--ip",required=True)
    p.add_argument("-p","--port",required=True,type=int)
    p.add_argument("--processing-ip",default="127.0.0.1")
    p.add_argument("--processing-port",default=9000,type=int)
    a=p.parse_args()

    global PROCESSING_IP,PROCESSING_PORT
    PROCESSING_IP=a.processing_ip
    PROCESSING_PORT=a.processing_port

    app=web.Application()
    app.router.add_get("/scrape",handle)
    web.run_app(app,host=a.ip,port=a.port)

if __name__=="__main__":
    main()
