from django.db import models
from random import randint
# Create your models here.

'''
API Gateway core model. This model describes the configuration entries for API Gateway.
The API Endpoint on the gateway will route to the target microservice URL.
Microservice URL be a full path along with the host and port as applied ( for internal route balancing  if applied, if not just the full service URL)

'''

#example /heartbeat
class GatewayEndpoint(models.Model):
    endpoint_id = models.AutoField(primary_key=True)
    endpoint_description = models.CharField(max_length=200)
    endpoint_path = models.CharField(max_length=100,unique=True)
    updated_date = models.DateTimeField(auto_now=True)
    added_date = models.DateTimeField(auto_now_add=True)
    stream = models.BooleanField(default=False)
    def __str__(self):
        return f"Gateway Endpoint : {self.endpoint_path}"

#example https://microservice/heartbeat
class TargetURL(models.Model):
    url_id = models.AutoField(primary_key=True)
    url_description = models.CharField(max_length=200)
    url_path = models.CharField(max_length=300,unique=True)
    updated_date = models.DateTimeField(auto_now=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TargetURL : {self.url_path}"

'''
Gateway route will proxy the Gateway Endpoint, to a one to many relationship of endpoint routes.

This can also emulate a single target , a direct route when the one to many becomes => one to one
'''
class GatewayRouteManager(models.Manager):

    def getLBRoute(self,endpoint):
        ep=GatewayEndpoint.objects.get(endpoint_path=endpoint)
        routes=list(GatewayRoute.objects.filter(endpoint=ep).filter(activate=True))
        
        getpk=randint(0,len(routes)-1)
        #returns url,timeout,stream,route
        return TargetURL.objects.filter(pk=routes[getpk].targeturl.pk).values('url_path')[0]['url_path'],routes[getpk].timeout,ep.stream,routes[getpk]
        #return routes[randint(0,routes.count()-1)]
        
        
        #

class GatewayRoute(models.Model):
    #end point at the gateway => https://gateway/{endpoint}
    endpoint = models.ForeignKey(GatewayEndpoint,on_delete=models.CASCADE)
    #target route to which request is to be proxied by the gateway => https://microservice/
    targeturl=models.ForeignKey(TargetURL,on_delete=models.CASCADE)
    #primary key for identifying this route
    route_id= models.AutoField(primary_key=True)
    added_date = models.DateTimeField(auto_now_add=True)
    activate=models.BooleanField(default=True)
    timeout=models.IntegerField(default=10)
    objects = GatewayRouteManager()
    class Meta:
        unique_together = ('endpoint', 'targeturl',)

    def __str__(self):
        return f"GatewayRoute : on  {self.endpoint} to {self.targeturl}"





