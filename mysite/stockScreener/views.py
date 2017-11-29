# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
import stockScreener

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        template_name = "index.html"
        return render(request, 'index.html', context=None)       

class WatchlistPageView(TemplateView):
    template_name = "watchlist.html"

class GeneratePageView(TemplateView):
    template_name = "generate.html"

def submit(request):
    if request.method == 'POST':
        output = subprocess.check_output(['python', 'script.py'])
        return HttpResponse(output, content_type="text/plain")
