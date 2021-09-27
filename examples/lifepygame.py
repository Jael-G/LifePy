import pygame
from lifepy import lifepy
from pygame import event
'''
Using Pygame to show a lifepy simulation
'''

DISPLAY_H =500
DISPLAY_W = 500
CELL_SPACE = 10
'''
Note:
The width and height are the size of the window, and the cell space is the amount of pixels from said window that EACH cell will take.
Therefore, cell space must be a divisor of both width and height. 

Furthermore, reducing the cell space on the same width and height means that more cells will appear in the same
width and height. 

Example:

if height and with are 100 and cell space is 10, the array will be (100/10 * 100/10) = 10*10, but if the cell space is 1, then the array will
be 100*100, without having to increase screen size.
'''
DEAD_COLOR = (0, 0, 0)
LIVE_COLOR = (200, 200, 200)
SIMULATION = lifepy.Simulator(m_size=int(DISPLAY_W/CELL_SPACE), n_size=int(DISPLAY_H/CELL_SPACE), mode='ASCII')

def main():

    if DISPLAY_W%CELL_SPACE!=0 or DISPLAY_H%CELL_SPACE!=0:
        print("The cell space must be a divisor of the width and height of the screen size.")
        quit()
        
    global DISPLAY, SIMULATION
    SIMULATION.generate_array()

    pygame.init()
    DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

    while True:
        generate_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()


def generate_grid():
    global SIMULATION
    contine_running = SIMULATION.step()
    if not contine_running:
        input("Press enter to exit")
        pygame.quit()
        quit()
    

    for i in range(0, DISPLAY_W, CELL_SPACE):
        for j in range(0, DISPLAY_H, CELL_SPACE):
            cell = pygame.Rect(i, j, CELL_SPACE, CELL_SPACE)
            if SIMULATION.get_array()[int(i/CELL_SPACE)][int(j/CELL_SPACE)]:
                pygame.draw.rect(DISPLAY, LIVE_COLOR, cell, 0)
            else:
                pygame.draw.rect(DISPLAY, DEAD_COLOR, cell, 0)


main()