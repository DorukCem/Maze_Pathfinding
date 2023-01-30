from global_objects import*

class Manager:
    def __init__(self):
        self.algorithms = ["BFS", "DFS", "A*"]
        self.selected = 0
        

    def scroll(self, direction):
        if direction == "up":
            self.selected += 1
        else:
            self.selected -= 1    
        self.selected %= len(self.algorithms)

    
    def get_selected_algorithm(self):
        return self.algorithms[self.selected]
