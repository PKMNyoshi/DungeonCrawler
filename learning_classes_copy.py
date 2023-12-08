"""
Will initially use this copy to use in my main copy copy so i don't mess up things that are working
"""

import pygame

pygame.init()

# region: color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)
gray = (72, 84, 84)
dark_gray = (72, 84, 84)
darker_gray = (55, 58, 62)
# endregion
tap_damage = 1

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Dungeon Crawlers')
background = white
font = pygame.font.Font('freesansbold.ttf', 16)
font2 = pygame.font.Font('freesansbold.ttf', 12)
timer = pygame.time.Clock()
fps = 60


class ScrollingButton:
    def __init__(self, x_pos, y_pos, image, name, description, level, dps, surface):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image
        self.name = name
        self.description = description
        self.level = level
        self.dps = dps
        self.surface = surface  # Pass the surface as a parameter
        self.draw()

    # main thing is draw these to scrollable content and not the screen
    def draw(self):
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (580, 55))
        pygame.draw.rect(self.surface, darker_gray, button_rect, 0, 10)
        pygame.draw.rect(self.surface, 'white', button_rect, 2, 10)
        if self.image is not None:
            button_image = pygame.image.load(self.image)
            self.surface.blit(button_image, (self.x_pos + 5, self.y_pos + 3))
        if self.name is not None:
            button_name = font.render(self.name, True, white)
            self.surface.blit(button_name, (self.x_pos + 50, self.y_pos + 5))
        if self.description is not None:
            button_description = font2.render(self.description, True, white)
            self.surface.blit(button_description, (self.x_pos + 50, self.y_pos + 30))
        if self.level is not None:
            button_level = font.render(self.level, True, white)
            self.surface.blit(button_level, (self.x_pos + 400, self.y_pos + 3))
        if self.dps is not None:
            button_dps = font.render(self.dps, True, white)
            self.surface.blit(button_dps, (self.x_pos + 400, self.y_pos + 30))


class UpgradeButton:
    def __init__(self, x_pos, y_pos, currency_image, upgrade_text, upgrade_cost, surface):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.currency_image = currency_image
        self.upgrade_text = upgrade_text
        self.upgrade_cost = upgrade_cost
        self.surface = surface
        self.rect = pygame.Rect((self.x_pos, self.y_pos), (117, 49))  # Create a pygame.Rect for the button
        self.draw()

    def draw(self):
        # button_rect = pygame.Rect((self.x_pos, self.y_pos), (117, 49))
        pygame.draw.rect(self.surface, gray, self.rect, 0, 10)
        pygame.draw.rect(self.surface, white, self.rect, 2, 10)

        # Calculate the center position for text within the button
        text_center_x = self.x_pos + self.rect.width // 2
        text_center_y = self.y_pos + self.rect.height // 2

        if self.currency_image is not None:
            currency_image = pygame.image.load(self.currency_image)
            self.surface.blit(currency_image, (self.x_pos + 5, self.y_pos + 33))
        if self.upgrade_text is not None:
            upgrade_text = font2.render(self.upgrade_text, True, white)
            text_rect = upgrade_text.get_rect(center=(text_center_x, self.y_pos + 17))
            self.surface.blit(upgrade_text,
                              text_rect.topleft)  # Use the top-left corner of the text rect for blitting       #(self.x_pos + 58, self.y_pos + 5))
        if self.upgrade_cost is not None:
            upgrade_cost = font2.render(self.upgrade_cost, True, white)
            self.surface.blit(upgrade_cost, (self.x_pos + 80, self.y_pos + 33))

    def is_mouse_over(self):
        # Check if the mouse is over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)


class Player:
    def __init__(self):
        global tap_damage
        self.player_image = "Images\player-export.png"

    def draw_player(self):
        player_image = pygame.image.load(self.player_image)
        screen.blit(player_image, (225, 360))

    def render(self):
        self.draw_player()


class Bad:
    def __init__(self):
        global tap_damage
        self.health = 7
        self.max_health = 7
        self.health_bar_length = 150
        self.bad_guy = "images/skeleton-export.png"

    def draw_health_bar(self):
        pygame.draw.rect(screen, black, [350, 250, self.health_bar_length, 20], 0, 10)
        pygame.draw.rect(screen, red, [350, 250, self.health_bar_length * (self.health / self.max_health), 20], 0, 10)
        health_bar_border = pygame.draw.rect(screen, white, [350, 250, self.health_bar_length, 20], 2, 10)
        health_text = font.render(str(round(self.health)), True, white)
        screen.blit(health_text, (480, 270))

    def draw_bad_guy(self):
        bad_guy_image = pygame.image.load(self.bad_guy)
        bad_name_text = font.render('Skeleton', True, white)
        screen.blit(bad_name_text, (350, 270))
        screen.blit(bad_guy_image, (400, 300))

    def render(self):
        self.draw_health_bar()
        self.draw_bad_guy()

# bad_health = BadHealth()

# run = True
# while run:
#     screen.fill('black')
#     timer.tick(fps)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # Left mouse button
#                 # Deplete health on left mouse button click
#                 bad_health.health -= tap_damage
#                 if bad_health.health < 0:
#                     bad_health.health = 0

#     bad_health.render()

#     pygame.display.flip()
# pygame.quit()

# bad_health = BadHealth()
# bad_health.render()


# region tutorial
# WIDTH = 500
# HEIGHT = 500
# screen = pygame.display.set_mode([WIDTH, HEIGHT])
# fps = 60
# timer = pygame.time.Clock()
# font = pygame.font.Font('freesansbold.ttf', 18)
# pygame.display.set_caption('Buttons!')
# button1_enabled = True
# button2_enabled = True
# new_press = True

# class Button:
#     def __init__(self, text, x_pos, y_pos, enabled):
#         self.text = text
#         self.x_pos = x_pos
#         self.y_pos = y_pos
#         self.enabled = enabled
#         self.draw()

#     def draw(self):
#         button_text = font.render(self.text, True, 'black')
#         button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150, 25))
#         if self.enabled:
#             if self.check_click():
#                 pygame.draw.rect(screen, 'dark gray', button_rect, 0, 5)
#             else:
#                 pygame.draw.rect(screen, 'light gray', button_rect, 0, 5)
#         else:
#             pygame.draw.rect(screen, 'black', button_rect, 0, 5)
#         pygame.draw.rect(screen, 'black', button_rect, 2, 5)
#         screen.blit(button_text, (self.x_pos + 3, self.y_pos + 3))

#     def check_click(self):
#         mouse_pos = pygame.mouse.get_pos()
#         left_click = pygame.mouse.get_pressed()[0] #0 is left click
#         button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150, 25))
#         if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
#             return True
#         else:
#             return False
# endregion

# region
# my_button = Button('Click Me!', 10, 10, button1_enabled)
# my_button2 = Button('Click Me Too!', 10, 40, button2_enabled)
# my_button3 = Button('Click Me Three!', 10, 70, True)

# # this is like a toggle. pressing button3 will make button with disabled.
# if pygame.mouse.get_pressed()[0] and new_press:
#     new_press = False
#     if my_button3.check_click():
#         if button1_enabled:
#             button1_enabled = False
#             button2_enabled = False
#         else:
#             button1_enabled = True
#             button2_enabled = True
# if not pygame.mouse.get_pressed()[0] and not new_press:
#     new_press = True

# # this is doing a function for the duration of the button being pressed.
# # in this case it just prints some text while you're holding button2 down.
# if my_button2.check_click():
#     button_text = font.render('Button 2 is being pressed', True, 'black')
#     screen.blit(button_text, (100, 200))
# endregion
