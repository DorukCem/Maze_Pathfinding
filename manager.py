from global_objects import*
from breadth_first_search import BFS
from depth_first_search import DFS
from a_star import A_star

class Manager:
    def __init__(self):
        self.algorithms = [BFS(), DFS(), A_star()]
        self.selected = 0
        

    def scroll(self, direction):
        if direction == "up":
            self.selected += 1
        else:
            self.selected -= 1    
        self.selected %= len(self.algorithms)

    
    def get_selected_algorithm(self):
        return self.algorithms[self.selected].name
    
    def run_algorithm(self, grid):
        self.algorithms[self.selected].run(grid)
