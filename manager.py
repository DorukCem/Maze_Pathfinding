from global_objects import*
from breadth_first_search import BFS
from depth_first_search import DFS

class Manager:
    def __init__(self):
        self.algorithms = [BFS(), DFS()]
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
