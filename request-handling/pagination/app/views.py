from csv import DictReader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from app.settings import BUS_STATION_CSV
from pprint import pprint

def index(request):
    return redirect(reverse(bus_stations))

def bus_stations(request):
    content_list = []
    # print(f'ЭТО ПУТЬ: {BUS_STATION_CSV}')
    with open(BUS_STATION_CSV, encoding='cp1251') as stops_file:
        for row in DictReader(stops_file):
            # print(f'row: {row}')
            content_list.append(row)
    current_page = int(request.GET.get('current_page', 1))
    next_page_url = int(request.GET.get('next_page', 1))  # 'write your url'
    paginator = Paginator(content_list, 10)
    bus_stations = paginator.get_page(current_page)
    context = {
        'bus_stations': bus_stations,
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
    }
    return render(request, 'index.html', context)