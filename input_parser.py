import re
import config
from tile import Tile


class TPInput:

    def __init__(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        self.lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))
        self.land_idx, self.tile_idx, self.target_idx, self.land_size = self.get_inds_and_size()
        self.COLORS = config.COLORS
        self.land_arr = self.read_landscape()
        self.tiles = self.read_tiles()
        self.targets = self.read_targets()

    def get_inds_and_size(self):
        """Reads the given txt and extracts the indexes of landscape, tiles, and targets from it. Landscape size is also
        got using this function."""
        land_idx, tile_idx, target_idx = 0, 0, 0

        tiles_found = False

        for i, x in enumerate(self.lines):
            if x.startswith('# Landscape'):
                land_idx = i + 1

            elif x.startswith('# Tiles:') and not tiles_found:
                tile_idx = i + 1
                tiles_found = True

            elif x.startswith('# Targets:'):
                target_idx = i + 1

        land_size = len(self.lines[land_idx]) // 2

        return land_idx, tile_idx, target_idx, land_size

    def read_landscape(self):
        """Reads the list of strings to generate a matrix of integers representing landscape."""
        land_int = [[0] * self.land_size for _ in range(self.land_size)]
        land_strs = self.lines[self.land_idx:self.land_idx+self.land_size]

        for i in range(self.land_size):
            cnt = 0
            for j in range(0, 2 * self.land_size, 2):
                if land_strs[i][j] != ' ':
                    land_int[i][cnt] = int(land_strs[i][j])
                cnt += 1

        return land_int

    def read_tiles(self):
        """Reads tiles into lists of landscape instance. Tiles are stored there as tile objects."""
        tile_objs = []
        tile_strs = self.lines[self.tile_idx]
        tile_strs = re.sub('[{}]', '', tile_strs)
        tile_strs = list(map(lambda t: t.strip(), tile_strs.split(',')))

        for t in tile_strs:
            k, v = t.split('=')
            tile_objs.append(Tile((k, int(v))))

        return tile_objs

    def read_targets(self):
        """Reads targets as a dictionary of colors."""
        tar = self.lines[self.target_idx:self.target_idx+self.COLORS]
        t_dict = {}
        for t in tar:
            k, v = t.split(':')
            t_dict[k] = int(v)

        return t_dict
