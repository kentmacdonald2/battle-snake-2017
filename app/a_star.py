class node():
    def __init__(self, pos, parent=None, f=0, g=0, h=0):
        self.parent = parent
        self.pos = pos
        self.f = f
        self.g = g
        self.h = h

def up(old_snake_head):
    return [old_snake_head[0], old_snake_head[1] - 1]


def down(old_snake_head):
    return [old_snake_head[0], old_snake_head[1] + 1]


def left(old_snake_head):
    return [old_snake_head[0] - 1, old_snake_head[1]]


def right(old_snake_head):
    return [old_snake_head[0] + 1, old_snake_head[1]]


def reconstruct(successor):
    return None


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
    if new_snake_head[1] > board_height - 1:
        return False
    if new_snake_head[0] < 0:
        return False
    if new_snake_head[0] > board_width - 1:
        return False
    return True

def search(snake_head, data, goal):
    open_list = []
    closed_list = []

    snek = node(snake_head, f=0)


    #Add starting node to the open list
    open_list.append(snake_head)
    #Set score to zero


    while len(open_list) > 0:
        q = min(open_list, key= lambda n: n.f)
        open_list.remove(q)

        successors = []
        if if_safe(up(q.pos), data):
            q_up = node(up(q.pos), parent=q)
            successors.append(q_up)
        if if_safe(down(q.pos), data):
            q_down = node(down(q.pos), parent=q)
            successors.append(q_down)
        if if_safe(left(q.pos), data):
            q_left = node(left(q.pos), parent=q)
            successors.append(q_left)
        if if_safe(right(q.pos), data):
            q_right = node(right(q.pos), parent=q)
            successors.append(q_right)


        for succesor in successors:
            #TODO: Implement reconstruct
            if succesor.pos == goal:
                return reconstruct(succesor)
            succesor.g = q.g + 1
            straight_line_distance = ((succesor.pos[0] - goal[0])**2) + ((succesor.pos[1] - goal[1])**2)
            succesor.h = q.h + straight_line_distance
            succesor.f = succesor.g + succesor.h
            add = True
            for item in open_list:
                if item.pos == succesor.pos:
                    if item.f < succesor.f:
                        add = False
            for item in closed_list:
                if item.pos == succesor.pos:
                    if item.f < succesor.f:
                        add = False
            if add:
                open_list.append(succesor)
        closed_list.append(q)



