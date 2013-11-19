from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import Max
from django.db.models.signals import post_save

# Create your models here.

class Machine(models.Model):
    name = models.CharField(max_length=40,unique=True)
    init_odds = models.IntegerField()
    @property
    def bet_count(self):
        return self.bet_set.filter(position=True).count()
    @property
    def reverse_bet_count(self):
        return self.bet_set.filter(position=False).count()
    @property
    def current_odds(self):
        sample = self.oddssample_set.filter(at_time=SampleSet.latest())
        return round(sample[0].value,2)
    @property
    def current_reverse_odds(self):
        sample = self.oddssample_set.filter(at_time=SampleSet.latest())
        odds = sample[0].reverse_value
        return round(odds,2)
    @property
    def odds_against(self):
        for_val = 0.0
        for b in self.bet_set.filter(position=True):
            for_val += b.value
        against_val = 0
        for b in self.bet_set.filter(position=False):
            against_val += b.value
        for b in Bet.objects.filter(position=False).exclude(machine=self):
            for_val += b.value/(9*float(Machine.objects.count()))
        all_bets = 0
        for c in Bet.objects.filter(position=True):
            all_bets += c.value
        for c in Bet.objects.filter(position=False):
            all_bets += c.value/float(Machine.objects.count())
        print all_bets,for_val,self.init_odds
        pool=5000.0
        return round((pool+against_val+all_bets)/(for_val+pool/self.init_odds),2)
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
    value = models.DecimalField(max_digits=8,decimal_places=2)

    @property
    def reverse_value(self):
        odds = self.value
        return float(odds)/float(odds-1)

    def __unicode__(self):
        return self.machine.name + " at %d" % self.value + ":1 at " + self.at_time.at_time.strftime("%b %d %H:%M")

class PinUser(models.Model):
    account = models.OneToOneField(User)
    wppr = models.IntegerField(default=0)
    @property
    def total_bets(self):
        return self.bet_set.count()
    @property
    def bet_count(self):
        return self.bet_set.filter(position=True).count()
    @property
    def reverse_bet_count(self):
        return self.bet_set.filter(position=False).count()
    @property
    def open_tickets(self):
        return Ticket.objects.filter(user=self)
    def __unicode__(self):
        return "%s's profiles" % self.account.username 

def create_pinuser(sender, instance, created, **kwargs):
    if created:
        profile,created = PinUser.objects.get_or_create(account=instance)
        if created:
            print "create ticket"
            Ticket.objects.create(user=profile,available_value=1000)
            print "created ticket"


post_save.connect(create_pinuser, sender=User)

class Ticket(models.Model):
    user = models.ForeignKey("PinUser")
    available_value = models.IntegerField()
    @property
    def value(self):
        ret = self.available_value
        for b in self.bet_set.all():
            ret -= b.value
        return ret
    def __unicode__(self):
        return "%s %s" % (self.user.account.username, self.available_value)

class Bet(models.Model):
    machine = models.ForeignKey('Machine')
    ticket = models.ForeignKey("Ticket")
    user = models.ForeignKey("PinUser")
    value = models.IntegerField()
    position = models.BooleanField()
    comment = models.CharField(max_length=140,default="")
    at_time = models.DateTimeField(auto_now=True)
    at_odds = models.ForeignKey("OddsSample")

admin.site.register(Machine)
admin.site.register(PinUser)
admin.site.register(OddsSample)
admin.site.register(Bet)
admin.site.register(Ticket)
