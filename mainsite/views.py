from django.shortcuts import render, redirect
from datetime import datetime
from pytz import timezone
from random import randint, choice
from . import data

# Create your views here.

def index(request):
    if ((not 'activities' in request.session) or
        (not 'locations' in request.session) or
        (not 'currentGold' in request.session)):
           return redirect ('/start')
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
    newamt = request.session['currentGold']
    request.session['activities'].insert(0, (new_activity.__dict__, str(new_activity)))
    actions = request.session['activities']
    
    # For turns, increment the turn counter and check to see if end of game.
    print(f'Game Scenario: {request.session["game_scenario"]}')
    request.session['turns'] += 1
    if ((request.session['game_scenario'] == 'turns') and
        (request.session['turns'] > request.session['game_amount'])):
        print('Turns')
        return redirect('/game-over')

    # For amounts, check if the win scenario met
    if request.session['game_scenario'] == 'amount':
        print('Amount')
        if request.session['currentGold'] > request.session['game_amount']:
            print('current gold > game amount')
            return redirect('/game-over')

    # Check if the user elected to allow loss and if they went below 0.
    print(request.session['game_allow_loss'])
    if request.session['currentGold'] < 0 and request.session['game_allow_loss'] == True:
        print('you lose!')
        return redirect('/game-over')
    return redirect('/')


def start(request):
    request.session['activities'] = []
    request.session['locations'] = data.locations_dict
    request.session['currentGold'] = 0
    request.session['turns'] = 1
    request.session['game_scenario'] = ''
    request.session['game_amount'] = 0
    request.session['game_allow_loss'] = True
    return render(request, 'start.html')


def process_game(request):
    request.session['game_scenario'] = request.POST['scenario']
    request.session['game_amount'] = int(request.POST['amount'])
    request.session['game_allow_loss'] = True if request.POST['loss'] == 'on' else False
    return redirect('/')


def game_over(request):
    return render(request, 'gameover.html')


def reset(request):
    request.session.flush()
    return redirect('/start')


