def solve(landscape, startX, startY):
    """Recursive backtracking algorithm to solve the problem."""

    if landscape.has_reached_target():
        return True

    for tile in landscape.tiles:
        if tile.count == 0:
            continue

        copied = landscape.create_copy()

        if landscape.can_put_tile(tile, startX, startY):
            tile.count -= 1
            landscape.bushes = landscape.put_tile(tile, startX, startY)
            landscape.current = landscape.count_colors(landscape.bushes)
            landscape.solution_map[f'X{startX}Y{startY}'] = tile.type

            prevstartY, prevstartX = startY, startX
            startX, startY = landscape.get_next_location(startX, startY)

            if solve(landscape, startX, startY):
                return True

            startX, startY = prevstartX, prevstartY
            landscape.bushes = copied
            landscape.current = landscape.count_colors(landscape.bushes)
            tile.count += 1

    return False