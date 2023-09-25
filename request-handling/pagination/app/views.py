from csv import DictReader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse(bus_stations))

def bus_stations(request):
    bus_stations = DictReader(BUS_STATION_CSV)
    paginator = Paginator(bus_stations, 10)
    current_page = 1
    next_page_url = int(request.GET.get('page', 1))  # 'write your url'
    return render(request, 'index.html', context={
        'bus_stations': [{'Name': 'название', 'Street': 'улица', 'District': 'район'},
                         {'Name': 'другое название', 'Street': 'другая улица', 'District': 'другой район'}],
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
    })