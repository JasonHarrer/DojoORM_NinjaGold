from django.shortcuts import render, redirect
from datetime import datetime
from pytz import timezone
from random import randint, choice
from . import data

# Create your views here.

def index(request):
    if not 'activities' in request.session:
        request.session['activities'] = []
    if not 'locations' in request.session:
        request.session['locations'] = data.location_dict
    if not 'currentGold' in request.session:
        request.session['currentGold'] = 0
    currgold = request.session['currentGold']
    return render(request, 'index.html')


def process_money(request):
    loc = data.locations[request.POST['location']]
    amount = randint(loc.min, loc.max)
    won = choice([data.GambleResult.WIN, data.GambleResult.LOSE]) if loc.gamble else data.GambleResult.WIN
    currtime = datetime.now(timezone('America/Chicago')).strftime('%Y/%m/%d %-I:%M %p')
    if loc.gamble and won == data.GambleResult.LOSE:
        request.session['currentGold'] -= amount
    else:
        request.session['currentGold'] += amount
    new_activity = data.Activity(won.value, amount, loc, currtime)
    newgold = request.session['currentGold']
    request.session['activities'].insert(0, (new_activity.__dict__, str(new_activity)))
    actions = request.session['activities']
    
    return redirect('/')

#def farm(request):
#    return process_money(request, data.farm)
#
#def cave(request):
#    return process_money(request, data.cave)
#
#def house(request):
#    return process_money(request, data.house)
#
#def casino(request):
#    return process_money(request, data.casino)

def reset(request):
    request.session.flush()
    return redirect('/')
