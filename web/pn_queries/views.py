from django.http import HttpResponse
from django.shortcuts import render
from .models import Pn_query
from django.http import HttpResponse


def all_pn_queries_view(request):
    context = {'all_pn_queries': Pn_query.objects.all()}
    return render(request, 'all_pn_queries.html', context)
    
