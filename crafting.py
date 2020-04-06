import pygame, copy, ast
from player import *

class Crafting:
    def __init__(self, empty):
        self.empty_crafting_grid = [[empty, empty, empty],
                              [empty, empty, empty],
                              [empty, empty, empty]]
        self.crafting_grid = [[empty, empty, empty],
                              [empty, empty, empty],
                              [empty, empty, empty]]
        self.recipes = []
        self.resultant = empty
        with open("crafting_recipes/recipes.txt") as recipes:
            recipes = ast.literal_eval(recipes.read())
            self.recipes = recipes
    def check_recipes(self):
        for recipe in self.recipes:
            converted_grid = [[0, 0, 0,],
                              [0, 0, 0,],
                              [0, 0, 0,]]
            for row in range(len(self.crafting_grid)):
                for column in range(len(self.crafting_grid[row])):
                    converted_grid[row][column] = self.crafting_grid[row][column].id
            if converted_grid == recipe[0]:
                return [recipe[1], recipe[2]]
        return 0
    def clear_crafting_grid(self, empty):
        self.crafting_grid = [[empty, empty, empty],
                              [empty, empty, empty],
                              [empty, empty, empty]]
