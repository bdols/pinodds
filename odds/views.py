from odds.models import *
from django.shortcuts import render_to_response
from django.db.models import Count
from django.contrib import auth
from django.http import HttpResponse
from django.template.context import RequestContext
import simplejson
import pytz,os


# Create your views here.

def table(request):
    data={}
    print request.user
    #data['machines']=Machine.objects.order_by('init_odds')
    data['machines']=[]
    for s in SampleSet.latest().oddssample_set.order_by('value'):
        data['machines'].append(s.machine)
    data['bets']=Bet.objects.filter(user=PinUser.objects.all()[0])
    data['users']=PinUser.objects.annotate(total=Count('bet')).order_by('total')
    data['last5bets']=form_bets_data()
    return render_to_response("table.html",data,context_instance = RequestContext(request))

def form_bets_data():
    tz=pytz.timezone(os.environ['TZ'])
    ret=[]
    for b in Bet.objects.order_by('-at_time')[0:5]:
        entry={}
        entry['machine'] = b.machine.name
        entry['value'] = b.value
        entry['position'] = b.position
        if b.position:
            entry['at_odds'] = round(b.at_odds.value, 2)
        else:
            entry['at_odds'] = round(b.at_odds.reverse_value, 2)
        entry['at_time'] = b.at_time.astimezone(tz).strftime("%b %d %I:%M %p")
        entry['comment'] = b.comment
        entry['user'] = b.user.account.username
        ret.append(entry)
    return ret

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def last5(request):
    data = {}
    data['bets']=form_bets_data()
    json = simplejson.dumps(data, ensure_ascii=False)
    return HttpResponse(json,mimetype='application/javascript')
    
