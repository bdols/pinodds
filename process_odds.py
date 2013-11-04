from django.core.management import setup_environ
import datetime, os, time
import pytz

if __name__ != '__main__':
    sys.exit(1)

os.environ['TZ'] = 'US/Eastern'
eastern=pytz.timezone(os.environ['TZ'])
time.tzset()

#import settings
#setup_environ(settings)
import pinodds.settings
setup_environ(pinodds.settings)

from odds.models import *

def creatOddsSample(m,at):
    ss=SampleSet.objects.filter(at_time=at)
    if len(ss) == 0:
        print at
        s = SampleSet()
        s.at_time = at
        s.save()
    else:
        s = ss[0]

    o=OddsSample()
    o.machine = m
    o.at_time = s
    o.value = m.odds_against
    o.save()
    return o

d=datetime.datetime.now()
for m in Machine.objects.all():
    creatOddsSample(m,d)
