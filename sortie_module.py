import pygame
from sprite_strip_anim import SpriteStripAnim
import random
import shop_module
import chernobyl_adventures


class MapObject:
    """Class of objects that have an image a type and xy coords"""
    def __init__(self):
        self.image = 0
        self.type = 0
        self.x = 0
        self.y = 370

    def draw(self, screen):
        """Draw the object"""
        screen.blit(self.image, [self.x, self.y])


def create_random_object():
    """Creates random instances of Object"""
    image_list = image_block("images/objects.png", 128, 128, 2, -1)
    random_index = random.randint(0, len(image_list) - 1)
    map_object = MapObject()
    map_object.image = image_list[random_index]
    map_object.type = random_index
    return map_object


def image_block(filename, width, height, count, color_key):
    """Loads and appends images"""
    sprite_list = []
    for i in range(count):
        blocks = SpriteStripAnim(filename, (0 + width * i, 0, width, height), count, color_key)
        sprite_image = blocks.next()
        sprite_list.append(sprite_image)
    return sprite_list


def draw_ablities(screen, BLACK, ability_x, square, ability_y, font):
    """Draws ability boxes and logo's"""
    abilities = []
    for row in range(2):
        ability = pygame.draw.rect(screen, BLACK, [ability_x + square * row, ability_y, square, square], 2)  # Grid for abilities
        abilities.append(ability)
    text = font.render('ABILITIES', True, BLACK)
    screen.blit(text, [ability_x, ability_y - 20])
    ability1 = pygame.image.load('images/attack_logo.png').convert() 
    ability2 = pygame.image.load('images/heal_logo.png').convert()

    screen.blit(ability1, [281, 530])
    screen.blit(ability2, [329, 530])
    return abilities


def draw_player_stats(screen, font, BLACK, player_stat_x, player_stat_y, character):
    """Draws the players stats when clicked on"""
    
    screen.blit(font.render("Player Stats ", True, BLACK), [player_stat_x, player_stat_y])
    screen.blit(font.render("Name: " + character.name, True, BLACK), [player_stat_x, player_stat_y + 30])
    screen.blit(font.render("Health: " + str(character.health) + " / " + str(character.max_health), True, BLACK), [player_stat_x, player_stat_y + 60])
    screen.blit(font.render("Dodge: " + str(character.dodge), True, BLACK), [player_stat_x, player_stat_y + 90])
    screen.blit(font.render("Damage: " + str(character.minimum_damage) + " - " + str(character.maximum_damage), True, BLACK), [player_stat_x, player_stat_y + 120])


def draw_enemy_stats(screen, font, BLACK, enemy_stat_x, enemy_stat_y, enemies, enemy_clicked):
    """Draws the enemy stats when clicked on"""

    screen.blit(font.render("Enemy Stats ", True, BLACK), [enemy_stat_x, enemy_stat_y])
    screen.blit(font.render("Name: " + enemies.name, True, BLACK), [enemy_stat_x, enemy_stat_y + 30])
    screen.blit(font.render("Health: " + str(enemies.health) + " / " + str(enemies.max_health), True, BLACK), [enemy_stat_x, enemy_stat_y + 60])
    screen.blit(font.render("Dodge: " + str(enemies.dodge), True, BLACK), [enemy_stat_x, enemy_stat_y + 90])
    screen.blit(font.render("Damage: " + str(enemies.minimum_damage) + " - " + str(enemies.maximum_damage), True, BLACK), [enemy_stat_x, enemy_stat_y + 120])

    
def draw_background(background_list, screen, x, background, battle_boolean):
    """If conditions are met, draws background"""
    if x % 1280 == 0 and x != 0 and battle_boolean is False:
            background_list.append(background[random.randrange(2)])
    for i in range(len(background_list)):
        screen.blit(background_list[i], [x + 1280 * i, 0])


def character_select(character_list, mouse, selected_character):
    """Determines if mouse is within given boundaries"""
    for i in range(4):
        if character_list[i].x < mouse[0] < character_list[i].x + 128 and character_list[i].y < mouse[1] < character_list[i].y + 128:
            return i
    return selected_character


def enemy_select(enemy_list, mouse, selected_enemy):
    """Determines if mouse is within given boundaries"""
    for i in range(len(enemy_list)):
        if enemy_list[i].health > 0:
            if enemy_list[i].x < mouse[0] < enemy_list[i].x + 128 and enemy_list[i].y < mouse[1] < enemy_list[i].y + 128:
                return i
    return selected_enemy


def draw_gameover(screen, BLACK, RED, large_font):
    """Draws gameover screen"""
    screen.fill(BLACK)
    screen.blit(large_font.render("GAME OVER", True, RED), [470, 320])


def draw_victory(screen, BLACK, YELLOW, large_font):
    """Draws victory screen"""
    screen.fill(BLACK)
    screen.blit(large_font.render("VICTORY", True, YELLOW), [510, 320])


def use_item(x_pos, y_pos, mouse, square, inventory, shop_items):
    """Removes item and adds item price to money"""
    # Calculates the grid
    grid_column = shop_module.grid_find(x_pos, mouse[0], square)
    grid_row = shop_module.grid_find(y_pos, mouse[1], square)

    # If click is within inventory boundaries
    if 0 <= grid_row <= 2 and 0 <= grid_column <= 3:
        # If selected box has an item
        if inventory.inventory[grid_row][grid_column] != 0:
            # determines what item is in the spot and returns its index
            for i in range(4):
                if inventory.inventory[grid_row][grid_column] == shop_items[i]:
                    return i
        return None


def damage(target, attacker):
    """Calculates damage and dodge chance"""
    
    dodge_chance = random.randrange(0, 100)

    # target gets grazed
    if target.dodge > dodge_chance:
        damage = 1
    # If attacker wins the coin toss
    else:
        damage = random.randrange(attacker.minimum_damage, attacker.maximum_damage)
    return damage


def def_enemy(level):
    """Defines the enemy and their stats depending on the level"""
    
    # List of enemies to be drawn
    enemies = []  

    # First level, 2 dogs
    if level == 1:
        for i in range(2):
            dog = shop_module.Character()
            dog.name = "Dog"
            dog.dodge = random.randrange(30, 40)
            dog.max_health = random.randrange(10, 15)
            dog.health = dog.max_health
            dog.minimum_damage = random.randrange(4, 7)
            dog.maximum_damage = random.randrange(7, 8)
            dog.grid = SpriteStripAnim('images/enemysprites.png', (0, 0, 128, 128), 1, -1)
            dog.image = dog.grid.next()
            dog.x = 800 + 150 * i
            dog.y = 310
            dog.turn = False
            enemies.append(dog)
        return enemies
    # Second level, 2 bandits
    elif level == 2:
        for i in range(2):
            bandit = shop_module.Character()
            bandit.name = "Bandit"
            bandit.dodge = random.randrange(20, 40)
            bandit.max_health = random.randrange(20, 30)
            bandit.health = bandit.max_health
            bandit.minimum_damage = random.randrange(6, 8)
            bandit.maximum_damage = random.randrange(8, 10)
            bandit.grid = SpriteStripAnim('images/enemysprites.png', (128, 0, 128, 128), 1, -1)
            bandit.image = bandit.grid.next()
            bandit.x = 800 + 150 * i
            bandit.y = 310
            bandit.turn = False
            enemies.append(bandit)
        return enemies
    # Third level, 2 bandit leaders
    elif level == 3:
        for i in range(2):
            bandit_leader = shop_module.Character()
            bandit_leader.name = "Bandit Leader"
            bandit_leader.dodge = random.randrange(25, 45)
            bandit_leader.max_health = random.randrange(22, 32)
            bandit_leader.health = bandit_leader.max_health
            bandit_leader.minimum_damage = random.randrange(6, 8)
            bandit_leader.maximum_damage = random.randrange(8, 9)
            bandit_leader.grid = SpriteStripAnim('images/enemysprites.png', (256, 0, 128, 128), 1, -1)
            bandit_leader.image = bandit_leader.grid.next()
            bandit_leader.x = 800 + 150 * i
            bandit_leader.y = 310
            bandit_leader.turn = False
            enemies.append(bandit_leader)
        return enemies
    # Fourty level, 4 dogs
    elif level == 4:
        for i in range(4):
            dog = shop_module.Character()
            dog.name = "Dog"
            dog.dodge = random.randrange(40, 60)
            dog.max_health = random.randrange(12, 15)
            dog.health = dog.max_health
            dog.minimum_damage = random.randrange(1, 2)
            dog.maximum_damage = random.randrange(2, 4)
            dog.grid = SpriteStripAnim('images/enemysprites.png', (0, 0, 128, 128), 1, -1)
            dog.image = dog.grid.next()
            dog.x = 700 + 140 * i
            dog.y = 310
            dog.turn = False
            enemies.append(dog)
        return enemies
    #  Fifth level, 2 bandit leaders and 2 dogs
    elif level == 5:
        for i in range(2):
            bandit_leader = shop_module.Character()
            bandit_leader.name = "Bandit Leader"
            bandit_leader.dodge = random.randrange(25, 35)
            bandit_leader.max_health = random.randrange(20, 31)
            bandit_leader.health = bandit_leader.max_health
            bandit_leader.minimum_damage = random.randrange(5, 7)
            bandit_leader.maximum_damage = random.randrange(7, 9)
            bandit_leader.grid = SpriteStripAnim('images/enemysprites.png', (256, 0, 128, 128), 1, -1)
            bandit_leader.image = bandit_leader.grid.next()
            bandit_leader.x = 900 + 128 * i
            bandit_leader.y = 310
            bandit_leader.turn = False

            dog = shop_module.Character()
            dog.name = "Dog"
            dog.dodge = random.randrange(30, 40)
            dog.max_health = random.randrange(10, 16)
            dog.health = dog.max_health
            dog.minimum_damage = random.randrange(2, 4)
            dog.maximum_damage = random.randrange(4, 6)
            dog.grid = SpriteStripAnim('images/enemysprites.png', (0, 0, 128, 128), 1, -1)
            dog.image = dog.grid.next()
            dog.x = 650 + 128 * i
            dog.y = 310
            dog.turn = False
            enemies.append(bandit_leader)
            enemies.append(dog)
        return enemies
    # Final level, 1 boss
    elif level == 6:
        for i in range(1):
            boss = shop_module.Character()
            boss.name = "Boss"
            boss.dodge = random.randrange(35, 60)
            boss.max_health = random.randrange(70, 100)
            boss.health = boss.max_health
            boss.minimum_damage = random.randrange(11, 13)
            boss.maximum_damage = random.randrange(13, 25)
            boss.grid = SpriteStripAnim('images/enemysprites.png', (384, 0, 128, 128), 1, -1)
            boss.image = boss.grid.next()
            boss.x = 1100
            boss.y = 310
            boss.turn = False
            enemies.append(boss)
        return enemies            
    
    
def remove_inventory_item(x_pos, y_pos, mouse, square, inventory):
    """Removes item from inventory"""
    
    # Calculates grid
    grid_column = shop_module.grid_find(x_pos, mouse[0], square)
    grid_row = shop_module.grid_find(y_pos, mouse[1], square)

    # If click is within inventory boundaries
    if 0 <= grid_row <= 2 and 0 <= grid_column <= 3:
        # If selected box has an item
        if inventory.inventory[grid_row][grid_column] != 0:
            # removes item
            inventory.remove_item(grid_row, grid_column)
            return inventory
    return inventory


def player_attack(enemy, player):
    """Calls function to calculate damage, subtracts from enemies health, and sets timer for damage text"""
    
    char_damage_value = damage(enemy, player)
    enemy.health -= char_damage_value
    enemy.damage_taken -= char_damage_value
    enemy.time_to_blit = pygame.time.get_ticks() + 2000
    return enemy


def player_heal(player):
    """Heals player, uses a turn, sets timer for heal text"""
    
    heal_value = 4
    if player.health + heal_value >= player.max_health:
        player.health = player.max_health
    else:
        player.health += heal_value
    ability_heal = False
    player.time_to_blit = pygame.time.get_ticks() + 2000
    player.damage_taken = heal_value
    player.turn = True
    return player


def sortie(player_inventory, shop_items, character_list):
    """Handles battles, traps, treasures, HUDs"""

    # it's the move speed (i didn't know that)
    MOVESPEED = 10

    # Frames/Clock
    FPS = 60
    clock = pygame.time.Clock()

    # Defining colors
    GREY = (211, 211, 211)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255,0,0)
    YELLOW = (255, 255, 0)
    
    # Screen size
    SIZE = (1280, 730)
    screen = pygame.display.set_mode(SIZE)

    # ends loop if true
    done = False
    
    # index of character selected
    selected_character = 0

    # Selected Enemy
    selected_enemy = 0

    # Creates 5 objects and puts them in a list
    object_num = 5
    object_list = []
    for i in range(object_num):
        object_element = create_random_object()
        object_list.append(object_element)

    # object you are passing
    object_counter = 0
    
    # Image of background
    background = image_block('images/background2.png', 1280, 730, 2, None)

    # List of background images
    background_list = [background[0], background[1]]

    # Sets up anti-aliasing, font and sizes
    font = pygame.font.SysFont('Calibri', 18, True, False)
    large_font = pygame.font.SysFont('Calibri', 72, True, True)
    
    # Background position
    x = 0
    
    # Coordinates of inventory box
    inventory_x = 500
    inventory_y = 530

    # Value of square
    square = 48
    
    # Coordinates of player stats
    player_stat_x = 30
    player_stat_y = 510
    
    # Coordinates of enemy stats 
    enemy_stat_x = 850
    enemy_stat_y = 510

    # Coordinates of the ability rectangle
    ability_x = 280
    ability_y = 530

    # Level counter
    level = 1

    # battle boolean
    battle_boolean = False

    # player ability booleans
    ability_damage = False
    ability_heal = False

    # Enemy list gets defined
    enemy_list = def_enemy(level)

    # Boolean for moving
    move = True

    # Boolean used to stop player from going out of bounds
    left = True
    
    # Boolean for radiation prevention
    rad_proof = False

    # sustain timer for blitting enemy turn text
    time_to_blit_enemy = None

    # sustain timer for blitting game over screen
    time_to_end = None

    # sustain timer for blitting win screen
    time_to_win = None
    
    # Sounds
    dog_attack_sound = pygame.mixer.Sound("sounds/dog_attack.ogg")

    # CS:GO death sound
    death_sound = pygame.mixer.Sound("sounds/death_sound.ogg")

    # https://www.youtube.com/watch?v=iutuQbMAx04&t source
    radiation_sound = pygame.mixer.Sound("sounds/radiation.ogg")

    # Darkest Dungeon music
    combat_music = pygame.mixer.Sound("sounds/combat_music.ogg")

    # Darkest Dungeon sound effect
    attack_sound = pygame.mixer.Sound("sounds/gunshot.ogg")

    # Darkest Dungeon music
    boss_music = pygame.mixer.Sound("sounds/boss_music.ogg")

    # Wilhelm scream
    enemy_death_sound = pygame.mixer.Sound("sounds/enemy_death_sound.ogg")###

    # i dont remember the source
    dog_death_sound = pygame.mixer.Sound("sounds/dog_death_sound.ogg")###

    # Stalker sound effect and knife combined in audacity
    boss_attack = pygame.mixer.Sound("sounds/boss_attack.ogg")

    # Stalker sound effect
    game_over_music = pygame.mixer.Sound("sounds/game_over_music.ogg")

    # Stalker sound effect
    boss_death_sound = pygame.mixer.Sound("sounds/boss_death_sound.ogg")

    # https://www.youtube.com/watch?v=jta2yE8qLQw
    heal_sound = pygame.mixer.Sound("sounds/heal_sound.ogg")

    # rainbow six siege sound
    adrenaline_sound = pygame.mixer.Sound("sounds/adrenaline_sound.ogg")

    # https: // www.youtube.com / watch?v = afA8N8vEWG4
    antirad_sound = pygame.mixer.Sound("sounds/antirad_sound.ogg")

    # https: // www.youtube.com / watch?v = NJbZ2thxCaI
    treasure_sound = pygame.mixer.Sound("sounds/treasure_sound.ogg")

    # https: // www.youtube.com / watch?v = zZmc84ldPyY
    vodka_sound = pygame.mixer.Sound("sounds/vodka_sound.ogg")

    # Allows music to be played once inside a loop
    music = True

    # Helps run game over once
    run_once = 0

    # Helps uns the boss end game part once
    run_once2 = 0

    while not done:
        # --- Main event loop --- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # Gets mouse pos
                mouse = pygame.mouse.get_pos()
                
                # Deletes item if used 
                used_item = use_item(inventory_x, inventory_y, mouse, square, player_inventory, shop_items)
                
                # Inventory for game
                player_inventory = remove_inventory_item(inventory_x, inventory_y, mouse, square, player_inventory)

                # Checks if character is clicked and which character is clicked
                selected_character = character_select(character_list, mouse, selected_character)

                # Checks if enemy is clicked and which enemy is clicked
                selected_enemy = enemy_select(enemy_list, mouse, selected_enemy)

                # If attack is selected
                ability_damage = chernobyl_adventures.button_click(ability_x, ability_y, mouse, square, square)

                # If heal is selected
                ability_heal = chernobyl_adventures.button_click(ability_x + square, ability_y, mouse, square, square)

                # Checks which item is used
                if used_item != None:
                    # Protects from radiation damage
                    if used_item == 0:
                        rad_proof = True
                        antirad_sound.play()
                    # Buffs player attack
                    elif used_item == 1:
                        character_list[selected_character].maximum_damage += 2
                        adrenaline_sound.play()
                    # Buffs player dodge chance
                    elif used_item == 2:
                        character_list[selected_character].dodge += 4
                        vodka_sound.play()
                    # Heals selected player
                    elif used_item == 3:
                        if character_list[selected_character].health + 4 < character_list[selected_character].max_health:
                            character_list[selected_character].health += 4
                        else:
                            character_list[selected_character].health = character_list[selected_character].max_health
                        heal_sound.play()

        # Code for keyboard movement
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and move is True:
            x -= MOVESPEED
        elif key[pygame.K_a] and move is True and left == True:
            x += MOVESPEED
        else:
            # stops animation
            for i in range(len(character_list)):
                character_list[i].image = character_list[i].grid.stop()

        # map movement border
        if x > 0:
            left = False
        else:
            left = True

        # Background Image
        draw_background(background_list, screen, x, background, battle_boolean)
        for i in range(len(object_list)):
            object_list[i].x = x + 500 + 1280 * i
            object_list[i].draw(screen)

        # Prevents index size from creating an error
        if object_counter <= object_num - 1:
            # If next object passes player
            if object_list[object_counter].x <= character_list[3].x:
                # If object is treasure
                if object_list[object_counter].type == 0:
                    player_inventory.add_item(random.choice(shop_items))
                    treasure_sound.play()
                # If object is a trap
                elif object_list[object_counter].type == 1:
                    # If player is not immune
                    if rad_proof is False:
                        for i in range(len(character_list)):
                            character_list[i].health -= 2
                        radiation_sound.play()

                # Next object
                object_counter += 1

        # Drawing Hud
        pygame.draw.rect(screen, GREY, [0, 500, 1280, 600], 0)  # Sets up bottom rectangle that has the hud
        pygame.draw.line(screen, BLACK, [800, 500], [800, 730], 3)  # Line that seperates player stats and inventory from enemy stats

        # Draw inventory
        shop_module.draw_inventory(player_inventory, screen, BLACK, WHITE, inventory_x, inventory_y, square, font)

        # Draw abilities
        draw_ablities(screen, BLACK, ability_x, square, ability_y, font)

        # Blit rubles onto screen
        text = font.render("Rubles: " + str(player_inventory.rubles), True, BLACK)
        screen.blit(text, [375, 590])

        # Displays levels at the top left corner
        level_text = font.render("Level: " + str(level) + " / 6", True, BLACK)
        screen.blit(level_text, [5, 5])

        # Draws player stat and box around player if they arent dead
        if character_list[selected_character].health > 0:
            draw_player_stats(screen, font, BLACK, player_stat_x, player_stat_y, character_list[selected_character])
            pygame.draw.rect(screen, BLACK, [character_list[selected_character].x, character_list[selected_character].y, 128, 128], 2)

        # If player reaches a certain point, draw enemy and start the battle sequence
        if x == -1280 * level:
            # draw stats and target rectangle
      
            if enemy_list[selected_enemy].health > 0:
                draw_enemy_stats(screen, font, BLACK, enemy_stat_x, enemy_stat_y, enemy_list[selected_enemy], selected_enemy)
                pygame.draw.rect(screen, BLACK, [enemy_list[selected_enemy].x, enemy_list[selected_enemy].y, 128, 128], 2)

            # prevents map from doing wierd things
            battle_boolean = True

            # if boss level, use boss music
            if level == 6:
                if music is True:
                    boss_music.play()
                    music = False
            # if regular level, use combat music
            else:
                if music is True:
                    combat_music.play()
                    music = False
                
            # Stops movement 
            move = False

            # Damages seleced enemy or heals selected character
            if ability_damage is True and character_list[selected_character].turn is False:
                # player does damage to enemy and uses turn
                enemy_list[selected_enemy] = player_attack(enemy_list[selected_enemy], character_list[selected_character])
                ability_damage = False
                character_list[selected_character].turn = True
                attack_sound.play()
            elif ability_heal is True and character_list[selected_character].turn is False:
                # player heals self and uses turn
                character_list[selected_character] = player_heal(character_list[selected_character])
                heal_sound.play()

            # if the enemy being targeted dies, switch to another enemy
            if enemy_list[selected_enemy].health < 0:
                for i in range(len(enemy_list)):
                    if enemy_list[i].health > 0:
                        selected_enemy = i
                        break
            # checks if all players have used their turns
            enemy_turn = True
            for i in range(len(character_list)):
                if character_list[i].turn is False:
                    enemy_turn = False

            # Checks if all enemies are alive
            enemies_alive = False
            for i in range(len(enemy_list)):
                if enemy_list[i].health > 0:
                    enemies_alive = True

            # If all player turns are used, and enemies alive, enemies attack
            if enemy_turn is True and enemies_alive is True:
                # List of characters health
                character_health_list = [character_list[0].health, character_list[1].health, character_list[2].health, character_list[3].health]

                # checks if all players are dead
                all_characters_dead = True
                for i in range(len(character_list)):
                    if character_list[i].health > 0:
                        lowest_health = min(i for i in character_health_list if i > 0)  # Looks for the index of the lowest health
                        all_characters_dead = False

                # Damage that the enemy does
                damage_combined = 0
                if all_characters_dead is False:
                    # all enemies try to attack
                    for i in range(len(enemy_list)):
                        # if enemy is alive, attack
                        if enemy_list[i].health > 0:
                            # prioritizes lowest health player
                            lowest_health_char = character_health_list.index(lowest_health)
                            enemy_target = lowest_health_char
                            # enemy calculates damage
                            enem_damage_value = damage(character_list[enemy_target], enemy_list[i])
                            character_list[enemy_target].health -= enem_damage_value
                            # total damage on target
                            damage_combined -= enem_damage_value
                            # sends the total damage and the timer to be drawn
                            character_list[enemy_target].damage_taken = damage_combined
                            character_list[enemy_target].time_to_blit = pygame.time.get_ticks() + 2000

                        # enemy attack sounds for all levels
                        if level == 1:
                            dog_attack_sound.play()
                        elif level == 2:
                            attack_sound.play()
                        elif level == 3:
                            attack_sound.play()
                        elif level == 4:
                            dog_attack_sound.play()
                        elif level == 5:
                            attack_sound.play()
                            dog_attack_sound.play()
                        elif level == 6:
                            boss_attack.play()
                    # 4 second sustain timer for enemy turn text
                    time_to_blit_enemy = pygame.time.get_ticks() + 4000

                # resets player turns
                for i in range(4):
                    character_list[i].turn = False

            # blits text for 4 seconds
            if time_to_blit_enemy:
                screen.blit(font.render("THE ENEMY HAS MADE THEIR MOVE!", True, BLACK), [560, 50])
                if pygame.time.get_ticks() >= time_to_blit_enemy:
                    time_to_blit_enemy = None
                    
            # check enemies
            for i in range(len(enemy_list)):
                # if enemy hp is below zero
                if enemy_list[i].health <= 0:
                    # if enemy wasn't already dead
                    if enemy_list[i].dead is False:
                        enemy_list[i].dead = True
                        # death sounds for each level
                        if level == 1 or level == 4:
                            dog_death_sound.play()
                        elif level == 2 or level == 3:
                            enemy_death_sound.play()
                        elif level == 5:
                            if enemy_list[i].name == "Dog":
                                dog_death_sound.play()
                            else:
                                enemy_death_sound.play()
                        elif level == 6:
                            boss_death_sound.play()


            # Blitting enemy
            for i in range(len(enemy_list)):
                enemy_list[i].draw(screen, font, BLACK)
            
            # Checks if there are enemies still alive
            end_battle = True
            for i in range(len(enemy_list)):
                if enemy_list[i].dead is False:
                    end_battle = False

            # Checks if battle is over and progresses level and enemies
            if end_battle is True:
                # if it is not boss level
                if level != 6:
                    x -= MOVESPEED
                    combat_music.stop()
                    for i in range(len(character_list)):
                        character_list[i].turn = False
                    level += 1
                    battle_boolean = False
                    enemy_list = def_enemy(level)
                    move = True
                    music = True
                    player_inventory.add_item(random.choice(shop_items))
                    player_inventory.rubles += 250
                # if it is boss battle and hasn't been run yet
                elif level == 6 and run_once2 == 0:
                    boss_music.stop()
                    player_inventory.add_item(random.choice(shop_items))
                    player_inventory.rubles += 750
                    time_to_win = pygame.time.get_ticks() + 8000
                    run_once2 += 1
                selected_enemy = 0

        # Displays rad proof buff
        if rad_proof is True:
            screen.blit(shop_items[0].image, [290, 600])

        # Blits player onto surfaced
        for i in range(4):
            # if players health is below 0
            if character_list[i].health <= 0:
                character_list[i].turn = True
                # if player character wasn't already dead
                if character_list[i].dead is False:
                    character_list[i].dead = True
                    death_sound.play()

            # Draws the players and animates them
            character_list[i].draw(screen, font, BLACK, battle_boolean, True)
            character_list[i].image = character_list[i].grid.next()

        # If all characters are dead, returns to shop
        game_is_over = True
        for i in range(len(character_list)):
            if character_list[i].health > 0:
                game_is_over = False

        # if the game is over and hasn't been run yet
        if game_is_over is True and run_once == 0:
            time_to_end = pygame.time.get_ticks() + 8000
            game_over_music.play()
            run_once += 1

        # displays game over screen for 8 seconds then returns to splashscreen
        if time_to_end:
            draw_gameover(screen, BLACK, RED, large_font)
            if pygame.time.get_ticks() >= time_to_end:
                combat_music.stop()
                if level == 6:
                    boss_music.stop()
                chernobyl_adventures.main()

        # displays victory screen for 8 seconds then returns to shop
        elif time_to_win:
            draw_victory(screen, BLACK, YELLOW, large_font)
            if pygame.time.get_ticks() >= time_to_win:
                done = True

        # Updates display
        pygame.display.update()

        clock.tick(FPS)
