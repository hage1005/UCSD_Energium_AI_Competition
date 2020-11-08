from energium.game_constants import GAME_CONSTANTS, DIRECTIONS
ALL_DIRECTIONS = [DIRECTIONS.EAST, DIRECTIONS.NORTH, DIRECTIONS.WEST, DIRECTIONS.SOUTH]
from energium.kit import Agent
import sys
import math
import random

# Create new agent
agent = Agent()

# initialize agent
agent.initialize()

# Once initialized, we enter an infinite loop
while True:

    # wait for update from match engine
    agent.update()

    commands = []

    # player is your player object, opponent is the opponent's
    player = agent.players[agent.id]
    opponent = agent.players[(agent.id + 1) % 2]

    # all your collectorunits
    my_units = player.units

    # all your bases
    my_bases = player.bases

    # use print("msg", file=sys.stderr) to print messages to the terminal or your error log.
    # normal prints are reserved for the match engine. Uncomment the lines below to log something
    # print('Turn {} | ID: {} - {} bases - {} units - energium {}'.format(agent.turn, player.team, len(my_bases), len(my_units), player.energium), file=sys.stderr)

    ### AI Code goes here ###

    # Let your creativity go wild. Feel free to change this however you want and
    # submit it as many times as you want to the servers

    # spawn unit until we have 4 units
    if len(my_units) < 4 and player.energium >= GAME_CONSTANTS["PARAMETERS"]["UNIT_COST"]:
        commands.append(my_bases[0].spawn_unit())
    
    # iterate over all of our collectors and make them do something
    for unit in my_units:
      # first we check the breakdown level, if unit is about to break down, lets make
      # it move towards a random friendly base
        if(opponent.units[0].get_breakdown_level() > unit.get_breakdown_level()):
            directionToHunt = unit.pos.direction_to(opponent.units[0].pos)
            commands.append(unit.move(directionToHunt))
        else:
    # otherwise lets try to collect our energium
    # choose a random direction to move in
    # food for thought - is this optimal to do?
            pass

    ### AI Code ends here ###

    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()