from odds.models import *
from django.shortcuts import render_to_response


# Create your views here.

def table(request):
    data={}
    #data['machines']=Machine.objects.order_by('init_odds')
    data['machines']=[]
    for s in SampleSet.latest().oddssample_set.order_by('value'):
        data['machines'].append(s.machine)
    return render_to_response("table.html",data)
