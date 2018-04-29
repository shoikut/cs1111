# Sean Reihani, sr9gv
# Abdullah Mahmood, aam2vp

import pygame
import gamebox
import random

"""
This will be a "bullet hell" game, with a rescue the princess element.
The player will battle enemies in different levels of the world,
collecting power-ups while avoiding losing all of his health.

After beating all levels, the player will be able to face the boss level,
containing the hardest enemy with a lot of health and different 
attack styles.

User input will require usage of the WASD keys to move and a the spacebar to fire arrows at enemies.

Possible optional features: 
- Possibly using animations for projectiles, animations for characters
    when the characters are at rest, moving, or attacking
- Collectibles to possibly increase attack damage, attacks per second,
    health, shields
- Health meter to show how many hits the player can take before dying
    and having the game reset
- Multiple levels of different difficulty enemies with different attack
    patterns and health
"""

cam = gamebox.Camera(800, 600)
title_text = [
    gamebox.from_text(400, 150, "THE ADVENTURE OF LORENZO", 70, 'yellow'),
    gamebox.from_text(400, 215, "Abdullah Mahmood, aam2vp", 20, "firebrick"),
    gamebox.from_text(400, 235, "Sean Reihani, sr9gv", 20, "firebrick"),
    gamebox.from_text(400, 300, "Welcome to The Adventure of Lorenzo! The goal of this game is to rescue the beautiful ", 25, 'white'),
    gamebox.from_text(400, 315, "princess Theresa Sullivan. The game consists of three levels. To rescue the princess,", 25, 'white'),
    gamebox.from_text(400, 330, "you must defeat the boss at the end of each level. The overworld is crawling with ", 25, 'white'),
    gamebox.from_text(400, 345, "enemies. When defeated, these enemies drop coins that make you stronger, ", 25, 'white'),
    gamebox.from_text(400, 360, "which might make boss battles easier. Best of luck, Ser Lorenzo!", 25, 'white'),
    gamebox.from_text(400, 385, "Optional Elements: Animation, Enemies, Collectibles, Health, Multiple Levels", 25, 'white'),
    gamebox.from_text(400, 435, "PRESS SPACE TO BEGIN", 30, 'blue')
]

horizontal_arrows = [gamebox.from_color(-300, 300, 'brown', 25, 8)]  # arrows fired when character fires left/right
vertical_arrows = [gamebox.from_color(-300, 300, 'brown', 8, 25)]  # arrows fired when character fires left/right

character = gamebox.from_color(300, 200, 'green', 25, 25)

# starting position for first enemy
enemy_x = character.x
enemy_y = character.y - 200
enemies = [gamebox.from_color(enemy_x, enemy_y, 'red', 30, 30)]
enemy_count = 9     # draws four more random enemies in addition to the preset one

boulders = []  # creates "boulders" so player can notice movement

while len(boulders) < 175:
    boulders.append(
        gamebox.from_color(
            random.randint(-1600, 1601), random.randint(-1600, 1601), 'grey', 30, 30))

direction = "forward"  # sets direction variable for shooting
cool_down = 0  # initializes cool_down timer variable

title_screen_on = True
level1_on = False
level2_on = False
level3_on = False
final_level_on = False
health_level = 100
boss_health_level = 100


# Health function
def health():
    global health_level
    return gamebox.from_color(cam.left + (400 * health_level / 100), cam.bottom - 15, "green", (800 * health_level / 100), 30)

# Boss health function
def boss_health():
    global boss_health_level
    return gamebox.from_color(cam.left + (400 * boss_health_level / 100), cam.top + 15, "red", (800 * boss_health_level / 100), 30)

# Draws a title screen
def title_screen():
    cam.clear('black')
    for text in title_text:
        cam.draw(text)
    cam.display()

def control(keys):
    #  Character movement and shooting direction
    global cool_down
    global direction

    if pygame.K_a in keys:
        direction = "left"
        character.x -= 4
    if pygame.K_d in keys:
        direction = "right"
        character.x += 4
    if pygame.K_w in keys:
        direction = "up"
        character.y -= 4
    if pygame.K_s in keys:
        direction = "down"
        character.y += 4
    if pygame.K_SPACE in keys and cool_down == 0:
        horizontal_arrows.append(
            gamebox.from_color(-300, 300, 'brown', 25, 8),
        )
        vertical_arrows.append(
            gamebox.from_color(-300, 300, 'brown', 8, 25),
        )

        if direction == "left":
            horizontal_arrows[-1].speedx = -10
            horizontal_arrows[-1].center = character.center
            keys.remove(pygame.K_SPACE)

        elif direction == "right":
            horizontal_arrows[-1].speedx = 10
            horizontal_arrows[-1].center = character.center
            keys.remove(pygame.K_SPACE)

        elif direction == "up":
            vertical_arrows[-1].speedy = -10
            vertical_arrows[-1].center = character.center
            keys.remove(pygame.K_SPACE)

        elif direction == "down":
            vertical_arrows[-1].speedy = 10
            vertical_arrows[-1].center = character.center
            keys.remove(pygame.K_SPACE)

        cool_down = 60  # sets a one second cool down timer on arrows


    # moves arrows, gives them a range
    for arrow in horizontal_arrows:
        arrow.move_speed()
        if abs(character.x - arrow.x) > 200:
            horizontal_arrows.remove(arrow)

    for arrow in vertical_arrows:
        arrow.move_speed()
        if abs(character.y - arrow.y) > 200:
            vertical_arrows.remove(arrow)

    if cool_down > 0:
        cool_down -= 1

    # Camera follows player
    cam.x = character.x
    cam.y = character.y

# This function controls the melee enemies
def monsters():
    global enemy_count, health_level, on_level
    if enemy_count > 0:
        enemy_x = character.x + random.randrange(-750, 751)
        enemy_y = character.y + random.randrange(-750, 751)
        enemies.append(gamebox.from_color(enemy_x, enemy_y, 'red', 30, 30))
        for enemy in enemies:
            cam.draw(enemy)
            cam.display()
        enemy_count -= 1


    # Enemy attacks player if within certain distance
    for enemy in enemies:
        if abs(enemy.x - character.x) < 300 and abs(enemy.y - character.y) < 300:
            if character.x > enemy.x:
                enemy.x += 3
            elif character.x < enemy.x:
                enemy.x -= 3

            if character.y < enemy.y:
                enemy.y -= 3
            elif character.y > enemy.y:
                enemy.y += 3

    for enemy in enemies:
        for arrow in horizontal_arrows:
            if arrow.touches(enemy):
                enemies.remove(enemy)
                horizontal_arrows.remove(arrow)
                if len(enemies) <= 0:
                    on_level = "final"
                    character.x = 400
                    character.y = 500
        for arrow in vertical_arrows:
            if arrow.touches(enemy):
                enemies.remove(enemy)
                vertical_arrows.remove(arrow)
                if len(enemies) <= 0:
                    on_level = "final"
                    character.x = 400
                    character.y = 500
        if enemy.touches(character):
            if enemy.x > character.x:
                character.x -= 50
            elif enemy.x < character.x:
                character.x += 50
            if enemy.y > character.y:
                character.y -= 50
            elif enemy.y < character.y:
                character.y += 50
            health_level -= 5

    if health_level <= 0:
        health()
        cam.draw("Game Over!", 120, 'red', 385, 300)
        cam.display()
        gamebox.pause()

    print(len(enemies))


# game world
def level1(keys):
    global cam, cool_down, direction, enemy_count, enemy_x, enemy_y, health_level, on_level

    cam.clear('tan')

    for boulder in boulders:
        cam.draw(boulder)
    cam.draw(character)
    for enemy in enemies:
        cam.draw(enemy)

    for arrow in horizontal_arrows:
        cam.draw(arrow)
    for arrow in vertical_arrows:
        cam.draw(arrow)

    cam.draw(health())

    cam.display()

    control(keys)
    monsters()


def final_level(keys):
    global character
    cam.clear("black")
    cam.draw(health())
    cam.draw(boss_health())
    cam.draw(character)
    cam.draw(gamebox.from_text(character.x, character.y, "BOSS LEVEL: TO BE DEVELOPED", 50, "red"))

    cam.display()


on_level = 0


def tick(keys):
    global on_level, title_screen_on, level1_on, level2_on, level3_on, final_level_on
    if pygame.K_SPACE in keys and on_level == 0:
        on_level = 1
        keys.remove(pygame.K_SPACE)

    if on_level == 1:  # Game begins after space is pressed
        title_screen_on = False
        level1(keys)

    if on_level == "final":
        final_level(keys)

    if title_screen_on:
        title_screen()


ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)