# Richard Han and Adam Abdi
# Chernobyl Adverntures
# January 16, 2019

import pygame
import shop_module


def draw_start_button(screen, BLACK, WHITE, start_x, start_y, button_width, button_height, font):
    """Draws start button"""
    pygame.draw.rect(screen, WHITE, [start_x, start_y, button_width, button_height], 0)
    text = font.render('START', True, BLACK)
    screen.blit(text, [start_x + 22, start_y + 12])


def draw_instructions(screen, DARKGREY, instruction_font, BLACK):
    """Draws instructions"""
    
    # List for text
    instruction_text = []
    
    # Appends text into list
    pygame.draw.rect(screen, DARKGREY, [430, 180, 700, 300])
    instruction_text.append(instruction_font.render("- Use A and D to move left and right", True, BLACK))
    instruction_text.append(instruction_font.render("- While in the shop, click on inventory items to sell,", True, BLACK))
    instruction_text.append(instruction_font.render("and click on shop items to buy ", True,BLACK))
    instruction_text.append(instruction_font.render("- Press SORTIE to start the playing", True, BLACK))
    instruction_text.append(instruction_font.render("- During the sortie phase run into chests to get items", True, BLACK))
    instruction_text.append(instruction_font.render("- To use items, select a character then an item", True, BLACK))
    instruction_text.append(instruction_font.render("- To attack, select a character, then an enemy, then the attack icon", True, BLACK))
    instruction_text.append(instruction_font.render("- To heal, select a character, then press heal button", True, BLACK))
    instruction_text.append(instruction_font.render("- If you use a character's action, the black square will disappear and,", True, BLACK))
    instruction_text.append(instruction_font.render("they can't do anything until it's their turn again", True, BLACK))
    instruction_text.append(instruction_font.render("- Once you have used all your actions, the enemy will attack the weakest character", True, BLACK))
    instruction_text.append(instruction_font.render("- When you beat all the enemies in the walking phase", True, BLACK))
    instruction_text.append(instruction_font.render("you will be returned to the shop where you can try again", True, BLACK))
    instruction_text.append(instruction_font.render("- This game is permadeath, if you lose a character, they will be", True, BLACK))
    instruction_text.append(instruction_font.render("lost forever", True, BLACK))
    instruction_text.append(instruction_font.render("- If all your characters die, the game ends", True, BLACK))
    instruction_text.append(instruction_font.render("Click anywhere to exit this menu...", True, BLACK))
    
    # Blits instructions to screen
    for i in range(len(instruction_text)):
        screen.blit(instruction_text[i], [433, 200 + 15 * i])


def draw_exit_button(screen, BLACK, WHITE, exit_x, exit_y, button_width, button_height, font):
    """Draws exit button"""
    pygame.draw.rect(screen, WHITE, [exit_x, exit_y, button_width, button_height], 0)
    text = font.render('EXIT', True, BLACK)
    screen.blit(text, [exit_x + 26, exit_y + 10])


def draw_instruction_button(screen, BLACK, WHITE, instruction_x, instruction_y, instruction_button_width, instruction_button_height, font):
    """ Draws instructions"""
    pygame.draw.rect(screen, WHITE, [instruction_x, instruction_y, instruction_button_width, instruction_button_height], 0)
    text = font.render('INSTRUCTIONS', True, BLACK)
    screen.blit(text, [instruction_x + 13, instruction_y + 10])


def draw_start_button(screen, BLACK, WHITE, start_x, start_y, button_width, button_height, font):
    """Draws start button"""
    pygame.draw.rect(screen, WHITE, [start_x, start_y, button_width, button_height], 0)
    text = font.render('START', True, BLACK)
    screen.blit(text, [start_x + 22, start_y + 12])


def button_click(x_pos, y_pos, mouse, width, height):
    """Determines if mouse is within given boundaries"""
    if x_pos < mouse[0] < x_pos + width and y_pos < mouse[1] < y_pos + height:
        return True


def main():
    """Handles starting splash screen and buttons"""
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARKGREY = (241, 241, 241)

    # Activates pygame
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (1280, 730)
    screen = pygame.display.set_mode(size)

    # Title bar
    pygame.display.set_caption("Chernobyl Adventures")

    # Loop until the user clicks the close button.
    done = False

    # instruction button
    instruction = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Enemy image on screen
    enemies = pygame.image.load("images/enemysprites.png").convert()

    # Makes the enemy image transparent
    enemies.set_colorkey(WHITE)

    # background image
    background = pygame.image.load("images/background2.png").convert()

    # Fonts
    font = pygame.font.SysFont('Calibri', 22, True, False)
    instruction_font = pygame.font.SysFont('Calibri', 18, True, False)
    title_font = pygame.font.SysFont('Calibri', 50, True, True)

    # Start button pos
    start_x = 40
    start_y = 300

    # Button dimensions
    button_width = 100
    button_height = 50

    # Instruction button dimensions
    instruction_button_width = 160
    instruction_button_height = 50

    # Instruction button pos
    instruction_x = 40
    instruction_y = 360

    # Exit button_pos
    exit_x = 40
    exit_y = 420
    
    # Background music
    main_menu_music = pygame.mixer.Sound("sounds/main_menu_music.ogg")
    main_menu_music.play(4, 113000)

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse pos
                mouse = pygame.mouse.get_pos()

                # check if start is clicked
                start = button_click(start_x, start_y, mouse, button_width, button_height)

                # check if instruction is clicked
                instruction = button_click(instruction_x, instruction_y, mouse, instruction_button_width, instruction_button_height)

                # check if exit is clicked
                exit = button_click(exit_x, exit_y, mouse, button_width, button_height)

                # if start is clicked stop music
                if start is True:
                    main_menu_music.stop()
                    shop_module.shop()
                    quit()
                elif exit is True:
                    done = True

        # draw background image
        screen.blit(background, [0, 0])

        # draw enemy image
        screen.blit(enemies, [700, 370])

        # draw start button
        draw_start_button(screen, BLACK, WHITE, start_x, start_y, button_width, button_height, font)

        # draw instruction button
        draw_instruction_button(screen, BLACK, WHITE, instruction_x, instruction_y, instruction_button_width, instruction_button_height, font)

        # draws exit button
        draw_exit_button(screen, BLACK, WHITE, exit_x, exit_y, button_width, button_height, font)

        # Draw credits
        text = font.render('By Richard Han & Adam Abdi - ICT12 Computer Programming 2018-2019', True, BLACK)
        screen.blit(text, [0, 700])

        # Draw title
        text = title_font.render('Chernobyl Adventures', True, BLACK)
        screen.blit(text, [300, 200])

        # Draws instruction
        if instruction is True:
            draw_instructions(screen, DARKGREY, instruction_font, BLACK)

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()
