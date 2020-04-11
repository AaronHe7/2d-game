import pygame, copy, ast
from player import *

class Crafting:
    def __init__(self, empty):
        self.empty_crafting_grid = [[empty, empty, empty], #unused
                              [empty, empty, empty],
                              [empty, empty, empty]]
        self.crafting_grid = [[empty, empty, empty], #declare the crafting grid, which is empty
                              [empty, empty, empty],
                              [empty, empty, empty]]
        self.furnace_grid = [empty, empty]
        self.recipes = []
        self.furnace_recipes = []
        self.furnace_progress = 0
        self.furnace_fuel = 0
        self.fuels = {3 : 10, 4 : 2, 6 : 5, 200 : 2}
        self.furnace_currently_cooking = empty
        
        self.resultant = empty #the resultant from the crafting table
        self.furnace_resultant = empty #the resultant from the furnace
        with open("crafting_recipes/crafting_recipes.txt") as recipes: #open crafting recipes from text file
            recipes = ast.literal_eval(recipes.read())
            self.recipes = recipes
        with open("crafting_recipes/furnace_recipes.txt") as recipes:
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
            if converted_grid == recipe[0]: 
                # [id, amount]
                return [recipe[1], recipe[2]]
        return 0 #if the crafting table does not match any recipe, then return nothing.
    def check_furnace_recipes(self):
        for recipe in self.furnace_recipes:
            converted_grid = [0, 0]
            for i in range(len(converted_grid)):
                converted_grid[i] = self.furnace_grid[i].id
            if converted_grid[0] == recipe[0]:
                #id,amount
                return recipe[1]
        if self.furnace_grid[0].id != 0:
            return 204
        else:
            return 0
    def clear_crafting_grid(self, empty): #unused
        self.crafting_grid = [[empty, empty, empty],
                              [empty, empty, empty],
                              [empty, empty, empty]]
