# Richard Han
# Shop module
# 20/12/2018

import pygame
from sprite_strip_anim import SpriteStripAnim
import sortie_module
import random
import chernobyl_adventures


class Item:
    """Class for items in the game, they have a name, image, and price"""
    def __init__(self, name, image, price):
        """Constructor function"""
        self.name = name
        self.image = image
        self.price = price



class Inventory:
    """Class for the player's inventory, with money and a grid of items"""
    def __init__(self):
        """Constructor function"""
        self.inventory = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
        self.rubles = 1000
        self.full = False

    def add_item(self, item):
        """Searches for empty spot in inventory grid, then adds an item to that spot."""
        item_found = False
        for row in range(3):
            for column in range(4):
                if self.inventory[row][column] == 0:
                    self.inventory[row][column] = item
                    item_found = True
                    break
            if item_found is True:
                break

    def remove_item(self, row, column):
        """Removes item from given coordinates"""
        self.inventory[row][column] = 0


class Character:
    def __init__(self):
        """Class of all character. Multiple stats, location and other variables"""
        self.name = ""
        self.dodge = 0
        self.health_max = 0
        self.health = 0
        self.minimum_damage = 0
        self.maximum_damage = 0
        self.grid = 0
        self.player = 0
        self.image = 0
        self.x = 0
        self.y = 0
        self.turn = False
        self.dead = False
        self.damage_taken = 0
        self.time_to_blit = None
        
    def draw(self, screen, font, BLACK, battle=False, player=False):
        """Draws onto the screen, displays damage taken, and turn availability"""
        # if instance of character is not dead
        if self.dead is False:
            # Draw image and health
            screen.blit(self.image, [self.x, self.y])
            screen.blit(font.render(str(self.health) + " / " + str(self.max_health), True, BLACK), [self.x + 35, self.y + 130])
            # If it is a player and in a battle, draw the turn rectangle
            if battle is True:
                if player is True:
                    if self.turn is False:
                        pygame.draw.rect(screen, BLACK, [self.x + 59, self.y - 20, 10, 10])
        # When time_to_blit is not none blit for 2 seconds
        if self.time_to_blit:
            # if time limit reached, make damage text disappear
            if pygame.time.get_ticks() >= self.time_to_blit:
                self.damage_taken = 0
                self.time_to_blit = None
            # if damage is -1, it is a grazing shot
            if self.damage_taken == -1:
                screen.blit(font.render(str(self.damage_taken) + " GRAZED", True, BLACK), [self.x + 100, self.y - 50])
            # Display if damage is taken
            elif self.damage_taken != 0:
                screen.blit(font.render(str(self.damage_taken), True, BLACK), [self.x + 100, self.y - 50])


def character_def():
    """Handles loading the player sprites and the positions, Then returns the character """
    characters = []
    for i in range(4):
        character = Character()
        character.name = "Blyat Brothers"
        character.dodge = random.randrange(10, 20)
        character.max_health = random.randrange(25, 40)
        character.health = character.max_health
        character.minimum_damage = random.randrange(3, 12)
        character.maximum_damage = random.randrange(12, 17)
        character.grid = SpriteStripAnim('images/charactersprites.png', (0, 0 + 128 * i, 128, 128), 4, -1, True, 10)
        character.image = character.grid.next()
        character.x = 20 + 115 * i
        character.y = 350
        character.turn = False
        character.dead = False

        characters.append(character)
    return characters


def image_block(filename, width, height, count, color_key):
    """Loads and appends images"""
    
    sprite_list = []
    for i in range(count):
        blocks = SpriteStripAnim(filename, (0 + width * i, 0, width, height), count, color_key)
        sprite_image = blocks.next()
        sprite_list.append(sprite_image)
    return sprite_list


def draw_inventory(player_inventory, screen, BLACK, WHITE, inventory_x, inventory_y, square, font):
    """Draws inventory section"""
    # Draws WHITE background
    pygame.draw.rect(screen, WHITE, [inventory_x, inventory_y, square * 4, square * 3], 0)
    # Blits inventory images
    for row in range(3):
        for column in range(4):
            if player_inventory.inventory[row][column] != 0:
                screen.blit(player_inventory.inventory[row][column].image, [inventory_x + square * column, inventory_y + square * row])
    # Draws 4x3 border boxes
    for row in range(3):
        for column in range(4):
            pygame.draw.rect(screen, BLACK, [inventory_x + square * column, inventory_y + square * row, square, square], 2)
    # Blits "INVENTORY" onto screen
    text = font.render('INVENTORY', True, BLACK)
    screen.blit(text, [inventory_x, inventory_y - 20])


def draw_shop(shop_items, screen, BLACK, shop_x, shop_y, square, font):
    """Draws shop section"""
    # Iterates through shop item images and blits out the images of the items
    item_counter = 0
    for row in range(2):
        for column in range(2):
            screen.blit(shop_items[item_counter].image, [shop_x + square * column, shop_y + square * row])
            item_counter += 1

    # Creates 4x4 border boxes
    for row in range(2):
        for column in range(2):
            pygame.draw.rect(screen, BLACK, [shop_x + square * row, shop_y + square * column, square, square], 2)
    # Blits shop text
    text = font.render('SHOP', True, BLACK)
    screen.blit(text, [shop_x, shop_y - 20])


def draw_upgrade_button(screen, BLACK, WHITE, upgrade_x, upgrade_y, button_width, button_height, font):
    """Draws upgrade button"""
    pygame.draw.rect(screen, WHITE, [upgrade_x, upgrade_y, button_width, button_height], 0)
    text = font.render('UPGRADE', True, BLACK)
    screen.blit(text, [upgrade_x + 6, upgrade_y + 10])


def draw_sortie_button(screen, BLACK, WHITE, sortie_x, sortie_y, button_width, button_height, font):
    """Draws sortie button"""
    pygame.draw.rect(screen, WHITE, [sortie_x, sortie_y, button_width, button_height], 0)
    text = font.render('SORTIE', True, BLACK)
    screen.blit(text, [sortie_x + 15, sortie_y + 10])


def draw_item_instructions(screen, instruction_font, BLACK):
    """Draws item use instructions"""

    # List of text
    instructions = []

    # Appends text into list
    instructions.append(instruction_font.render("Item Use:", True, BLACK))
    instructions.append(instruction_font.render("- Healthpacks heals characters for 4 health ", True, BLACK))
    instructions.append(instruction_font.render("- Anti-Rad stops radiation damage when used ", True, BLACK))
    instructions.append(instruction_font.render("- Adrenaline raises maximum damage value ", True, BLACK))
    instructions.append(instruction_font.render("- Vodka increases targets dodge when used ", True, BLACK))

    # Displays text with spacing
    for i in range(len(instructions)):
        screen.blit(instructions[i], [72, 420 + 15 * i])


def grid_find(pos, mouse, square):
    """Calculates grid position based on given variables"""
    grid = (mouse - pos) // square
    return grid


def buy_item(x_pos, y_pos, mouse, square, inventory, shop_items):
    """Adds item to inventory and subtracts item price from money or doesn't if inv is full"""
    column = grid_find(x_pos, mouse[0], square)
    row = grid_find(y_pos, mouse[1], square)
    item_click = False

    # Checks if inventory is full
    inventory.full = True
    for inv_row in range(3):
        for inv_column in range(4):
            if inventory.inventory[inv_row][inv_column] == 0:
                inventory.full = False

    # If inventory is not full
    if inventory.full is False:
        # Second quadrant
        if row == 0 and column == 0:
            selected_item = shop_items[0]
            item_click = True
        # First quadrant
        elif row == 0 and column == 1:
            selected_item = shop_items[1]
            item_click = True
        # Third quadrant
        elif row == 1 and column == 0:
            item_click = True
            selected_item = shop_items[2]
        # Fourth quadrant
        elif row == 1 and column == 1:
            item_click = True
            selected_item = shop_items[3]

        # Item has been selected
        if item_click is True:
            difference = inventory.rubles - selected_item.price
            # Check if sufficient funds
            if difference >= 0:
                inventory.add_item(selected_item)
                inventory.rubles -= selected_item.price
                return inventory
    return inventory


def sell_item(x_pos, y_pos, mouse, square, inventory):
    """Removes item and adds item price to money"""
    grid_column = grid_find(x_pos, mouse[0], square)
    grid_row = grid_find(y_pos, mouse[1], square)

    # If click is within inventory boundaries
    if 0 <= grid_row <= 2 and 0 <= grid_column <= 3:
        # If selected box has an item
        if inventory.inventory[grid_row][grid_column] != 0:
            inventory.rubles += inventory.inventory[grid_row][grid_column].price
            inventory.remove_item(grid_row, grid_column)
            return inventory
    return inventory


def shop():
    """Handles shop, menu buttons, and items"""
    pygame.init()

    # Assigns a class Inventory
    player_inventory = Inventory()

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (211, 211, 211)
    DARKGREY = (241, 241, 241)

    # Set the width and height of the screen [width, height]
    size = (1280, 730)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chernobyl Adventures")

    # Loop until the user clicks the close button.
    done = False
    
    # Checks if user clicks instruction button
    instructions = False

    # defines player characters
    character_list = character_def()
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # fonts
    font = pygame.font.SysFont('Calibri', 22, True, False)
    instruction_font = pygame.font.SysFont('Calibri', 18, True, False)

    # normal button dimensions
    button_width = 100
    button_height = 50

    # instruction button dimensions
    instruction_button_width = 160
    instruction_button_height = 50

    # instruction button pos
    instruction_x = 809
    instruction_y = 530

    # sortie button pos
    sortie_x = 990
    sortie_y = 530

    # exit button pos
    exit_x = 1110
    exit_y = 530

    # shop pos
    shop_x = 70
    shop_y = 292

    # inventory pos
    inventory_x = 70
    inventory_y = 86

    # size of squares
    square = 48

    # gets item images from sprite sheet
    item_images = image_block('images/Items48.png', square, square, 4, None)

    # define the items
    antirad = Item('Anti-rad', item_images[0], 100)
    adrenaline = Item('Adrenaline', item_images[1], 400)
    vodka = Item('Vodka', item_images[2], 300)
    bandage = Item('Bandage', item_images[3], 200)

    # Add them to a list
    shop_items = [antirad, adrenaline, vodka, bandage]

    # laods background image
    backgroundimage = pygame.image.load('images/shopbackground.png').convert_alpha()

    # Runescape music
    shop_music = pygame.mixer.Sound('sounds/shop_music.ogg')
    shop_music.play()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # checks if done button was clicked
                done = chernobyl_adventures.button_click(exit_x, exit_y, mouse, button_width, button_height)
                # checks if sortie button was clicked
                sortie = chernobyl_adventures.button_click(sortie_x, sortie_y, mouse, button_width, button_height)
                # if sorties button was clicked
                if sortie is True:
                    shop_music.stop()
                    sortie_module.sortie(player_inventory, shop_items, character_list)
                    shop_music.play()

                # checks if instructions button is clicked
                instructions = chernobyl_adventures.button_click(instruction_x, instruction_y, mouse, instruction_button_width, instruction_button_height)

                # Checks if item was bought
                player_inventory = buy_item(shop_x, shop_y, mouse, square, player_inventory, shop_items)

                # Checks if item was sold
                player_inventory = sell_item(inventory_x, inventory_y, mouse, square, player_inventory)

        # background color
        screen.fill(DARKGREY)

        # draws shopkeeper guy
        screen.blit(backgroundimage, [0, 0])

        # Grey rectangles for prettiness
        pygame.draw.rect(screen, GREY, [40, 40, 500, 320])
        pygame.draw.rect(screen, GREY, [40, 360, 1200, 240], 0)       

        # Draws inventory
        draw_inventory(player_inventory, screen, BLACK, WHITE, inventory_x, inventory_y, square, font)

        # Draws shop
        draw_shop(shop_items, screen, BLACK, shop_x, shop_y, square, font)
        
        # Draws instruction button
        chernobyl_adventures.draw_instruction_button(screen, BLACK, WHITE, instruction_x, instruction_y, instruction_button_width, instruction_button_height, font)

        # Draws sortie button
        draw_sortie_button(screen, BLACK, WHITE, sortie_x, sortie_y, button_width, button_height, font)

        # Draws exit button
        chernobyl_adventures.draw_exit_button(screen, BLACK, WHITE, exit_x, exit_y, button_width, button_height, font)

        # Draws item instructions
        draw_item_instructions(screen, instruction_font, BLACK)

        # Draws instructions and instruction box if clicked
        if instructions == True:
            chernobyl_adventures.draw_instructions(screen, DARKGREY, instruction_font, BLACK)

        # Blits player money
        text = font.render("Rubles: " + str(player_inventory.rubles), True, BLACK)
        screen.blit(text, [80, 558])

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()




