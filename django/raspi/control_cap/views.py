from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from  . import pi_control 

import os
import time

def control(request):
    context={}
    if request.method=='GET':
        command=request.GET.get('command')
        if command=='start':
            pi_control.start()
            context['res']='开启完成'
        if command=='stop':
            pi_control.stop()
            context['res']='关闭完成'
        if command=='del':
            pi_control.del_video()
            context['res']='删除完毕'
        if command=='down_rope':
            pi_control.down_rope(1)
            context['res']='正在下降...'
    return render(request,'control.html',context)