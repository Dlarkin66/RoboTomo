import pygame
from player_1 import Player_1
from player_2 import Player_2

class GameState():
    def __init__(self):
        self.state = "intro"
        
    def intro(self):
        #Draw background and text
        draw_bg()
        draw_intro_img()


        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "main_game"


        #update display
        pygame.display.update()

    def main_game(self):
        global intro_count
        global last_count_update
        global game_over
        global game_over_cd
        global run
        global game_over_time


        #Draw background, health/stamina bars, and players
        draw_bg()

        draw_health_bar(player_1.health, 20, 20)
        draw_health_bar(player_2.health, 580, 20)

        draw_stamina_bar(player_1.stamina, 17, 60)
        draw_stamina_bar(player_2.stamina, 681, 60)

        player_1.draw(screen)
        player_2.draw(screen)


        #Update fighter animations
        player_1.update()
        player_2.update()


        #Prevent  player pass through
        player_1.pass_through(player_2)
        player_2.pass_through(player_1)


        #Update countdown
        if intro_count <= 0:
            #Allow player movement after round starts
            player_1.move(screen, player_2)
            player_2.move(screen, player_1)
        else:
            draw_text(str(intro_count), font, white, screen_width / 2, screen_height / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

            player_2.rect.bottom = 470  #keep players at correct height while counting down.


        #Check for a game over
        if game_over == False:
            if player_1.alive == False:
                game_over = True
                game_over_time = pygame.time.get_ticks()
            elif player_2.alive == False:
                game_over = True
                game_over_time = pygame.time.get_ticks()
        else:
            if game_over == True and player_1.alive == True: 
                draw_p1_win_img()
            elif game_over == True and player_2.alive == True:
                draw_p2_win_img()
            if pygame.time.get_ticks() - game_over_time > game_over_cd:
                self.state = "continue_screen"


        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        #update display
        pygame.display.update()

    def continue_screen(self):
        global game_over
        global intro_count


        #Call background and text functions
        draw_bg()
        draw_continue_screen()


        #Scale and assign rects to yes and no text
        scaled_yes = pygame.transform.scale(yes_txt, (screen_width / 8, screen_height / 10))
        scaled_no = pygame.transform.scale(no_txt, (screen_width / 8.5, screen_height / 10.5))
        y = screen.blit(scaled_yes, (200, 300))
        n = screen.blit(scaled_no, (650, 300))


        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if y.collidepoint(pos):
                    player_1.health = 100
                    player_1.alive = True
                    player_1.rect.left = 100
                    player_2.health = 100
                    player_2.alive = True
                    player_2.rect.right = 900
                    game_over = False
                    intro_count = 4
                    self.state = "main_game"
                elif n.collidepoint(pos):
                    pygame.quit()
                    exit()
        
        
        #update display
        pygame.display.update()

    def state_manager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "main_game":
            self.main_game()
        if self.state == "continue_screen":
            self.continue_screen()


#General setup
pygame.init()
clock = pygame.time.Clock()
fps = 60


#Game window
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Robo-Tomo Fight!")


#Game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
game_over = False
game_over_cd = 2000


#Define colors used for health, stamina, etc
white = (255, 255, 255)
red = (255, 0 , 0)
yellow = (255, 255, 0)
purple = (93, 63, 211)
green = (0, 255, 0)
black = (0, 0 ,0)


#Make gamestate callable
game_state = GameState()


#Load fonts
font = pygame.font.Font("Font/DePixelBreit.ttf",50)


#Load images
bg_img = pygame.image.load("graphics/Sky.png").convert_alpha()

player_1_sheet = pygame.image.load("graphics/player/playerspritesheet.png").convert_alpha()
player_2_sheet = pygame.image.load("graphics/Tomato/Fbspritesheet.png").convert_alpha()

p1_win = pygame.image.load("graphics/Text/P1wins.png").convert_alpha()
p2_win = pygame.image.load("graphics/Text/P2wins.png").convert_alpha()

no_txt = pygame.image.load("graphics/Text/No.png").convert_alpha()
yes_txt = pygame.image.load("graphics/Text/Yes.png").convert_alpha()
intro_txt = pygame.image.load("graphics/Text/Introscreentext.png").convert_alpha()
continue_txt = pygame.image.load("graphics/Text/Continue.png").convert_alpha()


#Functions for drawing and resizing images
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_img, (screen_width, screen_height))
    screen.blit(scaled_bg, (0,0))

def draw_p1_win_img():
    scaled_p1_win_img = pygame.transform.scale(p1_win, (screen_width / 3.5, screen_height / 8))
    screen.blit(scaled_p1_win_img, (360, 150))

def draw_p2_win_img():
    scaled_p2_win_img = pygame.transform.scale(p2_win, (screen_width / 3.5, screen_height / 8))
    screen.blit(scaled_p2_win_img, (360, 150))

def draw_intro_img():
    scaled_intro = pygame.transform.scale(intro_txt, (screen_width / 2, screen_height / 8))
    screen.blit(scaled_intro, (250, 150))

def draw_continue_screen():
    scaled_continue = pygame.transform.scale(continue_txt, (screen_width / 2, screen_height / 8))
    screen.blit(scaled_continue, (250, 150))


#Functions for drawing health and stamina bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, black, (x -5, y -5, 410, 40))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, purple, (x, y, 400 * ratio, 30))

def draw_stamina_bar(stamina, x, y):
    ratio = stamina / 100
    pygame.draw.rect(screen, black, (x - 2, y -2.2, 305, 15))
    pygame.draw.rect(screen, red, (x, y, 300, 10))
    pygame.draw.rect(screen, green, (x, y, 300 * ratio, 10))


#Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Define player variables
player_1_size = 230
player_2_size = 250
player_animations_frames = [2, 2, 2, 1, 2]


#Define each player
player_1 = Player_1(100, 290, player_1_size, player_1_sheet, player_animations_frames)
player_2 = Player_2(800, 290, player_2_size, player_2_sheet, player_animations_frames)


#Play music and sound effects
bg_music = pygame.mixer.Sound("Music/main_game_music.wav")
bg_music.set_volume(0.2)
bg_music.play(loops = -1)


#game loop
run = True
while run:

    game_state.state_manager()
    clock.tick(fps)


#exit pygame
pygame.quit