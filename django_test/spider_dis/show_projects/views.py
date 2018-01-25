import json

from django.shortcuts import render,redirect
from django import http
import requests
# Create your views here.
def show_pros(request):
    res = requests.get('http://47.52.216.38:6800/listprojects.json')
    response = json.loads(res.text)
    projects = response.get('projects')
    node_name = response.get('node_name')
    return render(request,'show_projects.html',{'p':projects,'n':node_name})

def show_spiders(request):
    args = request.GET.get('project')
    res = requests.get('http://47.52.216.38:6800/listspiders.json?project={}'.format(args))
    response = json.loads(res.text)
    return render(request,'show_spider.html',{'s':response,'p':args})

def start_spider(request):
    # curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider
    spider_name = request.GET.get('spider')
    project = request.GET.get('project')
    res = requests.post(url='http://47.52.216.38:6800/schedule.json',data={'project':project,'spider':spider_name})
    response = json.loads(res.text)
    return render(request,'results.html',{'res':response})