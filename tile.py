import config


class Tile:
    def __init__(self, tile):
        self.type = tile[0]
        self.count = tile[1]

    def full(self, landscape, startX, startY):
        """Puts full shaped tile to the landscape and returns the copy of updated version"""
        cp = landscape.bushes.copy()
        for i in range(startX, startX + config.TILE_SIZE):
            for j in range(startY, startY + config.TILE_SIZE):
                cp[i][j] = 0
        return cp

    def out(self, landscape, startX, startY):
        """Puts outer shaped tile to the landscape and returns the copy of updated version"""
        cp = landscape.bushes.copy()
        for i in range(startX, startX + config.TILE_SIZE):
            for j in range(startY, startY + config.TILE_SIZE):
                if (i == startX) or (i == startX + config.TILE_SIZE - 1) or (j == startY) or (j == startY + config.TILE_SIZE - 1):
                    cp[i][j] = 0
        return cp

    def el(self, landscape, startX, startY):
        """Puts el shaped tile to the landscape and returns the copy of updated version"""
        cp = landscape.bushes.copy()
        for i in range(startX, startX + config.TILE_SIZE):
            for j in range(startY, startY + config.TILE_SIZE):
                if (i == startX) or (j == startY):
                    cp[i][j] = 0
        return cp

    def __str__(self) -> str:
        return f'Tile: {self.type}. Count: {self.count}.'
