import Xx_Connect4_Terminator_xX
import ai_student
from connect4module import Connect4
import pygame
import pygame_menu
import sys
import random
import math
import time

rand = random.Random()


class Connect4_GUI(Connect4):
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (0, 0, 128)
    BLACK = (0, 0, 0)
    GREY = (69, 69, 69)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    SQUARESIZE = 100
    WIDTH = Connect4.NUM_COLS * SQUARESIZE + 50
    HEIGHT = (1 + Connect4.NUM_ROWS) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)
    RADIUS = int(SQUARESIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(SIZE)

    def draw_board(self):
        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                loc_size = (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                pygame.draw.rect(self.SCREEN, self.BLUE, loc_size)
                loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                pygame.draw.circle(self.SCREEN, self.BLACK, loc, self.RADIUS)

        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                if self.board[r][c] == 1:
                    loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.RED, loc, self.RADIUS)
                elif self.board[r][c] == -1:
                    loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.YELLOW, loc, self.RADIUS)
        pygame.display.update()

    def run_game(self, difficulty, joueur):
        score = 0
        pygame.init()
        myfont = pygame.font.SysFont("impact", 75)
        texte = pygame.font.SysFont("impact", 17)
        texte_temps = pygame.font.SysFont("impact", 25)
        self.draw_board()
        pygame.display.update()

        moves = self.get_avail_moves()
        player = 1  # first player is always 1
        human_player = 1
        if joueur == 1:
            human_player = 1
        if joueur == 2:
            human_player = -1
        if joueur == 0:
            human_player = rand.choice([1, -1])
        if difficulty == 0.06969:
            human_player = -1
        winner = False
        exit_flag = False
        while moves != [] and winner == False and exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.WIDTH, self.SQUARESIZE))
                    label = texte_temps.render(str(difficulty) + "s", 1, self.GREY)
                    self.SCREEN.blit(label, (self.WIDTH - 50, 10))
                    posx = event.pos[0]
                    if player == 1 and posx < self.WIDTH - 50:
                        pygame.draw.circle(self.SCREEN, self.RED, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
                    if player == -1:
                        pygame.draw.circle(self.SCREEN, self.YELLOW, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)

                    pygame.display.update()

                # wait for player input
                if player == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.WIDTH, self.SQUARESIZE))
                    label = texte_temps.render(str(difficulty) + "s", 1, self.GREY)
                    self.SCREEN.blit(label, (self.WIDTH - 50, 10))
                    posx = event.pos[0]
                    move = int(math.floor(posx / self.SQUARESIZE))
                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if self.get_winner():
                            if human_player == 1:
                                label = myfont.render("Human wins !!!", 1, self.RED)
                                resultat = 1
                            else:
                                label = myfont.render("Human wins !!!", 1, self.YELLOW)
                                resultat = 1
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player

                # Ask for Player 2 Input
                elif player == -human_player:
                    move, score_temp, nombre_simulation = ai_student.ai_student(self.board, 2, difficulty)
                    if score_temp != None:
                        score = score_temp
                    #print(self.board)
                    if difficulty == 0.06969:
                        self.board = [[0., 0., -1., -1., 0., 0., 0.],
                                     [0., -1., 1., -1., 1., -1., 0.],
                                     [0., -1., -1., -1., -1., -1., 0.],
                                     [-1., 1., 1., 1., 1., 1., -1.],
                                     [0., -1., 1., 1., 1., -1., 0.],
                                     [0., 0., -1., -1., -1., 0., 0.]]
                        move = 5

                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if human_player == 1:
                            color1 = self.YELLOW
                            color2 = self.RED
                        else:
                            color1 = self.RED
                            color2 = self.YELLOW
                        pygame.draw.rect(self.SCREEN, color1, (self.WIDTH - 50, self.SQUARESIZE, 50, self.HEIGHT))
                        pygame.display.update()
                        Bar = (1 - (score / 100)) * ((self.HEIGHT - self.SQUARESIZE) / 2)
                        pygame.draw.rect(self.SCREEN, color2, (self.WIDTH - 50, self.SQUARESIZE, 50, Bar))
                        label = texte.render(str(-(round(score, 2))), 1, self.GREY)
                        self.SCREEN.blit(label, (self.WIDTH - 47, Bar + self.SQUARESIZE - 23))
                        pygame.display.update()
                        if self.get_winner():
                            if player == 1:
                                label = myfont.render("Human loses !", 1, self.RED)
                                resultat = 0
                            else:
                                label = myfont.render("Human loses !", 1, self.YELLOW)
                                resultat = 0
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player
            moves = self.get_avail_moves()
        if winner == False and moves == []:
            label = myfont.render("It's a Draw :/", 1, self.LIGHT_BLUE)
            resultat = 0
            self.SCREEN.blit(label, (40, 10))
            self.draw_board()
        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
            time.sleep(5)
            popup = pygame.display.set_mode((500, 300))
            menu = pygame_menu.Menu('Partie terminée', 500, 300, theme=pygame_menu.themes.THEME_DARK)
            if resultat == 0:
                menu.add.button('Réessayer', retry)
            if resultat == 1:
                menu.add.button('Rejouer', retry)
            menu.add.button('Menu', Xx_Connect4_Terminator_xX.frame)
            menu.add.button('Quitter', pygame_menu.events.EXIT)
            menu.mainloop(popup)
        pygame.quit()


def retry():
    SQUARESIZE = 100
    WIDTH = Connect4.NUM_COLS * SQUARESIZE + 50
    HEIGHT = (1 + Connect4.NUM_ROWS) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)
    RADIUS = int(SQUARESIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(SIZE)
    main(diff, plr)


def main(difficulty, player):
    global diff
    diff = difficulty
    global plr
    plr = player
    my_game = Connect4_GUI()
    my_game.run_game(difficulty, player)


if __name__ == "__main__":
    main()
