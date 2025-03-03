import config
import numpy as np


def count_non_zeros(landscape, startX, startY):
    """Counts non zero elements within the given area."""
    non_zero_colors = 0

    for i in range(startX, startX + config.TILE_SIZE):
        for j in range(startY, startX + config.TILE_SIZE):
            if landscape[i][j] != 0:
                non_zero_colors += 1

    return non_zero_colors


class Landscape:
    def __init__(self, tile_input):
        self.bushes = tile_input.land_arr
        self.tiles = tile_input.tiles
        self.targets = tile_input.targets
        self.land_size = tile_input.land_size
        self.current = self.count_colors(self.bushes)
        self.states = [self.bushes]
        self.solution_map = {}

    def put_tile(self, tile, startX, startY):
        """Puts the given tile to the given coordinate and returns the copy of the landscape"""

        if tile.type == 'OUTER_BOUNDARY':
            return tile.out(self, startX, startY)
        elif tile.type == 'EL_SHAPE':
            return tile.el(self, startX, startY)
        elif tile.type == 'FULL_BLOCK':
            return tile.full(self, startX, startY)

    def get_variable_lands(self):
        """Function to get the small sublandscapes size of 4x4"""
        new_l = []
        divider = self.land_size // config.TILE_SIZE
        arr = np.array(self.bushes)
        ver_split = np.array_split(arr, divider, axis=0)

        for a in ver_split:
            hor_split = np.array_split(a, divider, axis=1)
            hor_split = list(map(lambda x: x.tolist(), hor_split))
            new_l += hor_split

        return new_l

    def get_variables(self):
        """Gets the coordinates of 4x4 divided sublandscapes."""
        divider = self.land_size // config.TILE_SIZE
        startX, startY = 0, 0
        variables = [(startX, startY)]
        for i in range(divider ** 2):
            variables.append((startX, startY))
            startX, startY = self.get_next_location(startX, startY)

        return variables

    def count_colors(self, landscape=None):
        """Counts the color of given landscpae. If no landscape is given counts the colors of current attribute of
        the class instance"""

        color_dict = {'1': 0, '2': 0, '3': 0, '4': 0}

        if landscape is None:
            landscape = self.bushes

        for i in range(self.land_size):
            for j in range(self.land_size):
                if landscape[i][j] != 0:
                    color_dict[str(landscape[i][j])] += 1

        return color_dict

    def check_distance(self, colors):
        """Checks color distance between given colors and target"""
        diff_dict = {'1': 0, '2': 0, '3': 0, '4': 0}

        for key, val in self.targets.items():
            diff_dict[key] = colors[key] - val

        return diff_dict

    def has_reached_target(self):
        """Checks whether the current state of the landscape instance has reached the target."""
        if all(self.current[key] == self.targets[key] for key, val in self.current.items()):
            return True
        else:
            return False

    def create_copy(self):
        """Creates copy of the given list of lists."""
        cp = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            for j in range(self.land_size):
                cp[i][j] = self.bushes[i][j]

        return cp

    def can_put_tile(self, tile, startX, startY):
        """Considering the color constraints, checks whether given tile can be put on the given coordinates."""

        possible = self.put_tile(tile, startX, startY)
        colors = self.count_colors(possible)

        for key, _ in colors.items():
            if colors[key] < self.targets[key]:
                return False

        return True

    def get_next_location(self, startX, startY):
        """Considering the land size, calculates the next location to put the tile by incrementing the previous
        coordinates with tile size
        """
        if startX + config.TILE_SIZE < self.land_size:
            startX += config.TILE_SIZE
        else:
            startX = 0

            if startY + config.TILE_SIZE < self.land_size:
                startY += config.TILE_SIZE
        return startX, startY

    def print_output(self):
        """Prints the solution map as the output"""
        res = '# Tiles:\n'
        for i, (key, val) in enumerate(self.solution_map.items()):
            res += f'{i} {config.TILE_SIZE} {val}\n'
        return res

    def __str__(self) -> str:
        """Str function to print the landscape instance in readable format"""
        res = "\n_______________________________________\n"
        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.bushes[i][j] > 0:
                    res += str(self.bushes[i][j]) + config.CELL_SEPARATOR
                else:
                    res += ' ' + config.CELL_SEPARATOR
            res += config.LINE_SEPARATOR
        res += "_______________________________________"
        return res
