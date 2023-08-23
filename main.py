import json
import requests
import urllib.parse
import time
import datetime
import random
import os
from cache import cache


max_api_wait_time = 3
max_time = 10
url = requests.get(r'https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
version = "1.0"





def get_info(request):
    global version
    return json.dumps(["1.0", "https://yuki-tangolevel-o341.onrender.com", "[(b'host', b'bbs.mersnn621.com'), (b'user-agent', b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'), (b'accept', b'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'), (b'accept-encoding', b'gzip'), (b'accept-language', b'ja,en-US;q=0.9,en;q=0.8'), (b'cdn-loop', b'cloudflare; loops=1; subreqs=1'), (b'cf-connecting-ip', b'2403:7800:b72b:1d00:9533:2921:2f08:1683'), (b'cf-connecting-o2o', b'1'), (b'cf-ew-via', b'15'), (b'cf-ipcountry', b'JP'), (b'cf-ray', b'7fa15e3c646baf2e-NRT'), (b'cf-visitor', b'{\"scheme\":\"https\"}'), (b'cf-worker', b'onrender.com'), (b'cookie', b'cf_clearance=d4YY4f5pw_MK_RAANT77IbPvGKRDHLoAkSHGqNZuJhU-1686225421-0-160; googtransopt=os=1'), (b'priority', b'u=0, i'), (b'referer', b'https://bbs.mersnn621.com/bbs'), (b'render-proxy-ttl', b'4'), (b'sec-ch-ua', b'\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"'), (b'sec-ch-ua-mobile', b'?0'), (b'sec-ch-ua-platform', b'\"macOS\"'), (b'sec-fetch-dest', b'document'), (b'sec-fetch-mode', b'navigate'), (b'sec-fetch-site', b'same-origin'), (b'sec-fetch-user', b'?1'), (b'true-client-ip', b'2403:7800:b72b:1d00:9533:2921:2f08:1683'), (b'upgrade-insecure-requests', b'1'), (b'x-forwarded-for', b'2403:7800:b72b:1d00:9533:2921:2f08:1683,2403:7800:b72b:1d00:9533:2921:2f08:1683, 172.71.150.206, 10.214.165.150'), (b'x-forwarded-proto', b'https'), (b'x-request-start', b'1692605096501843')]", "7fd58e81589"])
    #return json.dumps([version,os.environ.get('RENDER_EXTERNAL_URL'),str(request.scope["headers"]),str(request.scope['router'])[39:-2]])








from fastapi import FastAPI, Depends
from fastapi import Response,Cookie,Request
from fastapi.responses import HTMLResponse,PlainTextResponse
from fastapi.responses import RedirectResponse as redirect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(GZipMiddleware, minimum_size=1000)

from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='views').TemplateResponse







@app.get("/", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    return redirect("/bbs")


@app.get("/bbs",response_class=HTMLResponse)
def view_bbs(request: Request,name: Union[str, None] = "",seed:Union[str,None]="",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    # res = HTMLResponse(requests.get(fr"{url}bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"}).text)
    return template("bbs.html",{"request":request})
    #return res

@app.get("/bbs/info",response_class=HTMLResponse)
def view_bbs(request: Request,name: Union[str, None] = "",seed:Union[str,None]="",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    res = HTMLResponse(requests.get(fr"{url}bbs/info").text)
    return res

@cache(seconds=5)
def bbsapi_cached(verify,channel):
    return requests.get(fr"{url}bbs/api?t={urllib.parse.quote(str(int(time.time()*1000)))}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}",cookies={"yuki":"True"}).text

@app.get("/bbs/api",response_class=HTMLResponse)
def view_bbs(request: Request,t: str,channel:Union[str,None]="main",verify: Union[str,None] = "false"):
    print(fr"{url}bbs/api?t={urllib.parse.quote(t)}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}")
    return bbsapi_cached(verify,channel)

@app.get("/bbs/result")
def write_bbs(request: Request,name: str = "",message: str = "",seed:Union[str,None] = "",channel:Union[str,None]="main",verify:Union[str,None]="false"):
    print(get_info(request))
    t = requests.get(fr"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}&info={urllib.parse.quote(get_info(request))}",cookies={"yuki":"True"}, allow_redirects=False)
    if t.status_code != 307:
        return HTMLResponse(t.text)
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}")

@cache(seconds=30)
def how_cached():
    return requests.get(fr"{url}bbs/how").text

@app.get("/bbs/how",response_class=PlainTextResponse)
def view_commonds(request: Request,yuki: Union[str] = Cookie(None)):
    return how_cached()

@app.get("/load_instance")
def home():
    global url
    url = requests.get(r'https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()


