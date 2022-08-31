import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from . import models


# Create your views here.

@login_required
def update_stock(request):
    data = json.loads(request.body)
    pk = data['id']
    stock = data['stock']
    models.TblProduct.objects.filter(pk=pk).update(stock=stock)
    return JsonResponse({'success': True})
