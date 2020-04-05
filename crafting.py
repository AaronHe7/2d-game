import pygame, copy, ast

class Crafting:
    def __init__(self):
        self.crafting_grid = {}
        self.recipes = []
        with open("crafting_recipes/recipes.txt") as recipes:
            recipes = ast.literal_eval(recipes.read())
            self.recipes = recipes
