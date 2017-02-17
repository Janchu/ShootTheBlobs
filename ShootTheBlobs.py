import pygame
import random
import sys
import math
from pygame.locals import *

'''
Classes
'''


class Map:
    def __init__(self):
        self.tiles = [[0 for y in range(60)] for x in range(90)]

    def randomize(self):
        for x in range(90):
            for y in range(60):
                # Create borders for the map
                if x == 0 or y == 0 or x == 89 or y == 59:
                    self.tiles[x][y] = 1
                # Make 11x11 area in the center empty
                elif 40 <= x <= 50 and 25 <= y <= 35:
                    self.tiles[x][y] = 0
                # Randomize the rest of the map
                else:
                    rand = random.randint(0, 20)
                    if rand == 1:
                        self.tiles[x][y] = 1
                    else:
                        self.tiles[x][y] = 0

                # Create the "base" in the middle of the map
                if x == 41 and 26 <= y <= 28 or x == 41 and 32 <= y <= 34:
                    self.tiles[x][y] = 1
                if x == 42 and y == 26 or x == 42 and y == 34:
                    self.tiles[x][y] = 1
                if x == 43 and y == 26 or x == 43 and y == 34:
                    self.tiles[x][y] = 1
                if x == 47 and y == 26 or x == 47 and y == 34:
                    self.tiles[x][y] = 1
                if x == 48 and y == 26 or x == 48 and y == 34:
                    self.tiles[x][y] = 1
                if x == 49 and 26 <= y <= 28 or x == 49 and 32 <= y <= 34:
                    self.tiles[x][y] = 1

    def draw(self, camera_pos_x, camera_pos_y):
        # Changing tile_size value here changes how big tiles are drawn on the map
        tile_size = 20
        for x in range(90):
            for y in range(60):
                if self.tiles[x][y] == 1:
                    pygame.draw.rect(screen, grey,
                                     ((x * tile_size - camera_pos_x - 10), (y * tile_size - camera_pos_y - 10),
                                      tile_size, tile_size))


class Player:
    def __init__(self):
        # Give the player default location in the center of the map
        self.player_coordinate_x = 45
        self.player_coordinate_y = 30
        self.player_width = 20
        self.player_height = 20
        self.center_camera_x = 450
        self.center_camera_y = 300

    def draw_player(self):
        pygame.draw.rect(screen, black,
                         (self.center_camera_x, self.center_camera_y, self.player_width, self.player_height))


class Bullet:
    def __init__(self):
        # Default values for bullets and its projectile
        self.bullet_color = red
        self.orientation = ""
        self.direction = ""
        self.bullet_location_adjusted = False
        self.bullet_exists = True
        self.bullet_pos_x = 0
        self.bullet_pos_y = 0
        self.bullet_width = 0
        self.bullet_height = 0
        self.bullet_velocity = 2

    def draw_bullet(self):

        global score
        global monster_list
        global monsters_dead

        # Check if bullet is going to go horizontally and then adjust its drawing shape accordingly:
        if self.orientation == "horizontal":
            self.bullet_width = 10
            self.bullet_height = 4

            # If bullet is shot towards left:
            if self.direction == "left":
                # Here we adjust the starting location for the bullet:
                if not self.bullet_location_adjusted:
                    self.bullet_pos_x -= 10
                    self.bullet_pos_y -= 2
                    self.bullet_location_adjusted = True
                tile_coord_x = int((((self.bullet_pos_x + 460) - ((self.bullet_pos_x + 460) % 20)) / 20) + 1)
                tile_coord_y = int((((self.bullet_pos_y + 320) - ((self.bullet_pos_y + 320) % 20)) / 20))
                if game_map.tiles[tile_coord_x][tile_coord_y] == 0:
                    # Drawing the actual bullet and set its direction of velocity to left:
                    pygame.draw.rect(screen, self.bullet_color, (
                        (460 + (self.bullet_pos_x - camera_x)), (310 + (self.bullet_pos_y - camera_y)),
                        self.bullet_width, self.bullet_height))
                    self.bullet_pos_x -= self.bullet_velocity
                else:
                    self.bullet_exists = False
                    if game_map.tiles[tile_coord_x][tile_coord_y] == 2:
                        for monsters in range(len(monster_list)):
                            if monster_list[monsters].monster_pos_x == tile_coord_x and monster_list[
                                    monsters].monster_pos_y == tile_coord_y:
                                monster_list[monsters].monster_health -= 1
                                if monster_list[monsters].monster_health == 0:
                                    game_map.tiles[monster_list[monsters].monster_pos_x][monster_list[
                                        monsters].monster_pos_y] = 0
                                    score += 50
                                    monsters_dead += 1

            # If bullet is shot towards right:
            if self.direction == "right":
                # Here we adjust the starting location:
                if not self.bullet_location_adjusted:
                    self.bullet_pos_x += 10
                    self.bullet_pos_y -= 2
                    self.bullet_location_adjusted = True
                tile_coord_x = int((((self.bullet_pos_x + 450) - ((self.bullet_pos_x + 450) % 20)) / 20) + 1)
                tile_coord_y = int((((self.bullet_pos_y + 320) - ((self.bullet_pos_y + 320) % 20)) / 20))
                if game_map.tiles[tile_coord_x][tile_coord_y] == 0:
                    # Drawing the actual bullet and set its direction of velocity to right:
                    pygame.draw.rect(screen, self.bullet_color, (
                        (460 + (self.bullet_pos_x - camera_x)), (310 + (self.bullet_pos_y - camera_y)),
                        self.bullet_width, self.bullet_height))
                    self.bullet_pos_x += self.bullet_velocity
                else:
                    self.bullet_exists = False
                    if game_map.tiles[tile_coord_x][tile_coord_y] == 2:
                        for monsters in range(len(monster_list)):
                            if monster_list[monsters].monster_pos_x == tile_coord_x and monster_list[
                                    monsters].monster_pos_y == tile_coord_y:
                                monster_list[monsters].monster_health -= 1
                                if monster_list[monsters].monster_health == 0:
                                    game_map.tiles[monster_list[monsters].monster_pos_x][monster_list[
                                        monsters].monster_pos_y] = 0
                                    score += 50
                                    monsters_dead += 1

        # Check if bullet is going to go horizontally and then adjust its drawing shape accordingly:
        if self.orientation == "vertical":
            self.bullet_width = 4
            self.bullet_height = 10

            # If the bullet is shot upwards:
            if self.direction == "up":
                # Here we adjust the starting location:
                if not self.bullet_location_adjusted:
                    self.bullet_pos_x -= 2
                    self.bullet_pos_y -= 10
                    self.bullet_location_adjusted = True
                tile_coord_x = int((((self.bullet_pos_x + 470) - ((self.bullet_pos_x + 470) % 20)) / 20))
                tile_coord_y = int((((self.bullet_pos_y + 310) - ((self.bullet_pos_y + 310) % 20)) / 20) + 1)
                if game_map.tiles[tile_coord_x][tile_coord_y] == 0:
                    # Drawing the actual bullet and set its direction of velocity to up:
                    pygame.draw.rect(screen, self.bullet_color, (
                        (460 + (self.bullet_pos_x - camera_x)), (310 + (self.bullet_pos_y - camera_y)),
                        self.bullet_width, self.bullet_height))
                    self.bullet_pos_y -= self.bullet_velocity
                else:
                    self.bullet_exists = False
                    if game_map.tiles[tile_coord_x][tile_coord_y] == 2:
                        for monsters in range(len(monster_list)):
                            if monster_list[monsters].monster_pos_x == tile_coord_x and monster_list[
                                    monsters].monster_pos_y == tile_coord_y:
                                monster_list[monsters].monster_health -= 1
                                if monster_list[monsters].monster_health == 0:
                                    game_map.tiles[monster_list[monsters].monster_pos_x][monster_list[
                                        monsters].monster_pos_y] = 0
                                    score += 50
                                    monsters_dead += 1

            # If the bullet is shot downwards:
            if self.direction == "down":
                # Here we adjust the starting location:
                if not self.bullet_location_adjusted:
                    self.bullet_pos_x -= 2
                    self.bullet_pos_y += 10
                    self.bullet_location_adjusted = True
                tile_coord_x = int((((self.bullet_pos_x + 470) - ((self.bullet_pos_x + 470) % 20)) / 20))
                tile_coord_y = int((((self.bullet_pos_y + 300) - ((self.bullet_pos_y + 300) % 20)) / 20) + 1)
                if game_map.tiles[tile_coord_x][tile_coord_y] == 0:
                    # Drawing the actual bullet and set its direction of velocity to down:
                    pygame.draw.rect(screen, self.bullet_color, (
                        (460 + (self.bullet_pos_x - camera_x)), (310 + (self.bullet_pos_y - camera_y)),
                        self.bullet_width, self.bullet_height))
                    self.bullet_pos_y += self.bullet_velocity
                else:
                    self.bullet_exists = False
                    if game_map.tiles[tile_coord_x][tile_coord_y] == 2:
                        for monsters in range(len(monster_list)):
                            if monster_list[monsters].monster_pos_x == tile_coord_x and monster_list[
                                    monsters].monster_pos_y == tile_coord_y:
                                monster_list[monsters].monster_health -= 1
                                if monster_list[monsters].monster_health == 0:
                                    game_map.tiles[monster_list[monsters].monster_pos_x][monster_list[
                                        monsters].monster_pos_y] = 0
                                    score += 50
                                    monsters_dead += 1


class Monster:
    def __init__(self):
        self.monster_health = 1
        self.monster_color = green
        self.monster_pos_x = 0
        self.monster_pos_y = 0

    def create_monster(self):
        # Lets make sure monsters don't spawn in the very middle of the map
        self.monster_pos_x = random.randint(1, 77)
        if self.monster_pos_x > 40:
            self.monster_pos_x += 11
        self.monster_pos_y = random.randint(1, 47)
        if self.monster_pos_y > 25:
            self.monster_pos_y += 11

    def draw_monster(self):
        if self.monster_health > 0:
            pos_x = self.monster_pos_x * 20 - camera_x - 10
            pos_y = self.monster_pos_y * 20 - camera_y - 10
            game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 2
            pygame.draw.rect(screen, self.monster_color, (pos_x, pos_y, 20, 20))

    def move_monster(self):
        # Monsters move randomly to 4 different directions
        # Also we need to make sure they don't walk through walls
        random_direction = random.randint(0, 3)
        if random_direction == 0:
            if game_map.tiles[self.monster_pos_x + 1][self.monster_pos_y] == 0:
                # Change the old position value back to 0 (= free space)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 0
                self.monster_pos_x += 1
                # Change the new position value to 2 (=monster in it)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 2
        elif random_direction == 1:
            if game_map.tiles[self.monster_pos_x - 1][self.monster_pos_y] == 0:
                # Change the old position value back to 0 (= free space)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 0
                self.monster_pos_x -= 1
                # Change the new position value to 2 (=monster in it)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 2
        elif random_direction == 2:
            if game_map.tiles[self.monster_pos_x][self.monster_pos_y + 1] == 0:
                # Change the old position value back to 0 (= free space)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 0
                self.monster_pos_y += 1
                # Change the new position value to 2 (=monster in it)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 2
        elif random_direction == 3:
            if game_map.tiles[self.monster_pos_x][self.monster_pos_y - 1] == 0:
                # Change the old position value back to 0 (= free space)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 0
                self.monster_pos_y -= 1
                # Change the new position value to 2 (=monster in it)
                game_map.tiles[self.monster_pos_x][self.monster_pos_y] = 2


'''
Functions
'''


def draw_main_menu():
    for j in range(len(main_menu_items)):
        main_menu_button(screen, black, white, (screen_x / 2 - 100), 200 + (75 * j), 200, 60, main_menu_items[j],
                         mouse_x, mouse_y)


# Function for creating main menu buttons
def main_menu_button(surface, button_color, text_color, x, y, width, height, text, mouse_pos_x, mouse_pos_y):
    # if mouse hovers button, make button red:
    if x <= mouse_pos_x < (x + width) and y <= mouse_pos_y <= (y + height):
        button_color = red
    pygame.draw.rect(surface, button_color, (x, y, width, height))  # Draw the main menu button shape
    font_main_menu_button = pygame.font.Font(None, 40)
    label = font_main_menu_button.render(text, True, text_color)  # Draw the text inside the main menu button
    surface.blit(label, (x + 20, y + 16))


# Function for checking which main_menu_button mouse clicks
def main_menu_button_check(pos, x, y, button_width, button_height):
    return x <= pos[0] < (x + button_width) and y <= pos[1] < (y + button_height)


# Creates a new map and calls for its randomize method and returns the new map
def new_game_map():
    screen.fill(white)
    new_map = Map()
    new_map.randomize()
    return new_map


def draw_score():
    score_font = pygame.font.Font(None, 40)
    score_label = score_font.render("Score: " + str(score), True, black)
    screen.blit(score_label, (10, 10))


def draw_monsters_alive():
    monsters_font = pygame.font.Font(None, 40)
    monsters_label = monsters_font.render("Monsters alive: " + str(monster_amount - monsters_dead), True, black)
    screen.blit(monsters_label, (350, 10))


def draw_ammo_amount():
    ammo_font = pygame.font.Font(None, 40)
    ammo_label = ammo_font.render("Ammo: " + str(ammo), True, black)
    screen.blit(ammo_label, (740, 10))


def create_monster_list():
    for monsters in range(monster_amount):
        monster = Monster()
        monster.create_monster()
        monster_list.append(monster)


def draw_game_over_score():
    score_font = pygame.font.Font(None, 40)
    score_label = score_font.render("Game over! Your score was: " + str(score), True, black)
    screen.blit(score_label, (250, 160))


'''
Main program starts here
'''

pygame.init()

# Colors
white = 255, 255, 255
black = 0, 0, 0
grey = 80, 80, 80
red = 255, 0, 0
green = 0, 255, 0

# Default values for window size and camera location
screen_x = 900
screen_y = 600
camera_x = 440
camera_y = 290

screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("ArenaGame")

# Main menu is created from these menu items
main_menu_items = ["New game", "Quit"]

# Main menu is shown by default
show_main_menu = True

# Game over boolean
game_over = False

# Default values for player
health = 100
score = 0
ammo = 2

# Initialize map to empty map
game_map = Map()

# Initialize player
player = Player()

# Initialize bullet list
bullet_list = []

# Initialize monster_list and monster_amount
monster_list = []
monster_amount = 10
monsters_dead = 0

while True:

    screen.fill(white)

    # Gets current mouse location, needed for menus and aiming
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Call function to draw main_menu_button len(main_menu_items) times
    if show_main_menu:
        draw_main_menu()

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()
            sys.exit()

        elif event.type == MOUSEMOTION:

            mouse_x, mouse_y = event.pos

            move_x, move_y = event.rel

        elif event.type == MOUSEBUTTONDOWN:

            mouse_down = event.button

            # Click to shoot when in game:
            if not show_main_menu:
                click_x = mouse_x - 460
                click_y = mouse_y - 310

                # Shooting left:
                if math.atan2(290, 440 - screen_x) < math.atan2(click_y, click_x) <= math.pi or (
                        - math.pi) < math.atan2(click_y, click_x) < math.atan2(290 - screen_y, 440 - screen_x):
                    bullet = Bullet()
                    bullet.orientation = "horizontal"
                    bullet.direction = "left"
                    bullet.bullet_pos_y = camera_y
                    bullet.bullet_pos_x = camera_x
                    bullet_list.append(bullet)
                    ammo -= 1

                # Shooting right:
                elif math.atan2(290 - screen_y, 440) < math.atan2(click_y, click_x) < 0 \
                        or 0 <= math.atan2(click_y, click_x) < math.atan2(290, 440):
                    bullet = Bullet()
                    bullet.orientation = "horizontal"
                    bullet.direction = "right"
                    bullet.bullet_pos_y = camera_y
                    bullet.bullet_pos_x = camera_x
                    bullet_list.append(bullet)
                    ammo -= 1

                # Shooting up:
                elif math.atan2(290 - screen_y, 440 - screen_x) < math.atan2(click_y, click_x) < math.atan2(
                                290 - screen_y, 440):
                    bullet = Bullet()
                    bullet.orientation = "vertical"
                    bullet.direction = "up"
                    bullet.bullet_pos_y = camera_y
                    bullet.bullet_pos_x = camera_x
                    bullet_list.append(bullet)
                    ammo -= 1

                # Shooting down:
                elif math.atan2(290, 440) < math.atan2(click_y, click_x) < math.atan2(290, 440 - screen_x):
                    bullet = Bullet()
                    bullet.orientation = "vertical"
                    bullet.direction = "down"
                    bullet.bullet_pos_y = camera_y
                    bullet.bullet_pos_x = camera_x
                    bullet_list.append(bullet)
                    ammo -= 1

            mouse_down = event.button

            mouse_down_x, mouse_down_y = event.pos

        elif event.type == MOUSEBUTTONUP:

            mouse_up = event.button

            mouse_up_x, mouse_up_y = event.pos

            # Assign correct jobs for main menu buttons and make selection when clicked:
            if show_main_menu:
                for i in range(len(main_menu_items)):
                    if main_menu_button_check(event.pos, (screen_x / 2 - 100), 200 + (75 * i), 200, 60):
                        if i == 0:
                            game_map = new_game_map()
                            ammo = 100
                            bullet_list = []
                            player = Player()
                            camera_x = 440
                            camera_y = 290
                            monster_list = []
                            monster_amount = 10
                            monsters_dead = 0
                            score = 0
                            show_main_menu = False
                            if game_over:
                                game_over = False

                        elif i == 1:
                            pygame.quit()
                            sys.exit()

    keys = pygame.key.get_pressed()

    if game_over:
        draw_game_over_score()

    if not show_main_menu:
        for b in range(len(bullet_list)):
            if bullet_list[b].bullet_exists:
                bullet_list[b].draw_bullet()

        if len(monster_list) == 0 or monsters_dead == monster_amount:
            if monsters_dead == monster_amount:
                monsters_dead = 0
                monster_amount += 2
                ammo += monster_amount
            create_monster_list()

        # If ammo is 0 and there's still monsters left the next click will end the game:
        if ammo == -1 and monster_amount > 0:
            screen.fill(white)
            show_main_menu = True
            game_over = True

        for m in range(len(monster_list)):
            if not monster_list[m].monster_health == 0:
                monster_list[m].draw_monster()
                if (pygame.time.get_ticks()) % 100 == 0:
                    monster_list[m].move_monster()

    # Variables for offsets. These are used to calculate players exact location.
    offset_x = (camera_x + 460) - (player.player_coordinate_x * 20)
    offset_y = (camera_y + 310) - (player.player_coordinate_y * 20)

    # Key presses to move the player around on the map
    if keys[K_LEFT] or keys[K_a]:
        if not show_main_menu:
            if camera_x < 450 + 900:
                if game_map.tiles[player.player_coordinate_x - 1][player.player_coordinate_y] != 0 and offset_x == 0:
                    camera_x += 0
                elif game_map.tiles[player.player_coordinate_x - 1][
                            player.player_coordinate_y + 1] != 0 and offset_x == 0 and offset_y != 0:
                    camera_x += 0
                else:
                    if player.player_coordinate_x > 0:
                        camera_x -= 1
                        if offset_x <= 0:
                            player.player_coordinate_x -= 1
            else:
                camera_x += 0

    if keys[K_RIGHT] or keys[K_d]:
        if not show_main_menu:
            if camera_x < 450 + 900:
                if game_map.tiles[player.player_coordinate_x + 1][player.player_coordinate_y] != 0 and offset_x == 0:
                    camera_x -= 0
                elif game_map.tiles[player.player_coordinate_x + 1][
                            player.player_coordinate_y + 1] != 0 and offset_x == 0 and offset_y != 0:
                    camera_x -= 0
                else:
                    if player.player_coordinate_x < 88:
                        camera_x += 1
                        if offset_x >= 19:
                            player.player_coordinate_x += 1

            else:
                camera_x += 0

    if keys[K_UP] or keys[K_w]:
        if not show_main_menu:
            if camera_y > 300 - 600:
                if game_map.tiles[player.player_coordinate_x][player.player_coordinate_y - 1] != 0 and offset_y == 0:
                    camera_y += 0
                elif game_map.tiles[player.player_coordinate_x + 1][
                            player.player_coordinate_y - 1] != 0 and offset_y == 0 and offset_x != 0:
                    camera_y += 0
                else:
                    if player.player_coordinate_y > 0:
                        camera_y -= 1
                        if offset_y <= 0:
                            player.player_coordinate_y -= 1
            else:
                camera_y += 0

    if keys[K_DOWN] or keys[K_s]:
        if not show_main_menu:
            if camera_y < 300 + 600:
                if game_map.tiles[player.player_coordinate_x][player.player_coordinate_y + 1] != 0 and offset_y == 0:
                    camera_y += 0
                elif game_map.tiles[player.player_coordinate_x + 1][
                            player.player_coordinate_y + 1] != 0 and offset_y == 0 and offset_x != 0:
                    camera_y += 0
                else:
                    if player.player_coordinate_y < 58:
                        camera_y += 1
                        if offset_y >= 19:
                            player.player_coordinate_y += 1
            else:
                camera_y += 0

    if not show_main_menu:
        game_map.draw(camera_x, camera_y)

    if not show_main_menu:
        player.draw_player()
        draw_score()
        draw_monsters_alive()
        draw_ammo_amount()

    pygame.display.update()
