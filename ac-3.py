from landscape import Landscape
from input_parser import TPInput


tile_input = TPInput('inputs/tilesproblem_1327003787335100.txt')
landscape = Landscape(tile_input)

variables = landscape.get_variables()
domains = [landscape.tiles for _ in variables]

def tile_count(subland1, subland2, tile1, tile2):
    """Checks whether there is enough tile to use for the current operation"""
    if tile1.count - 1 < 0 or tile2.count - 1 < 0:
        return False
    else:
        return False

def bush_count(subland1, subland2, tile1, tile2):
    """Checks whther the tiles can be put to the landscape at the same time vithout violating the final color
    limitation"""
    return landscape.can_put_tile(tile1, variables[subland1]) and landscape.can_put_tile(tile2, variables[subland2])

# List of constraints
constraints = [tile_count, bush_count]

# List of arcs can be all neighbouring 4x4 subspaces which the landscape is divided into. Subspaces are numbered from 0 to 
# (landscape_size^2 / tile_size^2) moving in direction of from up to bottom and from left to right. 

# arcs = [(0, 1), (1, 5), (1, 2), (1, 6) ...]

def revise(subland1, subland2):
    """Make variable `subland1` arc consistent with variable `subland2`. Sublandscape is a 4x4 sized divisions of
    the landscape"""
    revised = False

    # Get x and y domains
    x_domain = domains[subland1]
    y_domain = domains[subland2]

    for x_tile in x_domain:
        satisfies = False
        for y_tile in y_domain:
            for constraint in constraints:
                if constraint(x_tile, y_tile):
                    satisfies = True
                else:
                    satisfies = False

        if not satisfies:
            x_domain.remove(x_tile)
            revised = True

    return revised


def ac3(arcs):
    """Update `domains` such that each variable is arc consistent."""
    # Add all the arcs to a queue.
    queue = arcs[:]

    while queue:
        # Take the first arc off the queue (dequeue)
        (x, y) = queue.pop(0)

        # Make x arc consistent with y
        revised = revise(x, y)

        if revised:
            # Add all arcs of the form (k, x) to the queue (enqueue)
            neighbors = [neighbor for neighbor in arcs if neighbor[1] == x]
            queue = queue + neighbors
