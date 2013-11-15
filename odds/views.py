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
    data['machines']=[]
    for s in SampleSet.latest().oddssample_set.order_by('value'):
        data['machines'].append(s.machine)
    data['bets']=Bet.objects.filter(user=PinUser.objects.all()[0])
    data['tickets']=PinUser.objects.get(account=request.user).open_tickets
    data['users']=PinUser.objects.annotate(total=Count('bet')).order_by('total')
    data['last5bets']=form_bets_data()
    return render_to_response("table.html",data,context_instance = RequestContext(request))

def bet(request):
    data={}
    try:
        if not request.user.is_authenticated:
            raise Exception, "Unauthorized. Please login"
        ticket=Ticket.objects.get(id=int(request.POST['tickid']))
        value=int(request.POST['value'])
        if ticket.value<=value:
            raise Exception, "Only %d left and you chose %d pinbucks" % (ticket.value, value)
        b=Bet()
        b.machine=Machine.objects.get(id=request.POST['machid'])
        b.ticket=Ticket.objects.get(id=int(request.POST['tickid']))
        b.value=value
        b.position=request.POST['position']
        b.comment=request.POST['comment']
        b.at_odds=OddsSample.objects.get(at_time=SampleSet.latest(),machine=b.machine)
        b.user=PinUser.objects.get(account=request.user)
        b.save()
        data['result']=True
    except Exception,e :
        print e
        data['result']=False
        data['message']=str(e)
    
    json = simplejson.dumps(data, ensure_ascii=False)
    return HttpResponse(json,mimetype='application/javascript')

def form_bets_data():
    ret=[]
    for b in Bet.objects.order_by('-at_time')[0:5]:
        ret.append(form_bets_dict(b))
    return ret

def form_bets_dict(b):
    tz=pytz.timezone(os.environ['TZ'])
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
    return entry

def login (request):
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

def tickets (request,userid):
    data = []
    for t in Ticket.objects.filter(user=PinUser.objects.get(account=User.objects.get(id=userid))):
        tick={}
        tick['tickid']=t.id
        tick['value']=t.value
        tick['bets']=[]
        for b in t.bet_set.all():
            tick['bets'].append(form_bets_dict(b))
        data.append(tick)
    json = simplejson.dumps(data, ensure_ascii=False)
    return HttpResponse(json,mimetype='application/javascript')
    
def last5 (request):
    data = {}
    data['bets']=form_bets_data()
    json = simplejson.dumps(data, ensure_ascii=False)
    return HttpResponse(json,mimetype='application/javascript')
