import ai_student
from connect4module import Connect4
import PygameConnect4
import pygame
import pygame_menu
import sys
import random
import math


pygame.init()
surface = pygame.display.set_mode((750, 400))
difficulty_time = 0.5
player = 1
slider = False
text1 = False
text2 = False
text3 = False
text4 = False
text5 = False

def set_difficulty(value, difficulty):
    global difficulty_time
    difficulty_time = difficulty

    if value == (('Trivial', 0.5), 0):
        global text1
        text1 = True
        global label1
        label1 = menu.add.label("Temps de calcul de l'IA par coup : 0.5s", font_size=15, font_color=(255,0,0))
        menu.move_widget_index(label1, index=2, render=True)

    if value == (('Piece of cake', 1), 1):
        global text2
        text2 = True
        global label2
        label2 = menu.add.label("Temps de calcul de l'IA par coup : 1s", font_size=15, font_color=(255,0,0))
        menu.move_widget_index(label2, index=2, render=True)

    if value == (('Pilou Pilou', 3), 2):
        global text3
        text3 = True
        global label3
        label3 = menu.add.label("Temps de calcul de l'IA par coup : 3s", font_size=15, font_color=(255,0,0))
        menu.move_widget_index(label3, index=2, render=True)

    if value == (('PILOU PILOU !', 10), 3):
        global text4
        text4 = True
        global label4
        label4 = menu.add.label("Temps de calcul de l'IA par coup : 10s", font_size=15, font_color=(255,0,0))
        menu.move_widget_index(label4, index=2, render=True)

    if value == (('Personnalisée', 420), 4):
        global slider
        slider = True
        global difficulty_value
        difficulty_value = menu.add.range_slider('Temps de calcul ?', 1, range_values=[0.1, 60], increment=0.1,
                                                 onchange=set_difficulty_slider)
        menu.move_widget_index(difficulty_value, index=2, render=True)

    if value == (('Partie de maîtres', 0.06969), 5):
        global text5
        text5 = True
        global label5
        global label6
        label5 = menu.add.label("Légendaire partie opposant Rotlewi et Rubinstein qui initièrent la théorie autour du puissance 4.", font_size=15, font_color=(255, 0, 0))
        menu.move_widget_index(label5, index=2, render=True)
        label6 = menu.add.label("Lodz, 1907 (colorised)",
                                font_size=15, font_color=(255, 0, 0))
        menu.move_widget_index(label6, index=3, render=True)

    if value != (('Personnalisée', 420), 4) and slider:
        menu.remove_widget(difficulty_value)
        slider = False

    if value != (('Trivial', 0.5), 0) and text1:
        menu.remove_widget(label1)
        text1 = False

    if value != (('Piece of cake', 1), 1) and text2:
        menu.remove_widget(label2)
        text2 = False

    if value != (('Pilou Pilou', 3), 2) and text3:
        menu.remove_widget(label3)
        text3 = False

    if value != (('PILOU PILOU !', 10), 3) and text4:
        menu.remove_widget(label4)
        text4 = False

    if value != (('Partie de maîtres', 0.06969), 5) and text5:
        menu.remove_widget(label5)
        menu.remove_widget(label6)
        text5 = False


def set_difficulty_slider(difficulty):
    global difficulty_time
    difficulty_time = difficulty


def start_the_game():
    SQUARESIZE = 100
    WIDTH = Connect4.NUM_COLS * SQUARESIZE + 50
    HEIGHT = (1 + Connect4.NUM_ROWS) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)
    RADIUS = int(SQUARESIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(SIZE)
    print(difficulty_time)
    PygameConnect4.main(difficulty_time, player)



def player(value, joueur):
    global player
    player = joueur



def frame():
    surface = pygame.display.set_mode((750, 400))
    menu.clear(True)
    menu.add.text_input('Name : ', default='Gazou')
    menu.add.selector('Difficulty :',
                      [('Trivial', 0.5), ('Piece of cake', 1), ('Pilou Pilou', 3), ('PILOU PILOU !', 10),
                       ('Personnalisée', 420), ('Partie de maîtres', 0.06969)], onchange=set_difficulty)
    menu.add.selector('Joueur :',
                      [('1', 1), ('2', 2), ('Aléatoire', 0)], onchange=player)
    play = menu.add.button('Play', start_the_game)
    quit = menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)


menu = pygame_menu.Menu('Xx_Connect4_Terminator_xX', 750, 400, theme=pygame_menu.themes.THEME_ORANGE)

if __name__ == "__main__":
    frame()
