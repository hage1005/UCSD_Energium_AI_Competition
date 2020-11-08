from energium.game_constants import GAME_CONSTANTS, DIRECTIONS
ALL_DIRECTIONS = [DIRECTIONS.EAST, DIRECTIONS.NORTH, DIRECTIONS.WEST, DIRECTIONS.SOUTH]
from energium.kit import Agent
from energium.position import Position
from typing import List
import sys
import math
import random
import functools


# Create new agent
agent = Agent()

# initialize agent
agent.initialize()
#print("here")
# 
first_base = None
def p_1(a,b):
    print('a = {},{}, energium = {}, b = {},{}, energium = {}'.format(a.x, a.y, agent.map.get_tile_by_pos(a).energium, b.x, b.y, agent.map.get_tile_by_pos(b).energium), file = sys.stderr)
def p_2(msg, unit):
    print(msg, 'turn {} unit {} goal is {},{}, direction is {}'.format(unit.match_turn, unit.id,unit.goal.x,unit.goal.y,direction_to(unit,unit.goal)),file = sys.stderr)
def print_goal_list(goals):
     for goal in range(len(fixed_goal)):
        if(not fixed_goal[goal] is None):
            print('Turn {}, unit {}s goal is {},{}'.format(now_turn,goal, fixed_goal[goal].x, fixed_goal[goal].y), file = sys.stderr)

def unit_best_nearby_goal(my_unit):
    #print('unit {} at {},{} is calling best nearby goal'.format(my_unit.id, my_unit.pos.x, my_unit.pos.y), file = sys.stderr)
    global first_base
    first_base = my_unit
    list_raw = []
    radius = GAME_CONSTANTS["PARAMETERS"]["SEARCH_RADIUS"]
    leftX =  my_unit.pos.x - radius if (my_unit.pos.x - radius >= 0) else 0
    rightX=  my_unit.pos.x + radius + 1 if (my_unit.pos.x + radius < agent.mapWidth) else agent.mapWidth - 1
    leftY =  my_unit.pos.y - radius if (my_unit.pos.y - radius >= 0) else 0
    rightY=  my_unit.pos.y + radius + 1 if (my_unit.pos.y + radius < agent.mapWidth) else agent.mapWidth - 1
    for x in range(leftX, rightX):
            for y in range(leftX, rightY):
                #print('a = {},{}, energium = {}'.format(x, y, agent.map.get_tile_by_pos(Position(x,y)).energium), file = sys.stderr)
                if(not agent.map.get_tile(x,y).is_base() and not (x == my_unit.pos.x and y == my_unit.pos.y) and agent.map.get_tile(x,y).energium > 0):
                    list_raw.append(Position(x,y))
    priority_list = sorted(list_raw, key = functools.cmp_to_key(compare))
    for x in priority_list:
            if(goal_is_available(x,unit)):
                return x
    return None
            
def unit_best_goal(my_unit):
    #print('unit {} at {},{} is calling best goal'.format(my_unit.id, my_unit.pos.x, my_unit.pos.y), file = sys.stderr)
    global first_base
    first_base = my_unit
    list_raw = []
    for x in range(agent.mapWidth):
            for y in range(agent.mapHeight):
                #print('a = {},{}, energium = {}'.format(x, y, agent.map.get_tile_by_pos(Position(x,y)).energium), file = sys.stderr)
                if(not agent.map.get_tile(x,y).is_base() and not (x == my_unit.pos.x and y == my_unit.pos.y) and agent.map.get_tile(x,y).energium > 0):
                    list_raw.append(Position(x,y))
    priority_list = sorted(list_raw, key = functools.cmp_to_key(compare))
    for x in priority_list:
            if(goal_is_available(x,unit)):
                return x
    
def dead_end(pos, my_unit):
    checkDirections = [
            DIRECTIONS.NORTH,
            DIRECTIONS.EAST,
            DIRECTIONS.SOUTH,
            DIRECTIONS.WEST,
    ]
    for dir in checkDirections:    
        newPos = pos.translate(dir, 1)
        if newPos.x >= 0 and newPos.x < agent.mapWidth and newPos.y >= 0 and newPos.y < agent.mapHeight:
            if(not position_is_taken(newPos,my_unit) ):
                return False
    return True
    
def is_same_position(x1,y1):
    return x1.x == y1.x and x1.y == y1.y

def position_is_taken_simply(pos):
    for unit in agent.players[(agent.id + 1) % 2].units:
        if(pos == unit.pos):
            return True
    for unit in agent.players[agent.id].units:
        if(unit.pos.x == pos.x and unit.pos.y == pos.y):
            return True
    return False
    #see if a position is taken, but ignore enemy with lower breakdown level than my_unit
def position_is_taken(pos, my_unit):
    for unit in agent.players[(agent.id + 1) % 2].units:
        if(pos == unit.pos and unit.get_breakdown_level() < my_unit.get_breakdown_level()):
            return True
    for unit in agent.players[agent.id].units:
        if(unit.pos.x == pos.x and unit.pos.y == pos.y):
            return True
    return False
def goal_is_available(pos, my_unit):
    #occupied by enemy unit
    for unit in agent.players[(agent.id + 1) % 2].units:
        if(pos == unit.pos and unit.get_breakdown_level() < my_unit.get_breakdown_level()):
            return False
    # occupied by our unit
    for unit in agent.players[agent.id].units:
        if(my_unit.id != unit.id):
            if((fixed_goal[unit.id] and fixed_goal[unit.id] == pos) or unit.pos == pos):
                return False
    return True
def closest_base(unit):
    my_bases = agent.players[agent.id].bases
    result = my_bases[0]
    min_dist = GAME_CONSTANTS["PARAMETERS"]["MAX_DIST"]
    for base in my_bases:
        if base.pos.distance_to(unit.pos) < min_dist:
            min_dist = base.pos.distance_to(unit.pos)
            result = base
    #print('closest base fromm ({},{}) is ({},{})'.format(unit.pos.x,unit.pos.y,result.pos.x,result.pos.y), file = sys.stderr)
    return result
def is_being_hunted(unit):
    opponent = agent.players[(agent.id + 1) % 2]
    #print('opponent id is {}, our id is {}'.format((agent.id+1) %2, agent.id), file = sys.stderr)
    #for uni in opponent.units:
        #print("enemy unit ", uni.id," is at ",uni.pos.x, ", ",uni.pos.y, file = sys.stderr)
    for enemy in opponent.units:
        if enemy.pos.is_adjacent(unit.pos) and enemy.get_breakdown_level() < unit.get_breakdown_level():
            #print('enemy at {},{}| we at {},{}'.format(enemy.pos.x, enemy.pos.y, unit.pos.x, unit.pos.y),file = sys.stderr)
            return True
    return False
def direction_to(my_unit, targetPos):
        self = my_unit.pos
        """
        gives direction that moves closest to targetPos from this position or None if staying put is closer
        """
        checkDirections = [
            DIRECTIONS.NORTH,
            DIRECTIONS.EAST,
            DIRECTIONS.SOUTH,
            DIRECTIONS.WEST,
        ]
        if is_same_position(self, targetPos):
            return None
        closestDirection = None
        closestDist = GAME_CONSTANTS["PARAMETERS"]["MAX_DIST"]
        for dir in checkDirections:
            newPos = self.translate(dir, 1)
            if position_is_taken(newPos, my_unit) or dead_end(newPos, my_unit):
                continue
            dist = targetPos.distance_to(newPos)
            if newPos.x >= 0 and newPos.x < agent.mapWidth and newPos.y >= 0 and newPos.y < agent.mapHeight:
                if (dist < closestDist):
                    closestDist = dist
                    closestDirection = dir
        return closestDirection
    
def compare(a, b):
    #p_1(a,b)
    if(agent.map.get_tile_by_pos(a).energium == agent.map.get_tile_by_pos(b).energium):
        if (first_base.pos.distance_to(a) < first_base.pos.distance_to(b)):
            return -1
        else:
            return 1
    elif(agent.map.get_tile_by_pos(a).energium > agent.map.get_tile_by_pos(b).energium):
        return -1
    else:
        return 0

# Once initialized, we enter an infinite loop
first_time = True
now_turn = 0
fixed_goal = [None]*500
while(True):
    now_turn += 1
    # wait for update from match engine
    agent.update()

    # player is your player object, opponent is the opponent's
    player = agent.players[agent.id]
    opponent = agent.players[(agent.id + 1) % 2]

    # all your collectorunits
    my_units = player.units

    # all your bases
    my_bases = player.bases

    #my custom pq
    commands = []

    # use print("msg", file=sys.stderr) to print messages to the terminal or your error log.
    # normal prints are reserved for the match engine. Uncomment the lines below to log something
    # print('Turn {} | ID: {} - {} bases - {} units - energium {}'.format(agent.turn, player.team, len(my_bases), len(my_units), player.energium), file=sys.stderr)

    ### AI Code goes here ###

    # Let your creativity go wild. Feel free to change this however you want and
    # submit it as many times as you want to the servers
    # spawn unit until we have 4 units
    

    # iterate over all of our collectors and make them do something
    for unit in my_units:
        if(unit.get_breakdown_level() < 0.2):
            #print(unit.get_breakdown_level(), " enter f best goal", file = sys.stderr)
            fixed_goal[unit.id] = unit_best_goal(unit)
        elif unit.get_breakdown_level() >= GAME_CONSTANTS['PARAMETERS']['BREAKDOWN_MAX'] - 2:
            fixed_goal[unit.id] = closest_base(unit).pos
        elif(is_being_hunted(unit)):
            fixed_goal[unit.id] = unit_best_nearby_goal(unit)
        if(fixed_goal[unit.id] is None):
            fixed_goal[unit.id] = closest_base(unit).pos
        #print('turn {}, unit {}({},{}) goal is {},{}'.format(now_turn,unit.id,unit.pos.x,unit.pos.y,unit.goal.x,unit.goal.y),file = sys.stderr)
                    
        
        # otherwise lets try to collect our energium
        # choose a random direction to move in
        # food for thought - is this optimal to do?
        #randomDirection = ALL_DIRECTIONS[math.floor(random.random() * len(ALL_DIRECTIONS))]
        goodDirection = direction_to(unit,fixed_goal[unit.id])
      #print('try to move {}'.format(goodDirection),file = sys.stderr)
        # move in that direction if the tile the unit would move towards is not
        # negative in energium and is on the map
        if goodDirection:
            commands.append(unit.move(goodDirection))
            unit.pos = unit.pos.translate(goodDirection,1)
        else:
            pass
       ### AI Code ends here ###
    # submit commands to the engine
    if len(my_units) < agent.positive_cells*GAME_CONSTANTS["PARAMETERS"]["GOLDEN_RATIO"] and (len(my_units) < 1 or my_units[0].match_turn < 190) and player.energium >= GAME_CONSTANTS["PARAMETERS"]["UNIT_COST"] and (not position_is_taken_simply(my_bases[0].pos) ):
        commands.append(my_bases[0].spawn_unit())
    print(','.join(commands))

    # now we end our turn

    agent.end_turn()