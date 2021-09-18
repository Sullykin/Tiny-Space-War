import pygame
import sys
import os

class Game:
    def __init__(self):
        self.setup_pygame()

    def main_loop(self):
	self.handle_input()
	self.process_logic()
	self.render_frame()

    def handle_input(self):
        self.get_input_states()
        

class Enemy:
    def __init__(self):
        pass

    def update(self, game)
