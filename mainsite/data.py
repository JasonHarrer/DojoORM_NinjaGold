from enum import Enum


class Location:
    def __init__(self, name, minimum, maximum, gamble):
        self.name = name
        self.min = minimum
        self.max = maximum
        self.gamble = gamble

locations = {
              'farm':   Location('farm', 10, 20, False),
              'cave':   Location('cave', 5, 10, False),
              'house':  Location('house', 2, 5, False),
              'casino': Location('casino', 0, 50, True)
            }

# Django cannot access class values directly.  This list of dictionaries
#   is for the Django view version of locations to use to display info.
locations_dict = [
                   locations['farm'].__dict__,
                   locations['cave'].__dict__,
                   locations['house'].__dict__,
                   locations['casino'].__dict__
                 ]

class GambleResult(Enum):
    WIN = 'earned'
    LOSE = 'lost'


class Activity:
    def __init__(self, gamble_result, amount, location, dt):
        self.gamble_result = gamble_result
        self.amount = amount
        self.location = location.__dict__
        self.time = dt

    def __str__(self):
        print(f'Location: {self.location}')
        if self.location['gamble']:
            new_action = f'Entered a {self.location["name"]} and '
            new_action += 'won ' if self.gamble_result == GambleResult.WIN.value else 'lost '
            new_action += f'{self.amount} gold!  '
            new_action += 'Ouch!!!  ' if self.gamble_result == GambleResult.LOSE.value else ''
        else:
            new_action = f'Earned {self.amount} gold from the {self.location["name"]}!  '
        new_action += f'({self.time})'
        return new_action
