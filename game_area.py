"""
this will be the tapping area with the player, party, baddies
hopfully get some upgrades to the player and party to work too.
"""

import pygame
import random
from learning_classes_copy import ScrollingButton, UpgradeButton, Bad, Player

pygame.init()

# region: color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)
dark_gray = (72, 84, 84)
darker_gray = (55, 58, 62)
# endregion

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
background = black
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()
framerate = 60

margin = 5
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
horizontal_square_size = 50
scrolling_button_height = horizontal_square_size + margin
num_scrolling_buttons = 6
total_buttons_height = (num_scrolling_buttons * scrolling_button_height) + (num_scrolling_buttons * margin) + (
        margin * 2)
scrollable_content_height = total_buttons_height
scrollable_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 3)
scrollable_content = pygame.Surface((scrollable_rect.width, scrollable_content_height))
upgrade_screen = pygame.Rect(0, 0, 0, 0)
upgrade_rect_height = (SCREEN_HEIGHT / 3) - margin
scrollable_rect.top = SCREEN_HEIGHT - horizontal_square_size - (margin * 2) - scrollable_rect.height
upgrade_rect_top = 0
# scrollable_num_buttons = 10
# scrollable_button_height = 50
target_scroll_position = 0
scroll_speed = 6
scroll_position = 0
scrollbar_rect = pygame.Rect(595, 496, 10, 295)
scrollbar_handle_height = int(upgrade_rect_height * (scrollable_rect.height / scrollable_content_height))
scrollbar_handle_rect = pygame.Rect(scrollbar_rect.left, scrollable_rect.top, scrollbar_rect.width,
                                    (scrollbar_handle_height - margin))
tapping_area = pygame.Rect(0, 0, 600, 464)

player = ScrollingButton(7, 7, "Images\character.png", "Adventurer", "This is the area for tap damage", "Level 1", None,
                         scrollable_content)
auto_tap = ScrollingButton(7, 67, None, "Auto Tap Spell", "This spell will auto tap X times per second for 10 seconds",
                           "Level 1", None, scrollable_content)
more_money = ScrollingButton(7, 127, None, "More Money Spell",
                             "This spell will increase gold earned by X% for 10 seconds", "Level 1", None,
                             scrollable_content)
crit_chance = ScrollingButton(7, 187, None, "Increase Crit",
                              "This spell will increase tap crit chance by X% for 60 seconds", "Level 1", None,
                              scrollable_content)
skill_effect = ScrollingButton(7, 247, None, "Skill Up",
                               "This spell will increase effect of all spells by X% for 15 seconds", "Level 1", None,
                               scrollable_content)
cooldown = ScrollingButton(7, 307, None, "Cooldowns", "This spell will reduce cooldowns of all spells by X seconds",
                           "Level 1", None, scrollable_content)

upgrade_player = UpgradeButton(467, 10, "Images\gold.png", "Next Level:\n" "+X Damage", "200", scrollable_content)
upgrade_auto_tap = UpgradeButton(467, 70, "Images\gold.png", "Next Level:\n" "+X Taps", "300", scrollable_content)
upgrade_more_money = UpgradeButton(467, 130, "Images\gold.png", "Next Level:\n" "+X% Gold", "800", scrollable_content)
upgrade_crit_chance = UpgradeButton(467, 190, "Images\gold.png", "Next Level:\n" "+X% Crit Chance", "1300",
                                    scrollable_content)
upgrade_skill_effect = UpgradeButton(467, 250, "Images\gold.png", "Next Level:\n" "+X% Effect", "4200",
                                     scrollable_content)
upgrade_cooldown = UpgradeButton(467, 310, "Images\gold.png", "Next Level:\n" "+X% Seconds", "9200", scrollable_content)

tap_damage = 1
tap_upgrade_cost = 10
total_gold = 0
bad_health = 7

bad = Bad()
player = Player()


def draw_horizontal_buttons():
    global horizontal_num_squares
    global margin
    global horizontal_square_size

    horizontal_num_squares = 6
    margin = 5

    # region: square_size explanation
    # number of squares + 1 because there is 1 more divider for the amount of squares, those dividers
    # multiplied by the margin size will give us even spacing when dividing by the amount of squares
    # endregion
    horizontal_square_size = (SCREEN_WIDTH - (horizontal_num_squares + 1) * margin) // horizontal_num_squares
    for i in range(horizontal_num_squares):
        # region: coordinate explanation:
        # multiplying square number by the margin plus the square size to move to the right the
        # same amount of pixels as a margin and square size amount.
        # y coordinate is simpler, just needed to have enough space for the square and the margin
        # endregion
        x_coord = (i + 1) * margin + i * horizontal_square_size
        y_coord = SCREEN_HEIGHT - horizontal_square_size - margin
        tab_button = pygame.draw.rect(screen, dark_gray,
                                      [x_coord, y_coord, horizontal_square_size, horizontal_square_size])
        tab_name = font.render(str(i + 1), True, white)
        text_rect = tab_name.get_rect(
            center=(x_coord + horizontal_square_size // 2, y_coord + horizontal_square_size // 2))
        screen.blit(tab_name, text_rect)


def draw_game_screen():
    screen.fill(black)
    draw_horizontal_buttons()


def draw_upgrade_screen():
    global upgrade_rect_top
    global upgrade_rect_height
    global upgrade_screen
    global scroll_position

    # region: Placement explanation
    # I want the scrollable screen to be a third of the screen size and for the first corner
    # we can use the rect_top to line up with the square square size and margin size
    # endregion

    upgrade_rect_top = SCREEN_HEIGHT - horizontal_square_size - (margin * 2) - upgrade_rect_height

    # region: pygame.react explanation
    # if we make upgrade_screen a pygame.rect we can use that rectangle's position
    # for the bottom of the damage/currencies bar
    # endregion
    upgrade_screen = pygame.Rect(0, upgrade_rect_top, SCREEN_WIDTH, upgrade_rect_height)
    pygame.draw.rect(screen, darker_gray, upgrade_screen)

    scroll_position += (target_scroll_position - scroll_position) * 0.5

    scrollbar_handle_rect.top = upgrade_screen.top + int(
        target_scroll_position / scrollable_content_height * upgrade_screen.height)

    # Update scrollable_rect to reflect the scrolling position
    scrollable_rect.top = upgrade_screen.top

    screen.blit(scrollable_content, (scrollable_rect.left, (scrollable_rect.top)),
                (0, scroll_position, scrollable_rect.width, scrollable_rect.height - margin))

    pygame.draw.rect(screen, white, scrollbar_rect)
    pygame.draw.rect(screen, (100, 100, 100), scrollbar_handle_rect)


def draw_damage_stat_bar():
    # region: .Rect explanation
    # Here we are putting a rectangle of stats on top of the upgrade screen rectangle.
    # First we are making rect be a rectangle touching the screens edge that is as wide
    # as the screen with a height of a third of the buttons at the bottom.
    # then putting the bottom of rect to be the top of the upgrade screen
    # endregion
    rect = pygame.Rect(0, 0, SCREEN_WIDTH, horizontal_square_size / 3)
    rect.bottom = upgrade_screen.top
    pygame.draw.rect(screen, dark_gray, rect)

    # Same Idea as horizontal game buttons
    num_squares = 4
    left_right_margin = 50
    upper_lower_margin = 5

    square_width = (SCREEN_WIDTH - (num_squares + 1) * left_right_margin) // num_squares
    square_height = horizontal_square_size / 3 - 2 * upper_lower_margin

    for i in range(num_squares):
        x_coord = (i + 1) * left_right_margin + i * square_width
        y_coord = rect.top + upper_lower_margin
        inner_rect = pygame.Rect(x_coord, y_coord, square_width, square_height)
        pygame.draw.rect(screen, darker_gray, inner_rect)

        # region: Placeholder explaination
        # here we are just putting a placehold for images later.
        # the .8 and the 1.1 we trial and error which may not work on all screens.
        # TEST HOW IT LOOKS FOR OTHER DEVICES !!!!!!!!!
        # endregion
        placeholder_width = left_right_margin * .8
        placeholder_height = square_height
        placeholder_rect = pygame.Rect(x_coord - (placeholder_width * 1.1), y_coord, placeholder_width,
                                       placeholder_height)
        pygame.draw.rect(screen, (red), placeholder_rect)


test_button = pygame.Rect(100, 100, 50, 50)

running = True
while running:
    timer.tick(framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                target_scroll_position -= scroll_speed
            elif event.button == 5:  # Scroll down
                target_scroll_position += scroll_speed
            elif event.button == 1:  # Left mouse button
                # Deplete health on left mouse button click
                bad.health -= tap_damage
                if bad.health <= 0:
                    bad.health = 0
                    # Step 1: Generate random gold between 3 and 6
                    earned_gold = random.randint(3, 6)
                    # Step 2: Add earned gold to total gold
                    total_gold += earned_gold
                    # Step 3: Slightly increase max health
                    bad.max_health *= 1.2
                    # Step 3: Refill the health bar
                    bad.health = bad.max_health
                # Check if the mouse is over the upgrade_player button
                if upgrade_player.rect.move(scrollable_rect.x, scrollable_rect.y).collidepoint(event.pos):
                    # The mouse is over the upgrade_player button
                    # Perform your actions here, such as handling the button click
                    print("Upgrade Player button clicked!")
                    # Add your logic for upgrading the player here
            # print("Mouse Clicked at:", event.pos)
            # if event.button == 1 and test_button.collidepoint(event.pos):
            #     print("Test Button Clicked!")

    # Update total_gold_text inside the loop to reflect the current value
    total_gold_text = font.render(str(round(total_gold)), True, white)

    draw_game_screen()
    draw_upgrade_screen()
    draw_damage_stat_bar()
    screen.blit(total_gold_text, (290, 20))

    pygame.draw.polygon(screen, darker_gray, [(0, 350), (300, 200), (600, 350), (600, 464), (0, 464)])
    pygame.draw.rect(screen, black, tapping_area, 1)
    bad.render()
    player.render()
    # pygame.draw.rect(screen, white, test_button)
    # pygame.draw.rect(screen, green, upgrade_player.rect)

    if target_scroll_position < 0:
        target_scroll_position = 0
    elif target_scroll_position > scrollable_content_height - scrollable_rect.height:
        target_scroll_position = scrollable_content_height - scrollable_rect.height

    pygame.draw.rect(screen, "Green", upgrade_player.rect.move(scrollable_rect.x, scrollable_rect.y - target_scroll_position))
    screen.blit(font.render(f"{target_scroll_position}", False, "White"), (20, 20))

    pygame.display.update()
    timer.tick(framerate)

pygame.quit()
