from odds.models import *
from django.shortcuts import render_to_response
from django.db.models import Count


# Create your views here.

def table(request):
    data={}
    #data['machines']=Machine.objects.order_by('init_odds')
    data['machines']=[]
    for s in SampleSet.latest().oddssample_set.order_by('value'):
        data['machines'].append(s.machine)
    data['bets']=Bet.objects.filter(user=PinUser.objects.all()[0])
    data['users']=PinUser.objects.annotate(total=Count('bet')).order_by('total')
    data['last5bets']=Bet.objects.order_by('-at_time')[0:5]
    return render_to_response("table.html",data)
