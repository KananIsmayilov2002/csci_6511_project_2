from input_parser import TPInput
from landscape import Landscape
from backtracking import solve



if __name__ == "__main__":
    input_name = 'inputs/tilesproblem_1327003802793100.txt'
    tile_input = TPInput(input_name)
    landscape = Landscape(tile_input)
    print(landscape)
    print(landscape.targets)
    solve(landscape, 0, 0)
    print(landscape)
    print(landscape.count_colors(landscape.bushes))
    print(landscape.print_output())

