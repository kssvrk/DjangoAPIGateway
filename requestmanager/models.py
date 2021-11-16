from django.db import models
from router.models import GatewayRoute
# Create your models here.

class IncomingRequest(models.Model):

    from_ip = models.CharField(max_length=40)
    route = models.ForeignKey(GatewayRoute,on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)
    added_date = models.DateTimeField(auto_now_add=True)
    resp_status = models.IntegerField(default=10)
    resp_size = models.IntegerField(default=0)



