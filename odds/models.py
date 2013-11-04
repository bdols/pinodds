from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import Max

# Create your models here.

class Machine(models.Model):
    name = models.CharField(max_length=40,unique=True)
    init_odds = models.IntegerField()
    @property
    def bet_count(self):
        return self.bet_set.count()
    @property
    def current_odds(self):
        sample = self.oddssample_set.filter(at_time=SampleSet.latest())
        return sample[0].value
    @property
    def current_reverse_odds(self):
        sample = self.oddssample_set.filter(at_time=SampleSet.latest())
        odds = sample[0].value
        return round(float(odds)/(odds-1),2)
    @property
    def odds_against(self):
        for_val=0
        for b in self.bet_set.filter(position=True):
            for_val += b.value
        all_bets=0
        for c in Bet.objects.all():
            all_bets+=c.value
        #if all_val==0:
            #return self.init_odds
        #print all_bets,for_val,self.init_odds
        return round((5000+all_bets)/(for_val+int(5000/self.init_odds)),2)
    def probability(self):
        return 1/(self.odds_against()+1)
    def __unicode__(self):
        return self.name + " at %d" % self.init_odds + ":1"
class SampleSet(models.Model):
    at_time = models.DateTimeField()

    @staticmethod
    def latest():
        at = SampleSet.objects.aggregate(Max('at_time'))['at_time__max']
        return SampleSet.objects.filter(at_time=at)[0]
    def __unicode__(self):
        return self.at_time.strftime("%b %d %H:%M")

class OddsSample(models.Model):
    at_time = models.ForeignKey('SampleSet')
    machine = models.ForeignKey('Machine')
    value = models.IntegerField()
    def __unicode__(self):
        return self.machine.name + " at %d" % self.value + ":1 at " + self.at_time.at_time.strftime("%b %d %H:%M")

class PinUser(models.Model):
    account = models.OneToOneField(User)
    wppr = models.IntegerField()
    email = models.CharField(max_length=140)
    def __unicode__(self):
        return self.account.username 

class Bet(models.Model):
    machine = models.ForeignKey('Machine')
    value = models.IntegerField()
    user = models.ForeignKey("PinUser")
    position = models.BooleanField()
    comment = models.CharField(max_length=140,default="")
    at_time = models.DateTimeField(auto_now=True)
    at_odds = models.ForeignKey("OddsSample")

admin.site.register(Machine)
admin.site.register(PinUser)
admin.site.register(OddsSample)
admin.site.register(Bet)
