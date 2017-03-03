import bottle
import os
import random


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
    
    print ("********************START DUMP"+data.__str__())
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FF00FF',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Kents Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    direction = 'up'

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    print ("MOVE DUMP" + data.__str__())
    print ("Food: "+data.get('food').__str__())
    print ("Items: " + data.items().__str__())
    food_list = data.get('food')

    snakes = data.get('snakes')
    #TODO: Change this so it actually checks if the snake is ours
    snake_coords = snakes[0].get('coords')
    snake_head = snake_coords[0]
    board_width = data.get('width')
    board_height = data.get('height')

    print ("Snake_Head ->  " + snake_head.__str__())
    #print ("First_Food -> "+ first_food.__str__())

    first_food = food_list[find_closest_food_index(snake_head, data)]


    if (first_food[1] < snake_head[1]) and (if_safe(up(snake_head), data)):
        print ("Going UP")
        direction = 'up'

    elif( first_food[1] > snake_head[1]) and (if_safe(down(snake_head), data)):
        direction = 'down'
        print ("Going DOWN")

    elif( first_food[0] < snake_head[0]) and (if_safe(left(snake_head), data)):
        direction = 'left'
        print ("Going LEFT")

    elif(first_food[0] > snake_head[0]) and (if_safe(right(snake_head), data)):
        direction = 'right'
        print ("Going RIGHT")

    else:
        if (if_safe(up(up(snake_head)), data)) and (if_safe(up(snake_head), data)):
            direction = 'up'
        elif if_safe(down(down(snake_head)), data) and if_safe(down(snake_head), data):
            direction = 'down'
        elif if_safe(left(left(snake_head)), data) and if_safe(left(snake_head), data):
            direction = 'left'
        elif if_safe(right(right(snake_head)), data) and if_safe(right(snake_head), data):
            direction = 'right'
        else:
            if if_safe(up(snake_head), data):
                direction = 'up'
                print("Going UP2")
            elif if_safe(down(snake_head), data):
                direction = 'down'
                print("Going DOWN2")
            elif if_safe(left(snake_head), data):
                direction = 'left'
                print("Going LEFT2")
            else:
                direction = 'right'
                print("Going RIGHT2")

    return {
        'move': direction,
        'taunt': 'kent-snek2'
    }


def find_closest_food_index(snake_head, data):
    food_list = data.get('food')
    current_mindex = 0
    current_min_score = 999999
    count = 0
    for current_food in food_list:
        current_distance = [99,99]
        current_distance[0] = snake_head[0]-current_food[0]
        current_distance[1] = snake_head[1]-current_food[1]
        current_distance[0] = current_distance[0] * current_distance[0]
        current_distance[1] = current_distance[1] * current_distance[1]
        current_score = current_distance[0] + current_distance[1]
        if current_score < current_min_score:
            current_min_score = current_score
            current_mindex = count
        count += 1
    return current_mindex



def if_safe(new_snake_head,data):
    snakes = data.get('snakes')
    our_id = data.get('you')
    board_width = data.get('width')
    board_height = data.get('height')

    #print("Snakes List -> " +snakes.__str__())
    for snake in snakes:
        if new_snake_head in snake.get('coords'):
            return False
    #If new position is off the board
    if new_snake_head[1] < 0:
            return False
    if new_snake_head[1] > board_height-1:
        return False
    if new_snake_head[0] < 0:
        return False
    if new_snake_head[0] >board_width-1:
        return False
    return True


def up(old_snake_head):
    return [old_snake_head[0], old_snake_head[1]-1]


def down(old_snake_head):
    return [old_snake_head[0], old_snake_head[1]+1]


def left(old_snake_head):
    return [old_snake_head[0]-1, old_snake_head[1]]


def right(old_snake_head):
    return [old_snake_head[0]+1, old_snake_head[1]]

# def check_if_valid(snake_body,snake_head,intended_direction,board_width, board_height):
#     up_head = [snake_head[0], snake_head[1]-1]
#     down_head = [snake_head[0], snake_head[1]+1]
#     left_head = [snake_head[0]-1, snake_head[1]]
#     right_head = [snake_head[0]+1, snake_head[1]]
#     if intended_direction == 'up':
#         print ("Checking valid moving UP to -> " + up_head.__str__())
#         if up_head in snake_body:
#             print ("-COLLISION-")
#             return False
#         else:
#             if up_head[1] < 0:
#                     return False
#             return True
#     if intended_direction == 'down':
#         print ("Checking valid moving DOWN to -> " + down_head.__str__())
#         if down_head in snake_body:
#             print ("-COLLISION-")
#             return False
#         else:
#             if down_head[1] > board_height:
#                 print ("GOING TO GO OFF STAGE2")
#                 return False
#             return True
#     if intended_direction == 'left':
#         print ("Checking valid moving LEFT to -> " + left_head.__str__())
#         if left_head in snake_body:
#             print ("-COLLISION-")
#             return False
#         else:
#             if left_head[0] < 0:
#                 return False
#             return True
#     if intended_direction == 'right':
#         print ("Checking valid moving RIGHT to -> " + right_head.__str__())
#         if right_head in snake_body:
#             print ("-COLLISION-")
#             return False
#         else:
#             if right_head[0] > board_width:
#                 print ("GOING TO GO OFF STAGE1")
#                 return False
#             return True
#     else:
#         return False

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8000'))
