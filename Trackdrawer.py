## Written by chatgpt

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 720, 540
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Line Drawer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Line storage
lines = []
current_line = []

def draw_lines():
    for line in lines:
        pygame.draw.line(window, BLACK, line[0], line[1], 2)
    if len(current_line) > 1:
        for i in range(len(current_line) - 1):
            pygame.draw.line(window, RED, current_line[i], current_line[i + 1], 2)

def save_lines():
    with open('C:/Users/louis/OneDrive/Documents/_uni/MDN/RL Project/lines.txt', 'a') as f:
        for line in lines:
            f.write(f"self.walls.append(Wall(({line[0][0]},{line[0][1]}),({line[1][0]},{line[1][1]}),self.agent))\n")

# Main loop
running = True
while running:
    window.fill(WHITE)
    draw_lines()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_lines()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if current_line:
                    lines.append((current_line[-1], event.pos))
                current_line.append(event.pos)
            elif event.button == 3:  # Right click
                current_line = []
    
    if len(current_line) > 0:
        pos = pygame.mouse.get_pos()
        pygame.draw.line(window, RED, current_line[-1], pos, 2)
    
    pygame.display.flip()
