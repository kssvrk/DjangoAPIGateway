from django.shortcuts import render
import requests,json
from requests import get,put,delete,post
# Create your views here.
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from requestmanager.models import IncomingRequest
from ipware import get_client_ip

'''
TODO :
1) Write tests for Non valid request methods.
2) Write appropriate error codes for improper responses
3) Write appropriate error codes for timeouts
'''

#-------- SETUP CLOSE FUNCTIONS----------------
def outgoinginsert(ir,status,size=0):
    try:
        before_size=ir.resp_size
        #print(size,before_size,ir,ir.pk)
        ir.resp_status=status
        ir.resp_size=size+before_size
        ir.save()
    except Exception as e:
        print(e)

#-------- SETUP CLOSE FUNCTIONS DONE----------------        

def index(request):
    return HttpResponse("Hello, world. You're at the router index.")
def stream_rendered(resp,ir,status):
    for chunk in resp.iter_content(512 * 1024):
        outgoinginsert(ir,status,size=len(chunk))
        yield chunk

from .models import GatewayRoute



def proxy(request,path):
    #SITE_NAME='http://172.31.6.22:5495/'
    ip, is_routable = get_client_ip(request)
    ir=None
    try:
        SITE_NAME,timeout,stream,route=GatewayRoute.objects.getLBRoute(path)
        if ip is not None:
            ir=IncomingRequest.objects.create(from_ip=ip,route=route)
        
    except ObjectDoesNotExist:
        status=404
        outgoinginsert(ir,status)
        return JsonResponse(
                status=status,
                data={'status':f"On the URL {path} No configuration found at Gateway",}
                )
    
    accepted_methods=['get','post','put','delete']
    method=request.method.lower()
    if(method in accepted_methods):
        try:
            
            resp = globals()[method](f'{SITE_NAME}',headers=request.headers,data=request.body,timeout=timeout,stream=stream)
            #excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            #headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
            #print(resp.content,resp.status_code,headers)
            if(not stream):
                response = HttpResponse(resp.content, status=resp.status_code)
                for (name,value) in resp.raw.headers.items():
                #if(name.lower() not in excluded_headers):
                    response[name]=value
                status=resp.status_code
                outgoinginsert(ir,status)
                return response
            else:
                size=0
                response = StreamingHttpResponse(
                            stream_rendered(resp,ir,resp.status_code),
                            status=resp.status_code ,
                            )
                for (name,value) in resp.raw.headers.items():
                #if(name.lower() not in excluded_headers):
                    response[name]=value
                return response
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            status=504
            outgoinginsert(ir,status)
            return JsonResponse(
                    status=status,
                    data={'status':f"On the URL {path} , Downstream server didn't respond within expected time",}
                    )
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            status=508
            outgoinginsert(ir,status)
            return JsonResponse(
                status=status,
                data={'status':f"On the URL {path} a loop was detected!",}
                )
        except Exception as e:
            # catastrophic error. bail.
            print(e)
            status=500
            outgoinginsert(ir,status)
            return JsonResponse(
                status=status,
                data={'status':f"On the URL {path} Internal server error occured!",}
                )
    else:
        status=400
        outgoinginsert(ir,status)
        return JsonResponse(
                status=status,
                data={'status':f"Proxying the URL {path} on an Unknown method!",}
                )
        
