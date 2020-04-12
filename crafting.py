import copy, ast
from player import *
from assets import item_name_to_id, block_name_to_id

class Crafting:
    def __init__(self, empty):
        self.empty_crafting_grid = [[empty, empty, empty], #unused
                              [empty, empty, empty],
                              [empty, empty, empty]]
        self.crafting_grid = [[empty, empty, empty], #declare the crafting grid, which is empty
                              [empty, empty, empty],
                              [empty, empty, empty]]

        self.fuels = {3 : 150, 4 : 10, 6 : 25, 200 : 10, 206: 500}
        
        self.resultant = empty #the resultant from the crafting table
        self.recipes = compile_recipes()
        
        with open("crafting_recipes/furnace_recipes.txt") as recipes: #open crafting recipes from text file
            recipes = ast.literal_eval(recipes.read())
            self.furnace_recipes = recipes

    def check_recipes(self): #convert the grid into a list of ids instead of objects, then compare it to the list and return the id of the resultant and the amount.
        for recipe in self.recipes:
            converted_grid = [[0, 0, 0,],
                              [0, 0, 0,],
                              [0, 0, 0,]]
            for row in range(len(self.crafting_grid)):
                for column in range(len(self.crafting_grid[row])):
                    converted_grid[row][column] = self.crafting_grid[row][column].id
            
            if transform_recipe_grid(converted_grid) == transform_recipe_grid(recipe[0]): 
                # [id, amount]
                return [recipe[1], recipe[2]]
        return 0 #if the crafting table does not match any recipe, then return nothing.

    def clear_crafting_grid(self, empty): #unused
        self.crafting_grid = [[empty, empty, empty],
                              [empty, empty, empty],
                              [empty, empty, empty]]
def transform_recipe_grid(grid):
    top_left_r = 0
    top_left_c = 0
    for r in range(3):
        found = False
        for c in range(3):
            if (grid[r][c] != 0):
                top_left_r = r
                top_left_c = c
                found = True
                break
        if found:
            break
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for r in range(3):
        for c in range(3):
            new_r = r - top_left_r
            new_c = c - top_left_c
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                result[new_r][new_c] = grid[r][c]
    return result

def name_to_id(name):
    if name.isnumeric():
        return int(name)
    if name in block_name_to_id: # convert block/item name to id
        return block_name_to_id[name]
    if name in item_name_to_id:
        return item_name_to_id[name]
    print("No corresponding item id for: " + name)

def compile_recipes():
  result = []
  with open("crafting_recipes/recipes.txt", "r") as f:
    lines = f.read().split('\n')
    for line in lines:
      if len(line) < 12:
        continue
      line = line.split()
      #print(line)
      recipe = [[[], [], []]]
      for i in range(9):
        word = line[i]
        recipe[0][i//3].append(name_to_id(word))
      if (line[10].isnumeric()):
        recipe.append(name_to_id(line[11]))
        recipe.append(int(line[10]))
      else:
        recipe.append(name_to_id(line[10]))
        recipe.append(1)
      result.append(recipe)
  return result

