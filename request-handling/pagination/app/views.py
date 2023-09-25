from csv import DictReader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from app.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse(bus_stations))

def bus_stations(request):
    content_list = []
    with open(BUS_STATION_CSV, encoding='cp1251') as stops_file:
        for row in DictReader(stops_file):
            content_list.append(row)
    paginator = Paginator(content_list, 10)
    current_page = int(request.GET.get('current_page', 1))
    bus_stations = paginator.get_page(current_page)
    if bus_stations.has_next():
        next_page_url = bus_stations.next_page_number()
    else:
        next_page_url = None
    if bus_stations.has_previous():
        prev_page_url = bus_stations.previous_page_number()
    else:
        prev_page_url = None
    context = {
        'bus_stations': bus_stations,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
    return render(request, 'index.html', context)