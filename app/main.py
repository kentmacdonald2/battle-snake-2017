import bottle
import os
import random
from a_star import search

taunts = [
    'i am courtney, hear me roar',
    'BEAMZ HUNGRY',
]

class food():
    def __init__(self, loc, sld):
        self.loc = loc
        self.sld = sld


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    global_board_height = board_height
    global_board_width = board_width
    
    return {
        'color': '#FF00FF',
        'taunt': random.choice(taunts),
        'head_url': 'https://cvws.icloud-content.com/CAEQARoQIXZCvczX_7a27NPmpe95GQ/0191b84e87ff1a08720e9186b86339bd2e8e8c854a/output.jpg?v=0&z=https://p28-content.icloud.com:443&x=1&a=BhVl218Uf32vVuzvjFyEj9iWRwPWAx%2BROQEAAA%3D%3D&e=1488666178000&r=4a7b14fa-6860-4ba3-ad4c-13b8d71a341e-1&c=&s=f4fmJgIh6Otmw4bAjZ71BlnsmO0',
        'name': 'beames.ai'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    direction = 'up'

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    food_list = data.get('food')

    snakes = data.get('snakes')
    # TODO: Change this so it actually checks if the snake is ours
    for snake in snakes:
        if data.get('you') == snake.get('id'):
            snake_coords = snake.get('coords')
    snake_head = snake_coords[0]
    board_width = data.get('width')
    board_height = data.get('height')

    sorted_list = get_food_list(snake_head, data)
    first_food = sorted_list[0].loc

    primary_path = search(snake_head, data, first_food)
    sec_path = None

    if len(sorted_list) > 1:
        sec_food = sorted_list[1]
        new_list = get_food_list(first_food, data)
        sec_path = search(first_food, data, new_list[0].loc)
        new_path = search(snake_head, data, new_list[0].loc)

    if len(sorted_list) > 1:
        if not primary_path and sec_path:
            primary_path = new_path

    if len(sorted_list) > 1:
        if not sec_path:
            primary_path = search(snake_head, data, sec_food.loc)


    if not primary_path:
        #Desperation Move
        if (if_safe(up(snake_head,1), data)):
            return {
                'move': 'up',
                'taunt': random.choice(taunts),
            }
        if (if_safe(down(snake_head,1), data)):
            return {
                'move': 'down',
                'taunt': random.choice(taunts),
            }
        if (if_safe(left(snake_head,1), data)):
            return {
                'move': 'left',
                'taunt': random.choice(taunts),
            }
        if (if_safe(right(snake_head,1),data)):
            return {
                'move': 'right',
                'taunt': random.choice(taunts),
            }
    else:
        first_move = primary_path[-1]
        if (up(snake_head, 1) == first_move):
            direction = 'up'
        if (down(snake_head, 1) == first_move):
            direction = 'down'
        if (left(snake_head, 1) == first_move):
            direction = 'left'
        if (right(snake_head, 1) == first_move):
            direction = 'right'

    return {
        'move': direction,
        'taunt': random.choice(taunts),
    }

def get_inverse_coord(board_width, board_height, data, snake_head):
    x = board_width - snake_head[0]
    y = board_height - snake_head[1]
    if if_safe([x, y], data):
        return [x, y]

    pos = [x,y]
    rad = 1
    while True:
        if if_safe(up(pos, rad), data):
            return up(pos, rad) 
        if if_safe(down(pos, rad), data):
            return down(pos, rad) 
        if if_safe(right(pos, rad), data):
             return right(pos, rad) 
        if if_safe(left(pos, rad), data):
            return left(pos, rad) 
        rad += 1

def get_food_list(snake_head, data):
    food_list = data.get('food')
    current_mindex = 0
    current_min_score = 999999
    l = []
    for current_food in food_list:
        current_distance = [99, 99]
        current_distance[0] = snake_head[0] - current_food[0]
        current_distance[1] = snake_head[1] - current_food[1]
        current_distance[0] = current_distance[0] * current_distance[0]
        current_distance[1] = current_distance[1] * current_distance[1]
        current_score = current_distance[0] + current_distance[1]
        l.append(food(current_food, current_score)) 

    l.sort(key=lambda x: x.sld)
    return l

def if_safe(new_snake_head, data):
    snakes = data.get('snakes')
    our_id = data.get('you')
    board_width = data.get('width')
    board_height = data.get('height')

    # print("Snakes List -> " +snakes.__str__())
    for snake in snakes:
        if new_snake_head in snake.get('coords'):
            return False
    # If new position is off the board
    if new_snake_head[1] < 0:
        return False
    if new_snake_head[1] > board_height-1:
        return False
    if new_snake_head[0] < 0:
        return False
    if new_snake_head[0] > board_width-1:
        return False
    return True


def up(old_snake_head, rad):
    return [old_snake_head[0], old_snake_head[1] - rad]


def down(old_snake_head, rad):
    return [old_snake_head[0], old_snake_head[1] + rad]


def left(old_snake_head, rad):
    return [old_snake_head[0] - rad, old_snake_head[1]]


def right(old_snake_head, rad):
    return [old_snake_head[0] + rad, old_snake_head[1]]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8000'))
