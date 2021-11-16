from django.shortcuts import render
import requests,json

# Create your views here.
from django.http import HttpResponse,JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the router index.")

from .models import GatewayRoute


def proxy(request,path):
    #SITE_NAME='http://172.31.6.22:5495/'
    print(path)
    SITE_NAME=GatewayRoute.objects.getLBRoute(path)
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}',headers=request.headers,data=request.body)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        #print(resp.content,resp.status_code,headers)
        response = HttpResponse(resp.content, status=resp.status_code)
        for (name,value) in resp.raw.headers.items():
            if(name.lower() not in excluded_headers):
                response[name]=value
        return response

    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}',headers=request.headers,data=request.body)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = HttpResponse(resp.content, status=resp.status_code)
        for (name,value) in resp.raw.headers.items():
            if(name.lower() not in excluded_headers):
                response[name]=value
        return response

    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}',headers=request.headers,data=request.body)
        response = HttpResponse(resp.content, status=resp.status_code)
        for (name,value) in resp.raw.headers.items():
            if(name.lower() not in excluded_headers):
                response[name]=value
        return response

    else:
        return HttpResponse(f"Proxying the URL {path} on an Unknown method!")
