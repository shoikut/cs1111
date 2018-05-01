# Sean Reihani, sr9gv
# Abdullah Mahmood, aam2vp

import pygame, gamebox, random, math

"""
After beating the first two levels, the player will be able to face the boss level,
containing the hardest enemy with a lot of health and different 
attack styles.

User input will require usage of the WASD keys to move and a the spacebar to fire arrows at enemies.

Optional features:
-Enemies
-Scrolling level
-Health Meter
-Multiple Levels


Image Sources:

Rocks: https://openclipart.org/detail/209758/harvestable-resources-rock
Trees: https://openclipart.org/detail/9491/rpg-map-symbols-deserted-tree
Character Sprites (edited): http://goldenhylian.tripod.com/l2plink.gif
Goblin: https://openclipart.org/detail/65551/goblin-warrior
Torch: https://opengameart.org/content/animated-torch

"""

cam = gamebox.Camera(800, 600)
title_text = [
    gamebox.from_text(400, 150, "THE ADVENTURE OF LORENZO", 70, 'yellow'),
    gamebox.from_text(400, 215, "Abdullah Mahmood, aam2vp", 20, "firebrick"),
    gamebox.from_text(400, 235, "Sean Reihani, sr9gv", 20, "firebrick"),
    gamebox.from_text(400, 300, "Welcome to The Adventure of Lorenzo! The goal of this game is to rescue the beautiful ", 25, 'white'),
    gamebox.from_text(400, 315, "princess Theresa Sullivan. The game consists of three levels. To rescue the princess,", 25, 'white'),
    gamebox.from_text(400, 330, "you must clear each level and beat the boss level. The overworld is crawling with ", 25, 'white'),
    gamebox.from_text(400, 345, "enemies. When defeated, these enemies drop coins that make you stronger, ", 25, 'white'),
    gamebox.from_text(400, 360, "which might make boss battles easier. Best of luck, Ser Lorenzo!", 25, 'white'),
    gamebox.from_text(400, 385, "Optional Elements: Enemies, Scrolling level, Health, Multiple Levels", 25, 'white'),
    gamebox.from_text(400, 435, "PRESS SPACE TO BEGIN", 30, 'blue'),
    gamebox.from_text(400, 520, "CONTROLS: Use WASD to move and SPACE to shoot in the direction you are facing!", 25, "white"),
    gamebox.from_text(400, 540, "Cheat: Press ENTER  on level 1 to skip to the boss", 15, "white")
]
defeated_boss_text = [
    gamebox.from_text(400, 150, "CONGRATULATIONS, HERO", 50, "white"),
    gamebox.from_text(400, 200, "YOU HAVE DEFEATED THE EVIL GOBLIN KING!", 50, "white")
]

# Character info
character = gamebox.from_image(300, 200, "character_front.png")
character.scale_by(1.25)
cam_locked = True

# Boss and boss room info
boss = gamebox.from_image(400, 150, "goblin_king.png")
boss.scale_by(.25)

boss_room = gamebox.from_image(400, 300, "boss_room.png")
boss_room.scale_by(.78)

# generates arrows
horizontal_arrows = [gamebox.from_image(-30000, 30000, 'horizontal_arrow.png')]
vertical_arrows = [gamebox.from_image(-30000, 30000, 'vertical_arrow.png')]

# starting position for first enemy
enemy_x = character.x
enemy_y = character.y - 200
enemies = [gamebox.from_image(enemy_x, enemy_y, 'goblin.png')]

enemy_count = 9   # draws random enemies

# Level 1 environmental details
boulders = []  # creates boulders so player can notice movement
trees = []   # creates dead trees for desert level

# Level 2 environmental details
torches = []  # torch list
sheet = gamebox.load_sprite_sheet('torch.png', 2, 3)  # torch sprite sheet
sheet = [
    sheet[0],
    sheet[1],
    sheet[2],
    sheet[3],
    sheet[4],
    sheet[5],
]


while len(boulders) < 140:
    boulders.append(
        gamebox.from_image(
            random.randint(-1850, 1851),  random.randint(-1600, 1601),  'rock.png'))

while len(trees) < 85:
    trees.append(
        gamebox.from_image(
            random.randint(-1850, 1851),  random.randint(-1600, 1601),  'tree.png'))

while len(torches) < 50:
    torches.append(gamebox.from_image(random.randint(-1600, 1601), random.randint(-1600, 1601), sheet[0]))

direction = "forward"  # sets direction variable for shooting
cool_down = 0  # initializes cool_down timer variable

title_screen_on = True
level1_on = False
level2_on = False
final_level_on = False
health_level = 100
enemy_health = 1
boss_health_level = 100


# Health function
def health():
    global health_level
    return gamebox.from_color(cam.left + (400 * health_level / 100), cam.bottom - 15, "green", (800 * health_level / 100), 30)


# Boss health function
def boss_health():
    global boss_health_level
    return gamebox.from_color(cam.left + (400 * boss_health_level / 100), cam.top + 15, "red", (800 * boss_health_level / 100), 30)


# Boss attack projectiles and phases
daggers_up, daggers_down, daggers_left, daggers_right = [], [], [], []
# Saw attack going top-right, top-left, bottom-left, and bottom-right
saw_tr, saw_tl, saw_bl, saw_br = [], [], [], []


def boss_move(speed):
    if ticks > 60:
        if boss.x < character.x:
            boss.x += speed
        elif boss.x > character.x:
            boss.x -= speed
        if boss.y < character.y:
            boss.y += speed
        elif boss.y > character.y:
            boss.y -= speed


def dagger_attack():
    daggers_up.append(gamebox.from_image(boss.x, boss.y, "dagger_up.png"))
    daggers_down.append(gamebox.from_image(boss.x, boss.y, "dagger_down.png"))
    daggers_left.append(gamebox.from_image(boss.x, boss.y, "dagger_left.png"))
    daggers_right.append(gamebox.from_image(boss.x, boss.y, "dagger_right.png"))


def saw_attack():
    saw_tr.append(gamebox.from_image(boss.x, boss.y, "saw.png"))
    saw_tl.append(gamebox.from_image(boss.x, boss.y, "saw.png"))
    saw_bl.append(gamebox.from_image(boss.x, boss.y, "saw.png"))
    saw_br.append(gamebox.from_image(boss.x, boss.y, "saw.png"))
    saw_tr[-1].scale_by(.025), saw_tl[-1].scale_by(.025)
    saw_br[-1].scale_by(.025), saw_bl[-1].scale_by(.025)


def boss_attack1():
    if ticks % 120 == 0:
        dagger_attack()


def boss_attack2():
    if ticks % 60 == 0 or ticks % 60 == 10:
        saw_attack()


def boss_phase1():
    # Boss walks slowly towards player and shoots slow, medium damage projectiles
    boss_attack1()
    boss_move(.5)


def boss_phase2():
    # Move boss back to starting position
    if boss.x < 400:
        boss.x += .5
        if boss.x < 395:
            boss.x += 1.5
    elif boss.x > 400:
        boss.x -= .5
        if boss.x > 405:
            boss.x -= 1.5
    if boss.y < 150:
        boss.y += .5
        if boss.y < 145:
            boss.y += 1.5
    elif boss.y > 150:
        boss.y -= .5
        if boss.y > 155:
            boss.y -= 1.5

    if boss.x == 400 and boss.y == 150:
        boss_attack1()
        boss_attack2()


def boss_phase3():
    boss_attack1()
    boss_attack2()
    boss_move(1)

# def boss_phase2():
# Boss goes to a set position and starts firing waves of medium-high speed, low damage projectiles
# away from itself and fires the occasional slow, medium damage projectile


# def boss_phase3():
# Similar to phase 2, but now boss slowly moves toward player


# Draws a title screen
def title_screen():
    cam.clear('black')
    for text in title_text:
        cam.draw(text)
    cam.display()


def control(keys):
    #  Character movement and shooting direction
    global character, cool_down, direction, cam_locked

    if pygame.K_a in keys:
        character = gamebox.from_image(character.x, character.y, "character_left.png")
        character.scale_by(1.25)
        direction = "left"
        if pygame.K_s in keys and pygame.K_w in keys:
            character.x -= 4
        elif pygame.K_s in keys or pygame.K_w in keys:
            character.x -= math.sqrt(12)
        else:
            character.x -= 4

    if pygame.K_d in keys:
        character = gamebox.from_image(character.x, character.y, "character_right.png")
        character.scale_by(1.25)
        direction = "right"
        if pygame.K_s in keys and pygame.K_w in keys:
            character.x += 4
        elif pygame.K_s in keys or pygame.K_w in keys:
            character.x += math.sqrt(12)
        else:
            character.x += 4

    if pygame.K_w in keys:
        character = gamebox.from_image(character.x, character.y, "character_back.png")
        character.scale_by(1.25)
        direction = "up"
        if pygame.K_a in keys and pygame.K_d in keys:
            character.y -= 4
        elif pygame.K_a in keys or pygame.K_d in keys:
            character.y -= math.sqrt(12)
        else:
            character.y -= 4

    if pygame.K_s in keys:
        character = gamebox.from_image(character.x, character.y, "character_front.png")
        character.scale_by(1.25)
        direction = "down"
        if pygame.K_a in keys and pygame.K_d in keys:
            character.y += 4
        elif pygame.K_a in keys or pygame.K_d in keys:
            character.y += math.sqrt(12)
        else:
            character.y += 4

    if pygame.K_SPACE in keys and cool_down == 0:
        horizontal_arrows.append(
            gamebox.from_image(-30000, 30000, 'horizontal_arrow.png')
        )
        vertical_arrows.append(
            gamebox.from_image(-30000, 30000, 'vertical_arrow.png')
        )

        if direction == "left":
            horizontal_arrows[-1].speedx = -10
            horizontal_arrows[-1].center = character.center
            # keys.remove(pygame.K_SPACE)

        elif direction == "right":
            horizontal_arrows[-1].speedx = 10
            horizontal_arrows[-1].center = character.center
            # keys.remove(pygame.K_SPACE)

        elif direction == "up":
            vertical_arrows[-1].speedy = -10
            vertical_arrows[-1].center = character.center
            # keys.remove(pygame.K_SPACE)

        elif direction == "down":
            vertical_arrows[-1].speedy = 10
            vertical_arrows[-1].center = character.center
            # keys.remove(pygame.K_SPACE)

        cool_down = 30  # sets a half-second cool down timer on arrows

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
    if cam_locked:
        cam.x = character.x
        cam.y = character.y


# Defines enemy behavior
def monsters(strength):
    global enemy_count, enemy_health, health_level, on_level
    if enemy_count > 0:
        enemy_x = character.x + random.randrange(-750, 751)
        enemy_y = character.y + random.randrange(-750, 751)
        enemies.append(gamebox.from_image(enemy_x, enemy_y, 'goblin.png'))
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
        #enemy.move_to_stop_overlapping(enemy)  <-- Buggy, don't try

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
            health_level -= strength

    if health_level <= 0:
        health()
        cam.draw("Game Over!", 120, 'red', 385, 300)
        cam.display()
        gamebox.pause()

    cam.draw("Enemies Left: " + str(len(enemies)), 20, 'blue', 675, 25)  # prints remaining # of enemies
    #cam.display()


# game world
def level1(keys):
    global cam, cool_down, direction, enemy_count, enemy_health, enemy_x, enemy_y, health_level, on_level

    cam.clear('tan')

    upper_boundary = gamebox.from_color(0, -1800, 'tan', 3600, 1)
    lower_boundary = gamebox.from_color(0, 1800, 'tan', 3600, 1)
    left_boundary = gamebox.from_color(-1800, 0, 'tan', 1, 3600)
    right_boundary = gamebox.from_color(1800, 0, 'tan', 1, 3600)

    cam.draw(character)

    for boulder in boulders:
        cam.draw(boulder)

    for tree in trees:
        cam.draw(tree)

    for enemy in enemies:
        cam.draw(enemy)

    for arrow in horizontal_arrows:
        cam.draw(arrow)
    for arrow in vertical_arrows:
        cam.draw(arrow)

    cam.draw(health())

    if character.touches(upper_boundary) or character.touches(lower_boundary) or character.touches(left_boundary) or character.touches(right_boundary):
        cam.draw("Turn around, ser!", 75, 'blue', 400, 300)

    control(keys)
    monsters(10)
    cam.display()

    character.move_to_stop_overlapping(upper_boundary)
    character.move_to_stop_overlapping(lower_boundary)
    character.move_to_stop_overlapping(left_boundary)
    character.move_to_stop_overlapping(right_boundary)

    if len(enemies) == 0:
        enemy_count = 10
        on_level = 2


ticks = 0


def level2(keys):
    global cam, cool_down, direction, enemy_count, enemy_health, enemy_x, enemy_y,  health_level, on_level, sheet, torch, ticks
    ticks += 1

    cam.clear('black')

    upper_boundary = gamebox.from_color(0, -1800, 'black', 3600, 1)
    lower_boundary = gamebox.from_color(0, 1800, 'black', 3600, 1)
    left_boundary = gamebox.from_color(-1800, 0, 'black', 1, 3600)
    right_boundary = gamebox.from_color(1800, 0, 'black', 1, 3600)

    cam.draw(character)

    for torch in torches:
        torch.image = sheet[(ticks//6) % len(sheet)]
        cam.draw(torch)

    for enemy in enemies:
        cam.draw(enemy)

    for arrow in horizontal_arrows:
        cam.draw(arrow)
    for arrow in vertical_arrows:
        cam.draw(arrow)

    cam.draw(health())

    if character.touches(upper_boundary) or character.touches(lower_boundary) or character.touches(left_boundary) or character.touches(right_boundary):
        cam.draw("Turn around, ser!", 75, 'orange', 400, 300)

    control(keys)
    monsters(25)
    cam.display()

    character.move_to_stop_overlapping(upper_boundary)
    character.move_to_stop_overlapping(lower_boundary)
    character.move_to_stop_overlapping(left_boundary)
    character.move_to_stop_overlapping(right_boundary)

    if len(enemies) == 0:
        enemy_count = 25
        ticks = 0
        character.x, cam.x = 400, 400
        character.y, cam.y = 450, 300
        on_level = "final"


def final_level(keys):
    global cam, cool_down, direction, health_level, boss_health_level, on_level, sheet, ticks
    if ticks == 10:
        dagger_attack()
    ticks += 1

    cam.clear("black")
    cam.draw(boss_room)
    cam.draw(health())
    cam.draw(boss_health())
    cam.draw(character)
    cam.draw(boss)
    # cam.draw(gamebox.from_text(character.x, character.y, "BOSS LEVEL: TO BE DEVELOPED", 50, "red"))
    control(keys)

    # Keep player in the boss arena and not clipping through the boss
    if character.x >= 800:
        character.x = 800
    elif character.x <= 0:
        character.x = 0
    if character.y >= 555:
        character.y = 555
    elif character.y <= 45:
        character.y = 45
    if character.touches(boss):
        character.move_to_stop_overlapping(boss)
        health_level -= 20
        if character.x > boss.x:
            character.x += 15
        elif character.x < boss.x:
            character.x -= 15
        if character.y > boss.y:
            character.y += 15
        elif character.y < boss.y:
            character.y -= 15

    # Draw attacks
    for arrow in horizontal_arrows:
        if arrow.touches(boss):
            horizontal_arrows.remove(arrow)
            boss_health_level -= 2
        cam.draw(arrow)
    for arrow in vertical_arrows:
        if arrow.touches(boss):
            vertical_arrows.remove(arrow)
            boss_health_level -= 2
        cam.draw(arrow)

    for dagger in daggers_up:
        dagger.y -= 2
        cam.draw(dagger)
        if dagger.touches(character):
            daggers_up.remove(dagger)
            health_level -= 15
    for dagger in daggers_up:
        if dagger.y < -100:
            daggers_up.remove(dagger)
    for dagger in daggers_down:
        dagger.y += 2
        cam.draw(dagger)
        if dagger.touches(character):
            daggers_down.remove(dagger)
            health_level -= 15
    for dagger in daggers_down:
        if dagger.y > 700:
            daggers_down.remove(dagger)
    for dagger in daggers_left:
        dagger.x -= 2
        cam.draw(dagger)
        if dagger.touches(character):
            daggers_left.remove(dagger)
            health_level -= 15
    for dagger in daggers_left:
        if dagger.x < -100:
            daggers_left.remove(dagger)
    for dagger in daggers_right:
        dagger.x += 2
        cam.draw(dagger)
        if dagger.touches(character):
            daggers_right.remove(dagger)
            health_level -= 15
    for dagger in daggers_right:
        if dagger.x > 900:
            daggers_right.remove(dagger)

    for saw in saw_tr:
        saw.x += 4
        saw.y -= 4
        cam.draw(saw)
        if saw.touches(character):
            saw_tr.remove(saw)
            health_level -= 4
    for saw in saw_tr:
        if saw.x >= 900 or saw.y <= -100:
            saw_tr.remove(saw)
    for saw in saw_tl:
        saw.x -= 4
        saw.y -= 4
        cam.draw(saw)
        if saw.touches(character):
            saw_tl.remove(saw)
            health_level -= 4
    for saw in saw_tl:
        if saw.x <= -100 or saw.y <= -100:
            saw_tl.remove(saw)
    for saw in saw_bl:
        saw.x -= 4
        saw.y += 4
        cam.draw(saw)
        if saw.touches(character):
            saw_bl.remove(saw)
            health_level -= 4
    for saw in saw_bl:
        if saw.x <= -100 or saw.y >= 700:
            saw_bl.remove(saw)
    for saw in saw_br:
        saw.x += 4
        saw.y += 4
        cam.draw(saw)
        if saw.touches(character):
            saw_br.remove(saw)
            health_level -= 4
    for saw in saw_br:
        if saw.x >= 900 or saw.y >= 700:
            saw_br.remove(saw)

    # Boss health milestones
    if boss_health_level <= 0:
        gamebox.pause()
        for text in defeated_boss_text:
            cam.draw(text)
            cam.display()
    elif 0 < boss_health_level <= 33:
        boss_phase3()
        if ticks % 90 == 0:
            print("Boss is fighting for its life!")
    elif 33 < boss_health_level <= 67:
        boss_phase2()
        if ticks % 90 == 0:
            print("Boss is getting desperate!")
    elif 67 < boss_health_level <= 100:
        if ticks > 60:
            boss_phase1()
        if ticks % 90 == 0:
            print("Boss is toying with you.")

    if health_level <= 0:
        gamebox.pause()
        cam.draw(gamebox.from_text(400, 300, "YOU HAVE DIED", 100, "white"))

    cam.draw(health()), cam.draw(boss_health())

    cam.display()


on_level = 0


def tick(keys):
    global enemy_count, ticks, on_level, title_screen_on, level1_on, level2_on, final_level_on, cam_locked
    if pygame.K_RETURN in keys and (on_level == 1 or on_level == 2):
        character.x = 400
        character.y = 300
        cam.x = 400
        cam.y = 300
        on_level = "final"
        ticks = 0
        keys.remove(pygame.K_RETURN)

    if pygame.K_SPACE in keys and on_level == 0:
        on_level = 1
        keys.remove(pygame.K_SPACE)

    if on_level == 1:  # Game begins after space is pressed
        title_screen_on = False
        level1(keys)

    if on_level == 2:
        level2(keys)

    if on_level == "final":
        cam_locked = False
        final_level(keys)

    if title_screen_on:
        title_screen()


ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
