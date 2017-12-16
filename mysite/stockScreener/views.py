# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Template, Context, loader
import stockScreener
import lookup


def homepage(request):
    symbol = ""
    sp, sma, vol, macd, sto = "", "Value", "Value", "Value", "Value"
    if "symbol" in request.POST:
        symbol = request.POST["symbol"]
        sp = lookup.SMA(symbol)
        sma = lookup.SMA(symbol)
        vol = lookup.Vol(symbol)
        macd = lookup.MACD(symbol)
        sto = lookup.Sto(symbol)
    params = dict()
    params["sp"] = sp
    params["symbol"] = symbol
    params["sma"] = sma
    params["vol"] = vol
    params["macd"] = macd
    params["sto"] = sto
    template = loader.get_template("stockScreener/index.html")
    return HttpResponse(template.render(params, request))

class WatchlistPageView(TemplateView):
    template_name = "stockScreener/watchlist.html"

def list(request):
    returnList = stockScreener.main()
    printList = "<html><body>Results List:: %s.</body></html>" % returnList
    return HttpResponse(printList)


def generate(request):
    if request.path == "/generate/results/":
        returnList = stockScreener.getResults()
    else:
        returnList = []
    params = {"stockList": returnList}
    template = loader.get_template("stockScreener/generate.html")
    return HttpResponse(template.render(params, request))
