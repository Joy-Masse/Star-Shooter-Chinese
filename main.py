import pygame
from pygame import mixer
import random
import math

# Init
pygame.init()

# Mixer init
mixer.init()

# Screen configuration and caption. Best resolutions: 1024x768, 960x720.
res_width_file = open("config/res_width.txt", "r")
res_height_file = open("config/res_height.txt", "r")

width = int(res_width_file.read())
height = int(res_height_file.read())

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Star Shooter")
fps = 60

# Icon
icon = pygame.image.load("image/screen/star.png")
pygame.display.set_icon(icon)

# Background
if width == 1024 and height == 768:
    background = pygame.image.load("image/screen/background_1024x768_new.png").convert_alpha()
elif width == 960 and height == 720:
    background = pygame.image.load("image/screen/background_960x720_new.png").convert_alpha()

# Images
# Aliens
alien_tier1_image = pygame.image.load("image/char/alien_tier1.png")
alien_tier2_image = pygame.image.load("image/char/alien_tier2.png")
bomber_image = pygame.image.load("image/char/bomber.png")
bomber_damaged = [pygame.image.load("image/char/bomber_damaged1.png"), pygame.image.load("image/char/bomber_damaged2.png")]
boss_image = pygame.image.load("image/char/boss.png")
# Bomber stuff
bomber_reticle_small = pygame.image.load("image/objects/bomber_reticle_64x64.png")
bomber_reticle_medium = pygame.image.load("image/objects/bomber_reticle_128x128.png")
bomber_reticle_large = pygame.image.load("image/objects/bomber_reticle_256x256.png")

bomber_missile_image = pygame.image.load("image/objects/bomber_missile.png")
bomber_missile_nuke_image = pygame.image.load("image/objects/bomber_missile_nuke.png")

# Ship
ship_image = pygame.image.load("image/char/ship.png")
# Projectile
projectile_image = pygame.image.load("image/objects/projectile.png")

# Effects
impact_image = [pygame.image.load("image/objects/impact.png"), pygame.image.load("image/objects/impact1.png")]

explosion_image = [pygame.image.load("image/objects/explosion.png"), pygame.image.load("image/objects/explosion1.png"),
                   pygame.image.load("image/objects/explosion2.png"), pygame.image.load("image/objects/explosion3.png")]

bomber_explosion_small_images = [pygame.image.load("image/objects/bomber_exp/explosion_small.png"), pygame.image.load("image/objects/bomber_exp/explosion_small_1.png"),
                                 pygame.image.load("image/objects/bomber_exp/explosion_small_2.png"), pygame.image.load("image/objects/bomber_exp/explosion_small_3.png"),
                                 pygame.image.load("image/objects/bomber_exp/explosion_small_4.png"), pygame.image.load("image/objects/bomber_exp/explosion_small_5.png")]

bomber_explosion_large_images = [pygame.image.load("image/objects/bomber_exp/explosion_large.png"), pygame.image.load("image/objects/bomber_exp/explosion_large_1.png"),
                                 pygame.image.load("image/objects/bomber_exp/explosion_large_2.png"), pygame.image.load("image/objects/bomber_exp/explosion_large_3.png"),
                                 pygame.image.load("image/objects/bomber_exp/explosion_large_4.png"), pygame.image.load("image/objects/bomber_exp/explosion_large_5.png")]

laser_rays_image = pygame.image.load("image/objects/laser_rays.png")

health_bar = pygame.image.load("image/objects/health_bar.png")

hole_image = [pygame.image.load("image/objects/black_hole.png"), pygame.image.load("image/objects/black_hole1.png"),
              pygame.image.load("image/objects/black_hole2.png"), pygame.image.load("image/objects/black_hole3.png"),
              pygame.image.load("image/objects/black_hole4.png")]

# Menu
game_started = False
draw_controls = False
draw_settings = False
show_credits = False
quit_game = False
end_everything = False

# Credits
credits_x = 10
credits_y = 768

show_credits = False
endgame_cutscene = False

# Death screen
if width == 1024 and height == 768:
    death_screen_image = pygame.image.load("image/screen/death_screen_1024x768.png")
elif width == 960 and height == 720:
    death_screen_image = pygame.image.load("image/screen/death_screen_960x720.png")

# Upgrades
cartridge_upgrade_image = pygame.image.load("image/objects/cartridge_upgrade.png")
fire_rate_upgrade_image = pygame.image.load("image/objects/fire_rate_upgrade.png")
lifes_upgrade_image = pygame.image.load("image/objects/lifes_upgrade.png")
damage_upgrade_image = pygame.image.load("image/objects/damage_upgrade.png")
ammo_drop_image = pygame.image.load("image/objects/ammo.png")
all_sides_jump_drop_image = pygame.image.load("image/objects/all_sides_jump.png")

# Menu images
if width == 1024 and height == 768:
    menu_image = pygame.image.load("image/screen/menu_background_1024x768.png")
    menu_background_image = pygame.image.load("image/screen/menu_back_1024x768.png")
    controls_image = pygame.image.load("image/screen/menu_controls_1024x768.png")
    settings_image = pygame.image.load("image/screen/menu_settings_1024x768.png")
    settings_selection_image = pygame.image.load("image/objects/settings_selection.png")
elif width == 960 and height == 720:
    menu_image = pygame.image.load("image/screen/menu_background_960x720.png")
    menu_background_image = pygame.image.load("image/screen/menu_back_960x720.png")
    controls_image = pygame.image.load("image/screen/menu_controls_960x720.png")
    settings_image = pygame.image.load("image/screen/menu_settings_960x720.png")
    settings_selection_image = pygame.image.load("image/objects/settings_selection.png")

arrow_image = pygame.image.load("image/objects/arrow.png")

# Menu sounds
menu_choise_sound = pygame.mixer.Sound("sound\effect\menu_choise.wav")

# Egg
if width == 1024 and height == 768:
    egg_face = pygame.image.load("image/screen/egg_face_1024x768.png")
else:
    egg_face = pygame.image.load("image/screen/egg_face_960x720.png")

egg_image = pygame.image.load("image/objects/egg.png")

# Fonts
font_small = pygame.font.Font("fonts/BalooTamma2-Medium.ttf", 16)
font_medium = pygame.font.Font("fonts/BalooTamma2-Medium.ttf", 32)
font_large = pygame.font.Font("fonts/BalooTamma2-Medium.ttf", 64)

# Menu font
menu_font = pygame.font.Font("fonts/ShareTechMono-Regular.ttf", 64)

class Ship:
    def __init__(self, image, x, y, vel, score, lifes, alive, ammo, cartridge_capacity,
                 cartridge_ammo, fire_rate, damage, rel_timer, exp_count, exploded, blinking, should_blink, bl_counter, jumping,
                 jump_timer, jump_direction, all_sides_jump_available):
        self.image = image
        self.x = x
        self.y = y
        self.vel = vel
        self.score = score
        self.lifes = lifes
        self.alive = alive
        self.ammo = ammo
        self.cartridge_ammo = cartridge_ammo
        self.cartridge_capacity = cartridge_capacity
        self.fire_rate = fire_rate
        self.damage = damage
        self.rel_timer = rel_timer
        self.exp_count = exp_count
        self.exploded = exploded
        self.blinking = blinking
        self.should_blink = should_blink
        self.bl_counter = bl_counter
        self.jumping = jumping
        self.jump_timer = jump_timer
        self.jump_direction = jump_direction
        self.all_sides_jump_available = all_sides_jump_available

    def shoot(self, projectile, i):
        projectile.append(Projectile(projectile_image, 2000, 0, False, 0, 0, 0))
        projectile[i].x = self.x + 31
        projectile[i].y = self.y
        projectile[i].fired = True
        self.cartridge_ammo -= 1

    def replace_score(self, ship_score_x):
        if 1 <= self.score // 100 < 10:
            ship_score_x = width - 150
        elif 10 <= self.score // 100 < 100:
            ship_score_x = width - 166
        elif 100 <= self.score // 100 < 1000:
            ship_score_x = width - 182
        elif 1000 <= self.score // 100 < 10000:
            ship_score_x = width - 198

        return ship_score_x

    def revive(self, spawn_height):
        self.alive = True
        self.exploded = False
        self.should_blink = True
        self.blinking = True
        self.x = (width // 2) - 32
        self.y = spawn_height

    # direction 1 is upwards, 2 - downwards, 3 - left, 4 - right, 0 - undefined
    def jump(self):
        if self.jumping and 0 <= self.jump_timer < 10:

            # Upwards
            if self.jump_direction == 1:
                self.y -= 25
            # Downwards
            elif self.jump_direction == 2:
                self.y += 25
            # Left
            elif self.jump_direction == 3:
                self.x -= 25
            # Right
            elif self.jump_direction == 4:
                self.x += 25

            self.jump_timer += 1
        elif self.jumping and self.jump_timer == 10:
            self.jump_timer = -20
            self.jumping = False
        elif not self.jumping and self.jump_timer < 0:
            self.jump_timer += 1

    # Puts the ship in the given position
    def put_in_position(self, pos_x, pos_y):
        if self.x < pos_x - 5:
            self.x += self.vel
        elif self.x > pos_x + 5:
            self.x -= self.vel
        if self.y < pos_y:
            self.y += self.vel
        elif self.x > pos_y:
            self.y -= self.vel


class Projectile:
    def __init__(self, image, x, y, fired, timer, shoot_timer, direction):
        self.image = image
        self.x = x
        self.y = y
        self.fired = fired
        self.timer = timer
        self.shoot_timer = shoot_timer
        self.direction = direction

    # Moves the projectile
    def move(self, vel, direction):
        # 0 - upwards, 1 - downwards
        if direction == 0:
            self.y -= vel
        elif direction == 1:
            self.y += vel

    def set_direction(self):
        if self.fired and 0 <= self.y <= height:
            if self.direction == 0:
                self.y += 10
            elif self.direction == 1:
                self.y -= 10
        elif self.y >= height or self.y <= 0:
            self.fired = False


class Upgrade:
    def __init__(self, image, sound, x, y, dropped, applied, text_timer, description, description_x, description_y):
        self.image = image
        self.sound = sound
        self.x = x
        self.y = y
        self.dropped = dropped
        self.applied = applied
        self.text_timer = text_timer
        self.description = description
        self.description_x = description_x
        self.description_y = description_y

    def move(self):
        self.y += 4

    def drop(self, dropper, cor_x, cor_y):
        self.dropped = True
        self.x = dropper.x + cor_x
        self.y = dropper.y + cor_y

    def pick_up(self, picker):
        if (picker.x < self.x < picker.x + 64 and picker.y < self.y < picker.y + 64
        and not self.applied) \
        or (picker.x < self.x + 24 < picker.x + 64
        and picker.y < self.y + 24 < picker.y + 64 and not self.applied):
            self.applied = True
            self.sound.play()

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def show_upgrade_text(self, font, color):
        if self.text_timer < 45:
            show_text(self.description, font, self.description_x, self.description_y, color)
            self.text_timer += 1

    def redefine_description_coords(self, new_x, new_y):
        self.description_x = new_x
        self.description_y = new_y


class Alien:
    def __init__(self, image, x, y, vel_x, vel_y, alive, exp_count, exploded):
        self.image = image
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.alive = alive
        self.exp_count = exp_count
        self.exploded = exploded


class AlienTier1(Alien):
    def __init__(self, image, x, y, vel_x, vel_y, alive, exp_count, exploded, left_zone, right_zone):
        super().__init__(image, x, y, vel_x, vel_y, alive, exp_count, exploded)
        self.left_zone = left_zone
        self.right_zone = right_zone

    # Fills tier 1 aliens
    def fill(self):
        self.x = random.randint(100, width - 100)
        self.y = random.randint(-500, -32)
        self.vel_x = random.randint(3, 7)
        self.left_zone = self.x - random.randint(75, 200)
        self.right_zone = self.x + random.randint(75, 200)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def invert(self):
        if self.x <= self.left_zone:
            if self.vel_x < 0:
                self.vel_x = self.vel_x * (-1)
            self.x += self.vel_x
        elif self.x >= self.right_zone:
            if self.vel_x > 0:
                self.vel_x = -self.vel_x
            self.x += self.vel_x


class AlienTier2(Alien):
    def __init__(self, image, x, y, vel_x, vel_y, alive, health, exp_count, exploded, imp_count, imp_finished,
                 squad_count, squad_num, inv_speed):
        super().__init__(image, x, y, vel_x, vel_y, alive, exp_count, exploded)
        self.health = health
        self.imp_count = imp_count
        self.imp_finished = imp_finished
        self.squad_count = squad_count
        self.squad_num = squad_num
        self.inv_speed = inv_speed

    # Fills tier 2 aliens
    def fill(self):
        self.x = 175
        self.y = 0
        self.vel_x = 5

    def move(self):
        self.x += self.vel_x

    def invert(self):
        if not self.inv_speed and self.x >= width - 164:
            self.inv_speed = True
        if not self.inv_speed and self.x <= 100:
            self.inv_speed = True

    def strafe(self):
        if self.inv_speed:
            self.vel_x = self.vel_x * (-1)
            self.inv_speed = False
        elif self.inv_speed:
            self.vel_x = self.vel_x * (-1)
            self.inv_speed = False

    def rebuild(self, last_y):
        if self.squad_num == 0 and self.y < last_y + 100 < 500:
            self.y += self.vel_y

    def renumber(self):
        if self.squad_num == 0:
            self.squad_num = 4
        else:
            self.squad_num -= 1

    def change_skin(self):
        if self.health == 2:
            self.image = pygame.image.load(
                "image/char/alien_tier2_damaged.png")
        elif self.health == 1:
            self.image = pygame.image.load("image/char/alien_tier2_damaged1.png")


class Bomber(Alien):
    def __init__(self, image, x, y, vel_x, vel_y, alive, health, exp_count, exploded, imp_count, imp_finished, inv_vel, shot_ready,
                attack_type):
        super().__init__(image, x, y, vel_x, vel_y, alive, exp_count, exploded)
        self.health = health
        self.imp_count = imp_count
        self.imp_finished = imp_finished
        self.inv_vel = inv_vel
        self.shot_ready = shot_ready
        self.attack_type = attack_type

    def move(self):
        self.x += self.vel_x

    def invert(self):
        if not self.inv_vel and self.x >= width - 138:
            self.inv_vel = True
        if not self.inv_vel and self.x <= 10:
            self.inv_vel = True

    def strafe(self):
        if self.inv_vel:
            self.vel_x = self.vel_x * (-1)
            self.x += self.vel_x * 2
            self.inv_vel = False
        elif self.inv_vel:
            self.vel_x = self.vel_x * (-1)
            self.x += self.vel_x * 2
            self.inv_vel = False

    def change_skin(self):
        if 1000 >= self.health > 500:
            self.image = bomber_damaged[0]
        elif self.health < 500:
            self.image = bomber_damaged[1]


class Boss(Alien):
    def __init__(self, image, x, y, vel_x, vel_y, alive, health, exp_count, exploded, imp_count, imp_finished, inv_vel, shoots, attack_type, salvo_finished):
        super().__init__(image, x, y, vel_x, vel_y, alive, exp_count, exploded)
        self.health = health
        self.imp_count = imp_count
        self.imp_finished = imp_finished
        self.inv_vel = inv_vel
        self.shoots = shoots
        self.attack_type = attack_type
        self.salvo_finished = salvo_finished

    def move(self):
        self.x += self.vel_x

    def invert(self):
        if not self.inv_vel and self.x >= width - 537:
            self.inv_vel = True
        if not self.inv_vel and self.x <= 25:
            self.inv_vel = True

    def strafe(self):
        if self.inv_vel:
            self.vel_x = self.vel_x * (-1)
            if 0 < self.vel_x < 5:
                self.x += self.vel_x * 10
            else:
                self.x += self.vel_x * 2
            self.inv_vel = False

    def shoot(self, list, iterable):
        if self.attack_type == 1:
            for j in range(len(list)):
                list[j].fired = True
        elif self.attack_type in [2, 5]:
            list[iterable].fired = True


class Reticle:
    def __init__(self, image, x, y, active, shot):
        self.image = image
        self.x = x
        self.y = y
        self.active = active
        self.shot = shot

    def set_coordinates(self, border_x1, border_x2, border_y1, border_y2):
        self.x = random.randint(border_x1, border_x2)
        self.y = random.randint(border_y1, border_y2)
        self.active = True


class Missile:
    def __init__(self, x, y, vel_y, launched, exp_count, exploded):
        self.x = x
        self.y = y
        self.vel_y = vel_y
        self.launched = launched
        self.exp_count = exp_count
        self.exploded = exploded

    def launch(self, new_x, new_y, sound):
        self.launched = True
        self.x = new_x
        self.y = new_y
        sound.play()

    def fly(self):
        self.y += self.vel_y


class BossExplosion:
    def __init__(self, image_list, x, y):
        self.image_list = image_list
        self.x = x
        self.y = y
        self.explodes = False
        self.count = 0
        self.finished = False


def show_text(text, text_font, x, y, color):
    showing_text = text_font.render(text, True, color)
    window.blit(showing_text, (x, y))

def credits(x, y, endgame_cutscene):

    show_text("A GAME BY", menu_font, x, y, (254, 0, 246))
    show_text("GULAG ENTERTAINMENT", menu_font, x, y + 50, (253, 254, 2))

    show_text("PROGRAMMING AND GAME DESIGN", menu_font, x, y + 150, (254, 0, 246))
    show_text("NIKITA BOTVINOV", menu_font, x, y + 200, (253, 254, 2))

    show_text("SOME ART", menu_font, x, y + 300, (254, 0, 246))
    show_text("NIKITA BOTVINOV", menu_font, x, y + 350, (253, 254, 2))

    show_text("MOST OF ART", menu_font, x, y + 450, (254, 0, 246))
    show_text("GREAT ARTISTS OF FLATICON", menu_font, x, y + 500, (253, 254, 2))

    show_text("SOUND DESIGN", menu_font, x, y + 600, (254, 0, 246))
    show_text("NIKITA BOTVINOV", menu_font, x, y + 650, (253, 254, 2))

    show_text("MUSIC", menu_font, x, y + 750, (254, 0, 246))
    show_text("HYPER - FCKD", menu_font, x, y + 800, (253, 254, 2))
    show_text("HYPER - SPOILER", menu_font, x, y + 850, (253, 254, 2))
    show_text("DEFRAG - THE DAWN OF UTOPIA", menu_font, x, y + 900, (253, 254, 2))
    show_text("ORAX - ECTOPLASMIC", menu_font, x, y + 950, (253, 254, 2))
    show_text("SIGNAL VOID - GAIA", menu_font, x, y + 1000, (253, 254, 2))
    show_text("SURGERYHEAD - CONFORM", menu_font, x, y + 1050, (253, 254, 2))
    show_text("ZOMBIENICK - STALKER", menu_font, x, y + 1100, (253, 254, 2))

    show_text("TESTING", menu_font, x, y + 1200, (254, 0, 246))
    show_text("NIKITA BOTVINOV", menu_font, x, y + 1250, (253, 254, 2))
    show_text("BOGDAN \"GRANDPA\" KAMIENSKY", menu_font, x, y + 1300, (253, 254, 2))

    if y < -1425:
        if width == 1024 and height == 768:
            show_text("THANKS FOR PLAYING!", menu_font, width - 829, height - 393, (253, 254, 2))
            if not endgame_cutscene:
                show_text("PRESS ENTER", menu_font, width - 700, height - 343, (254, 0, 246))
            else:
                show_text("PRESS ESCAPE", menu_font, width - 721, height - 343, (254, 0, 246))
        else:
            show_text("THANKS FOR PLAYING!", menu_font, width - 797, height - 369, (253, 254, 2))
            if not endgame_cutscene:
                show_text("PRESS ENTER", menu_font, width - 668, height - 319, (254, 0, 246))
            else:
                show_text("PRESS ESCAPE", menu_font, width - 689, height - 319, (254, 0, 246))

def menu(choise, variants, confirmation, settings_choise, settings_variants):
    global game_started, quit_game, draw_controls, draw_settings, show_credits, credits_x, credits_y, end_everything

    def draw_menu_things(draw_controls):

        def draw_image(image, x, y):
            window.blit(image, (x, y))

        # Draw choise arrow if no menu vartiant is active
        if not draw_controls and not draw_settings and not show_credits:
            draw_image(menu_image, 0, 0)
            draw_image(arrow_image, arrow_x, arrow_y)
        # Draw controls if the controls variant is chosen
        elif draw_controls:
            draw_image(controls_image, 0, 0)
        # Do settings stuff if the settings variant is chosen
        elif draw_settings:
            draw_image(settings_image, 0, 0)
            # Selection box coordinates
            if width == 1024 and height == 768:
                settings_selection_x = [392, 392]
                settings_selection_y = [305, 354]
            elif width == 960 and height == 720:
                settings_selection_x = [359, 359]
                settings_selection_y = [285, 331]
            for i in range(len(settings_variants)):
                if i == settings_choise:
                    draw_image(settings_selection_image, settings_selection_x[i], settings_selection_y[i])
        # Draw credits if the credits variant is chosen
        elif show_credits:
            draw_image(menu_background_image, 0, 0)
            credits(credits_x, credits_y, False)

        pygame.display.update()

    # Arrow
    arrow_x = 560
    arrow_y = 319

    # Variants coordinates
    if width == 1024 and height == 768:
        variants_x = [393, 393, 393, 393, 393]
        variants_y = [206, 255, 304, 353, 402]
    elif width == 960 and height == 720:
        variants_x = [361, 361, 361, 361, 361]
        variants_y = [192, 238, 284, 330, 376]

    # Changing arrow's coordinates to contemplate with variant
    for i in variants:
        if choise == i:
            arrow_x = variants_x[i]
            arrow_y = variants_y[i]

    # Credits movement
    if show_credits:
        if credits_y >= -1425:
            credits_y -= 0.5

    # Confirmation
    if confirmation == True:
        # Draw controls
        if choise == 1:
            draw_controls = True
        if choise == 2:
            draw_settings = True
        if choise == 3:
            show_credits = True

        # Quiting the game
        if choise == 4:
            quit_game = True
            end_everything = True
    else:
        draw_controls = False
        draw_settings = False
        show_credits = False
        # Credits
        credits_x = 10
        credits_y = 768

    draw_menu_things(draw_controls)

def menu_stuff():
    global game_started, end_everything

    # Clock
    clock = pygame.time.Clock()

    # Menu variants
    menu_variants = [0, 1, 2, 3, 4]
    menu_choise = 0
    choise_confirmed = False

    # Settings variants
    settings_variants = ["1024x768", "960x720"]
    settings_choise = 0

    # Key pressed
    keydown_pressed = False
    keyup_pressed = False
    return_pressed = False

    # Music
    mixer.music.load("sound/music/menu_" + str(random.randint(1, 4)) + ".wav")
    mixer.music.set_volume(0.8) # Default 0.8
    mixer.music.play(-1)

    # Menu loop
    done = False
    while not done:
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_everything = True
                done = True

        # Choosing the variant from the menu
        keys = pygame.key.get_pressed()

        # Selecting the menu variant
        if not draw_controls and not draw_settings and not show_credits:
            # Downwards
            if keys[pygame.K_DOWN] and menu_choise < 4 and not keydown_pressed:
                menu_choise += 1
                menu_choise_sound.play()
                keydown_pressed = True
            elif keys[pygame.K_DOWN] and keydown_pressed:
                keydown_pressed = True
            else:
                keydown_pressed = False

            # Upwards
            if keys[pygame.K_UP] and menu_choise > 0 and not keyup_pressed:
                menu_choise -= 1
                menu_choise_sound.play()
                keyup_pressed = True
            elif keys[pygame.K_UP] and keyup_pressed:
                keyup_pressed = True
            else:
                keyup_pressed = False

        # Settings
        if draw_settings:
            # Left
            if keys[pygame.K_DOWN] and settings_choise <= 0:
                settings_choise += 1
                menu_choise_sound.play()
            # Right
            if keys[pygame.K_UP] and settings_choise >= 1:
                settings_choise -= 1
                menu_choise_sound.play()

        # Confirmation
        if keys[pygame.K_RETURN] and not return_pressed:

            # Game start
            if menu_choise == 0:
                mixer.music.set_volume(1)
                mixer.music.stop()
                game_started = True
                done = True

            # Settings
            if menu_choise == 2:

                # If choice is 960x720
                if settings_choise == 1:
                    res_width_file = open("config/res_width.txt", "w")
                    res_height_file = open("config/res_height.txt", "w")
                    res_width_file.write("960")
                    res_height_file.write("720")
                    res_width_file.close()
                    res_height_file.close()

                # If choice is 1024x768
                elif settings_choise == 0:
                    res_width_file = open("config/res_width.txt", "w")
                    res_height_file = open("config/res_height.txt", "w")
                    res_width_file.write("1024")
                    res_height_file.write("768")
                    res_width_file.close()
                    res_height_file.close()
            if not choise_confirmed:
                choise_confirmed = True
            else:
                choise_confirmed = False
            return_pressed = True

        elif keys[pygame.K_RETURN] and return_pressed:
            return_pressed = True
        else:
            return_pressed = False

        # Quiting the game
        if quit_game:
            done = True

        menu(menu_choise, menu_variants, choise_confirmed, settings_choise, settings_variants)

def main():
    global ship_image, hole_count, hole_x, hole_y, alien_tier1_image,\
    alien_tier2_image, health_bar, credits_x, credits_y, show_credits,\
    endgame_cutscene, description_seen_list, all_exploded, boss_explosion_amount, egg_picked,\
    egg_counter, game_started, end_everything

    # Clock
    clock = pygame.time.Clock()

    # Background y
    background_y = -3072

    # Cutscenes
    show_credits = False
    endgame_cutscene = False

    # Restart
    restart = False
    restart_pressed = False

    # Draw aliens
    draw_alien_tier1 = False
    draw_alien_tier2 = False

    # Death screen
    draw_death_screen = False
    death_screen_sound_played = False

    # Default ship spawn height. Used to prevent ship's spawning in lasers.
    ship_height = height - 100

    # Ship (image, x, y, vel, score, lifes, alive, ammo, cartridge_capacity, cartridge_ammo,
    # fire_rate, damage, rel_timer, exp_count, exploded,
    # blinking, should_blink, bl_counter, jumping, jump_timer, jump_direction)   damgage and fire rate is not deafult(5, 1)
    ship = Ship(ship_image, (width // 2) - 32, height - 100, 7, 0, 3,
                True, 250, 5, 5, 5, 1, 0, 0, False, False, False, 0, False, 0, 0, False)

    # Upgrades
    cartridge_upgrade = []
    fire_rate_upgrade = []
    lifes_upgrade = []
    damage_upgrade = []
    ammo_drop = []
    all_sides_jump_drop = []

    description_seen_list = []

    # Ship score
    ship_score_x = width - 116

    # Ship ammmo
    ship_ammo_y = height - 50

    # Ship cartridge ammo
    ship_cart_y = height - 80

    # Tier 1 aliens
    aliens_tier1 = []

    for i in range(30):
        aliens_tier1.append(AlienTier1(alien_tier1_image, 0, 0, 0, 2, True, 0, False, 0, 0))
        aliens_tier1[i].fill()

    aliens_tier1_len = len(aliens_tier1)

    # Tier 2 aliens
    aliens_tier2 = []
    aliens_tier2_y_lst = []
    aliens_tier2_amount = 25

    for i in range(25):
        aliens_tier2.append(AlienTier2(alien_tier2_image, 175, -500, 5, 5, True, 3, 0, False, 0, False, 0, 0, False))

    # BUILD THE SQUAD!
    for i in range(25):

        if i == 0:
            aliens_tier2[i].fill()
        else:
            aliens_tier2[i].squad_count = aliens_tier2[i - 1].squad_count + 1

        if aliens_tier2[i].squad_count < 5:
            aliens_tier2[i].x = aliens_tier2[i - 1].x + 100
            aliens_tier2[i].y = aliens_tier2[i - 1].y

        if aliens_tier2[i].squad_count > 4:
            aliens_tier2[i].squad_count = 0
            aliens_tier2[i].y = aliens_tier2[i - 1].y + 100

        if aliens_tier2[i].squad_count == 0 and i > 4:
            aliens_tier2[i].x = aliens_tier2[i - 5].x
            aliens_tier2[i].y = aliens_tier2[i - 5].y + 100
            aliens_tier2[i].squad_num = aliens_tier2[i - 5].squad_num + 1

        if aliens_tier2[i - 1].squad_num > 0 and aliens_tier2[i].squad_num == 0 and aliens_tier2[i].squad_count > 0:
            aliens_tier2[i].squad_num = aliens_tier2[i - 1].squad_num

        aliens_tier2_y_lst.append(aliens_tier2[i].y)

    aliens_tier2_last_y = max(aliens_tier2_y_lst)

    aliens_tier2_len = len(aliens_tier2)

    # Bomber
    bomber = Bomber(bomber_image, 448, -200, 5, 2, True, 1500, 0, False, 0, False, False, False, 0)
    bomber_shot_timer = 0

    # Bomber reticle
    bomber_reticles = []

    # Bomber missile
    missiles = []
    missiles_amount = 0

    for i in range(10):
        bomber_reticles.append(Reticle(bomber_reticle_medium, 0, -500, False, False))
        missiles.append(Missile(0, -500, 10, False, 0, False))

    # Laser rays
    laser_x = 0
    laser_y = 820

    # BOSS
    boss = Boss(boss_image, width // 2 - 256, -300, 5, 0.35, True, 5000, 0, False, 0, False, False, False, 0, False)

    boss_music_playing = False

    boss_cutscene = False

    # Attack type 1
    boss_shot_x = None
    boss_shot_y = None

    # Attack type 2
    boss_attack_timer = 0
    boss_projectile_timer = 0
    boss_shot_timer = 0
    boss_shot_count = 0

    # Attack type 3
    boss_reticles = []
    boss_missiles = []
    boss_missiles_amount = 5
    boss_missiles_exploded = False

    for i in range(5):
        boss_reticles.append(Reticle(bomber_reticle_large, 0, -500, False, False))
        boss_missiles.append(Missile(0, -500, 10, False, 0, False))

    # Attack type randomization variables
    rand_num_start = 1
    rand_num_end = 5

    # Max value of boss_shot_timer on which it must be reset
    boss_shot_timer_max = 60

    # Fourth attack type timer
    boss_fourth_timer = 0

    # Explosion
    boss_explosions = []
    boss_explosion_amount = 0
    all_exploded = False

    for i in range(random.randint(10, 25)):
        boss_explosions.append(BossExplosion(bomber_explosion_large_images, 0, 0))

    # EGG
    egg_picked = False
    egg_random = 0
    egg_list = []
    egg_counter = 0

    # Ship projectiles
    projectile = [Projectile(projectile_image, 2000, 0, False, 0, 0, 0)]
    projectile_timer = 0
    projectile_shoot_timer = 0

    # Black hole
    hole_x = 0
    hole_y = 0
    hole_count = 0

    # Tier 2 Aliens projectiles
    aliens_tier2_projectiles = []
    for i in range(aliens_tier2_len):
        aliens_tier2_projectiles.append(Projectile(projectile_image, 2000, 0, False, 0, 0, 0))

    # Boss projectiles
    boss_projectiles = []

    # Projectile impact
    impact_x = -100
    impact_y = 0

    # Sounds
    gun_sound = pygame.mixer.Sound("sound/effect/gunshot.wav")
    reload_sound = pygame.mixer.Sound("sound/effect/reload.wav")
    alien_t2_gun_sound = pygame.mixer.Sound("sound/effect/alien_t2_gunshot.wav")
    boss_gunshot = pygame.mixer.Sound("sound/effect/boss_gunshot.wav")
    impact_sound = pygame.mixer.Sound("sound/effect/impact.wav")
    hole_sound = pygame.mixer.Sound("sound/effect/hole.wav")
    ship_explosion_sound = pygame.mixer.Sound("sound/effect/ship_explosion.wav")
    alien_explosion_sound = pygame.mixer.Sound("sound/effect/alien_t1_explosion.wav")
    alien_t2_explosion_sound = pygame.mixer.Sound("sound/effect/alien_t2_explosion.wav")
    death_screen_sound = pygame.mixer.Sound("sound/effect/death.wav")
    missile_sound = pygame.mixer.Sound("sound/effect/missile_sound.wav")
    missile_hit = pygame.mixer.Sound("sound/effect/missile_hit.wav")

    # Upgrade sounds
    life_upgrade_sound = pygame.mixer.Sound("sound/effect/life_upgrade.wav")
    damage_upgrade_sound = pygame.mixer.Sound("sound/effect/damage_upgrade.wav")

    # Egg
    egg = mixer.Sound("sound/effect/egg.wav")
    
    # Silence
    silence = mixer.Sound("sound/effect/silence.wav")

    # Music
    mixer.music.load("sound/music/default.wav")
    mixer.music.set_volume(1) # Default 1
    mixer.music.play(-1)

    # Finds distance
    def distance(x1, x2, y1, y2):
        d = math.sqrt(pow((x1 - x2), 2) + pow((y2 - y1), 2))
        return d

    # Draws stuff
    def draw_things():
        global hole_x, hole_y, hole_count, show_credits, endgame_cutscene,\
        description_seen_list, all_exploded, boss_explosion_amount, egg_picked, egg_counter

        # Draws background
        window.blit(background, (0, background_y))

        # Draws ship
        if ship.alive and not ship.should_blink:
            window.blit(ship.image, (ship.x, ship.y))

        # Ship blinking and reincarnation
        if ship.lifes > 0 and ship.should_blink:
            ship.bl_counter += 1

            if 0 < ship.bl_counter // 5 < 5 or 10 < ship.bl_counter // 5 < 15 or 20 < ship.bl_counter // 5 < 25:
                window.blit(ship.image, (ship.x, ship.y))
                ship.blinking = True

            if ship.bl_counter > 120:
                ship.blinking = False
                ship.should_blink = False
                ship.bl_counter = 0

        # Ship explosion
        if not ship.alive and not ship.exploded:

            if ship.exp_count + 5 >= fps:
                ship.exp_count = 0
                ship.exploded = True

            else:
                window.blit(explosion_image[ship.exp_count // 15], (ship.x, ship.y))

                ship.exp_count += 5

        if not draw_death_screen:

            # Draws projectiles
            for i in range(len(projectile)):
                window.blit(projectile[i].image, (projectile[i].x, projectile[i].y))

            # Upgrades and drops
            # Upgrades
            for i in range(len(all_upgrades)):
                # Draws them
                if all_upgrades[i].dropped:
                    all_upgrades[i].draw()

            # Shows description
            if not description_seen_list == []:
                description_seen_list[0].show_upgrade_text(font_small, (254, 253, 2))

            # Drops
            for i in range(len(all_drops)):
                if all_drops[i].dropped:
                    all_drops[i].draw()
                if all_drops[i].applied and all_drops[i].image != all_sides_jump_drop_image:
                    all_drops[i].show_upgrade_text(font_small, (254, 253, 2))
                    description_seen_list = []
                elif all_drops[i].applied and all_drops[i].image == all_sides_jump_drop_image:
                    all_drops[i].show_upgrade_text(font_medium, (254, 253, 2))

            # Draws aliens tier 2 projectiles
            for i in range(aliens_tier2_len):
                if aliens_tier2_projectiles[i].fired:
                    window.blit(aliens_tier2_projectiles[i].image,
                                (aliens_tier2_projectiles[i].x, aliens_tier2_projectiles[i].y))

        # Death screen
        if draw_death_screen:
            window.blit(death_screen_image, (0, 0))

        # Black hole
        # Setting coordinates
        if ship.jumping and ship.jump_timer == 1:

            # Jumping upwards
            if ship.jump_direction == 1:
                hole_x = ship.x
                hole_y = ship.y - 64
                hole_count = 0
            # Jumping downwards
            if ship.jump_direction == 2:
                hole_x = ship.x
                hole_y = ship.y + 64
                hole_count = 0
            # Jumping to the left
            if ship.jump_direction == 3:
                hole_x = ship.x - 64
                hole_y = ship.y
                hole_count = 0
            # Jumping to the right
            if ship.jump_direction == 4:
                hole_x = ship.x + 64
                hole_y = ship.y
                hole_count = 0

        # Drawing
        if ship.jumping:
            if hole_count + 5 >= fps:
                hole_count = 0

            elif not hole_count + 5 > 10:

                # Upwards
                if ship.jump_direction == 1 or ship.jump_direction == 2:
                    hole_x = ship.x + 8
                elif ship.jump_direction == 3 or ship.jump_direction == 4:
                    hole_y = ship.y + 8

                window.blit(hole_image[3], (hole_x, hole_y))

                if ship.jump_direction == 1:
                    window.blit(hole_image[3], (hole_x, hole_y - 86))
                elif ship.jump_direction == 2:
                    window.blit(hole_image[3], (hole_x, hole_y + 86))
                elif ship.jump_direction == 3:
                    window.blit(hole_image[3], (hole_x - 86, hole_y))
                elif ship.jump_direction == 4:
                    window.blit(hole_image[3], (hole_x + 86, hole_y))

                hole_count += 2

            elif not hole_count + 5 > 30:
                if ship.jump_direction == 1 or ship.jump_direction == 2:
                    hole_x = ship.x
                elif ship.jump_direction == 3 or ship.jump_direction == 4:
                    hole_y = ship.y

                window.blit(hole_image[4], (hole_x, hole_y))

                if ship.jump_direction == 1:
                    window.blit(hole_image[4], (hole_x, hole_y - 86))
                elif ship.jump_direction == 2:
                    window.blit(hole_image[4], (hole_x, hole_y + 86))
                elif ship.jump_direction == 3:
                    window.blit(hole_image[4], (hole_x - 86, hole_y))
                elif ship.jump_direction == 4:
                    window.blit(hole_image[4], (hole_x + 86, hole_y))

                hole_count += 2

        elif not ship.jumping and fps > hole_count + 5 >= 5 and ship.jump_timer < 0:

            window.blit(hole_image[hole_count // 5], (hole_x, hole_y))

            if ship.jump_direction == 1:
                window.blit(hole_image[hole_count // 5], (hole_x, hole_y - 86))
            elif ship.jump_direction == 2:
                window.blit(hole_image[hole_count // 5], (hole_x, hole_y + 86))
            elif ship.jump_direction == 3:
                window.blit(hole_image[hole_count // 5], (hole_x - 86, hole_y))
            elif ship.jump_direction == 4:
                window.blit(hole_image[hole_count // 5], (hole_x + 86, hole_y))

            # Correcting hole's coordinates
            if ship.jump_direction in [1, 2]:
                if hole_count // 5 == 3:
                    hole_x = ship.x + 8
                elif hole_count // 5 == 2:
                    hole_x = ship.x + 16
                elif hole_count // 5 == 1:
                    hole_x = ship.x + 20
                elif hole_count // 5 == 0:
                    hole_x = ship.x + 24
            elif ship.jump_direction in [3, 4]:
                if hole_count // 5 == 3:
                    hole_y = ship.y + 8
                elif hole_count // 5 == 2:
                    hole_y = ship.y + 16
                elif hole_count // 5 == 1:
                    hole_y = ship.y + 20
                elif hole_count // 5 == 0:
                    hole_y = ship.y + 24

            hole_count -= 2

        if not draw_death_screen:
            # Alien tier 1 loop
            for i in range(aliens_tier1_len):
                # Draws aliens tier 1
                if aliens_tier1[i].alive and draw_alien_tier1:
                    window.blit(aliens_tier1[i].image, (aliens_tier1[i].x, aliens_tier1[i].y))

                # Aliens tier 1 explosion
                if not aliens_tier1[i].alive and not aliens_tier1[i].exploded:
                    if aliens_tier1[i].exp_count + 5 >= fps:
                        aliens_tier1[i].exp_count = 0
                        aliens_tier1[i].exploded = True
                    else:
                        window.blit(explosion_image[aliens_tier1[i].exp_count // 15], (aliens_tier1[i].x,
                                                                                       aliens_tier1[i].y))

                        aliens_tier1[i].exp_count += 5

            # Alien tier 2 loop
            for i in range(aliens_tier2_len):
                # Draws aliens tier 2
                if aliens_tier2[i].alive and draw_alien_tier2:
                    window.blit(aliens_tier2[i].image, (aliens_tier2[i].x, aliens_tier2[i].y))

                # Aliens tier 2 projectile impact
                if 3 > aliens_tier2[i].health >= 1 and not aliens_tier2[i].imp_finished:
                    if aliens_tier2[i].imp_count + 5 >= fps - 30:
                        aliens_tier2[i].imp_count = 0
                        aliens_tier2[i].imp_finished = True
                    else:
                        window.blit(impact_image[aliens_tier2[i].imp_count // 15], (impact_x,
                                                                                    impact_y))

                        aliens_tier2[i].imp_count += 5

                # Aliens tier 2 explosion
                if not aliens_tier2[i].alive and not aliens_tier2[i].exploded:
                    if aliens_tier2[i].exp_count + 5 >= fps:
                        aliens_tier2[i].exp_count = 0
                        aliens_tier2[i].exploded = True
                    else:
                        window.blit(explosion_image[aliens_tier2[i].exp_count // 15], (aliens_tier2[i].x,
                                                                                       aliens_tier2[i].y))

                        aliens_tier2[i].exp_count += 5

            # Bomber
            if bomber.alive:
                # Bomber reticles
                for i in range(len(bomber_reticles)):
                    if bomber_reticles[i].active:
                        window.blit(bomber_reticles[i].image, (bomber_reticles[i].x, bomber_reticles[i].y))

                # Missiles loop
                for i in range(len(missiles)):
                    if missiles[i].launched:
                        if bomber.attack_type in [1, 2]:
                            # Draws missile
                            window.blit(bomber_missile_image, (missiles[i].x, missiles[i].y))
                        else:
                            # Draws missile nuke
                            window.blit(bomber_missile_nuke_image, (missiles[i].x, missiles[i].y))

                    # Explosion type 1, 2
                    if bomber.attack_type in [1, 2]:
                        if not missiles[i].launched and not missiles[i].exploded and bomber_reticles[i].shot:
                            if missiles[i].exp_count + 4 >= fps:
                                missiles[i].exp_count = 0
                                missiles[i].exploded = True
                            else:
                                window.blit(bomber_explosion_small_images[missiles[i].exp_count // 10], (bomber_reticles[i].x,
                                                                                              bomber_reticles[i].y))
                                missiles[i].exp_count += 4

                    # Explosion type 3
                    elif bomber.attack_type == 3:
                        if not missiles[i].launched and not missiles[i].exploded and bomber_reticles[i].shot:
                            if missiles[i].exp_count + 4 >= fps:
                                missiles[i].exp_count = 0
                                missiles[i].exploded = True
                            else:
                                window.blit(bomber_explosion_large_images[missiles[i].exp_count // 10], (missiles[i].x - 96,
                                                                                               missiles[i].y - 96))
                                missiles[i].exp_count += 4

                # Bomber
                window.blit(bomber.image, (bomber.x, bomber.y))

                # Bomber health bar
                window.blit(health_bar, (bomber.x, bomber.y - 10))

                # Laser
                window.blit(laser_rays_image, (laser_x, laser_y))

            # Bomber explosion
            if not bomber.alive and not bomber.exploded:
                if bomber.exp_count + 4 >= fps:
                    bomber.exp_count = 0
                    bomber.exploded = True
                else:
                    window.blit(bomber_explosion_large_images[bomber.exp_count // 10], (bomber.x - 64,
                                                                                   bomber.y - 64))
                    bomber.exp_count += 4

            # Impact
            if ship.damage <= bomber.health <= 1500 and not bomber.imp_finished:
                if bomber.imp_count + 5 >= fps - 30:
                    bomber.imp_count = 0
                    bomber.imp_finished = True
                else:
                    window.blit(impact_image[bomber.imp_count // 15], (impact_x, impact_y))
                    bomber.imp_count += 5

            # Boss
            if not bomber.alive:

                # Draws boss
                if not boss_explosion_amount > len(boss_explosions) - len(boss_explosions) // 2:
                    window.blit(boss_image, (boss.x, boss.y))

                if boss.alive:

                    # Boss health bar
                    if not boss_cutscene:
                        window.blit(health_bar, (boss.x, boss.y - 15))

                    # Impact
                    if ship.damage <= boss.health <= 5000 and not boss.imp_finished:
                        if boss.imp_count + 5 >= fps - 30:
                            boss.imp_count = 0
                            boss.imp_finished = True
                        else:
                            window.blit(impact_image[boss.imp_count // 15], (impact_x, impact_y))
                            boss.imp_count += 5

                    # Reticles
                    for i in range(len(boss_reticles)):
                        if boss_reticles[i].active and not boss_reticles[i].shot:
                            window.blit(boss_reticles[i].image, (boss_reticles[i].x, boss_reticles[i].y))

                    # Missiles
                    for i in range(len(boss_missiles)):

                        # Explosion
                        if not boss_missiles[i].launched and not boss_missiles[i].exploded and boss_reticles[i].shot:
                            if boss_missiles[i].exp_count + 4 >= fps:
                                boss_missiles[i].exp_count = 0
                                boss_missiles[i].exploded = True
                            else:
                                window.blit(bomber_explosion_large_images[boss_missiles[i].exp_count // 10], (boss_missiles[i].x - 96,
                                                                                               boss_missiles[i].y - 96))
                                boss_missiles[i].exp_count += 4

                # Boss explosion
                if not boss.alive and not boss.exploded:

                    for i in range(len(boss_explosions)):
                        # Determines if explosion should happen
                        if random.randint(1, 30) == 1 and not boss_explosions[i].explodes:
                            boss_explosions[i].explodes = True
                            boss_explosions[i].x = random.randint(boss.x, boss.x + 256)
                            boss_explosions[i].y = random.randint(int(boss.y), int(boss.y + 100))

                        # Explosions!
                        if boss_explosions[i].explodes and not boss_explosions[i].finished:
                            if boss_explosions[i].count + 5 >= fps:
                                boss_explosions[i].count = 0
                                boss_explosions[i].finished = True
                                boss_explosion_amount += 1
                                missile_hit.play()
                            else:
                                window.blit(boss_explosions[i].image_list[boss_explosions[i].count // 10], (boss_explosions[i].x, boss_explosions[i].y))
                                boss_explosions[i].count += 4

                        if boss_explosion_amount == len(boss_explosions):
                            boss.exploded = True

                # Projectiles
                for i in range(len(boss_projectiles)):
                    # Projectiles
                    if boss_projectiles[i].fired:
                        window.blit(boss_projectiles[i].image, (boss_projectiles[i].x, boss_projectiles[i].y))

                # Missiles
                for i in range(len(boss_missiles)):
                    if boss_missiles[i].launched:
                        window.blit(bomber_missile_nuke_image, (boss_missiles[i].x, boss_missiles[i].y))

            if not boss_cutscene and not endgame_cutscene:
                # Ship score
                ship_score_text = font_medium.render("Score: " + str(ship.score), True, (255, 255, 255))
                window.blit(ship_score_text, (ship_score_x, 10))

                # Ship lifes
                ship_lifes_text = font_medium.render("Lifes: " + str(ship.lifes), True, (255, 255, 255))
                window.blit(ship_lifes_text, (10, 10))

                # Ship ammo
                ship_ammo_text = font_medium.render("AMMO: " + str(ship.ammo), True, (255, 255, 0))
                window.blit(ship_ammo_text, (width - 170, ship_ammo_y))

                # Ship cartridge ammo
                ship_cartridge_text = font_large.render(str(ship.cartridge_ammo), True, (255, 255, 0))

                if ship.cartridge_ammo == 0:
                    ship_cartridge_text = font_large.render("REL", True, (255, 255, 0))
                window.blit(ship_cartridge_text, (10, ship_cart_y))

            if egg_picked:
                window.blit(egg_face, (0, 0))
                egg_counter += 1
            # Credits
            if show_credits:
                credits(credits_x, credits_y, endgame_cutscene)

        pygame.display.update()

    # Main loop
    run = True
    while run:
        # Max framerate - 60
        clock.tick(fps)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_everything = True
                run = False

        # Movement
        keys = pygame.key.get_pressed()

        if ship.alive:

            if not boss_cutscene and not endgame_cutscene:
                if keys[pygame.K_w] and ((ship.y > ship.vel and not ship.jumping) or not egg_list == []):
                    ship.y -= ship.vel
                if keys[pygame.K_s] and ship.y + 64 < height and not ship.jumping:
                    ship.y += ship.vel
                if keys[pygame.K_a] and ship.x > ship.vel and not ship.jumping:
                    ship.x -= ship.vel
                if keys[pygame.K_d] and ship.x + 64 < width and not ship.jumping:
                    ship.x += ship.vel

                # Jumping
                # Upwards
                if keys[pygame.K_w] and keys[pygame.K_LSHIFT] and not ship.jumping and ship.jump_timer == 0:
                    ship.jumping = True
                    ship.jump_direction = 1
                    hole_sound.play()
                # Downwards
                if ship.all_sides_jump_available:
                    if keys[pygame.K_s] and keys[pygame.K_LSHIFT] and not ship.jumping and ship.jump_timer == 0:
                        ship.jumping = True
                        ship.jump_direction = 2
                        hole_sound.play()
                    # Left
                    if keys[pygame.K_a] and keys[pygame.K_LSHIFT] and not ship.jumping and ship.jump_timer == 0:
                        ship.jumping = True
                        ship.jump_direction = 3
                        hole_sound.play()
                    # Right
                    if keys[pygame.K_d] and keys[pygame.K_LSHIFT] and not ship.jumping and ship.jump_timer == 0:
                        ship.jumping = True
                        ship.jump_direction = 4
                        hole_sound.play()

                # Shooting a projectile
                if keys[pygame.K_SPACE]:
                    for i in range(len(projectile)):
                        if not projectile[i].fired and projectile_timer >= 1 and ship.cartridge_ammo > 0:
                            ship.shoot(projectile, i)
                            projectile_timer = 0
                            gun_sound.play()
                            break

        if keys[pygame.K_ESCAPE]:
            game_started = False
            run = False

        # Restart
        if keys[pygame.K_r]:
            if not restart and not restart_pressed and not egg_picked:
                    restart = True
                    restart_pressed = True
        else:
            restart_pressed = False

        if restart:

            # Images
            # Aliens
            alien_tier1_image = pygame.image.load("image/char/alien_tier1.png")
            alien_tier2_image = pygame.image.load("image/char/alien_tier2.png")

            # Background y
            background_y = -3072

            # Draw aliens
            draw_alien_tier1 = False
            draw_alien_tier2 = False

            # Death screen
            draw_death_screen = False
            death_screen_sound_played = False

            # Default ship spawn height. Used to prevent ship's spawning in lasers.
            ship_height = height - 100

            # Ship (image, x, y, vel, score, lifes, alive, ammo, cartridge_capacity, cartridge_ammo,
            # fire_rate, damage, rel_timer, exp_count, exploded,
            # blinking, should_blink, bl_counter, jumping, jump_timer, jump_direction)   damgage and fire rate is not deafult(5, 1)
            ship = Ship(ship_image, (width // 2) - 32, height - 100, 7, 0, 3,
                True, 250, 5, 5, 5, 1, 0, 0, False, False, False, 0, False, 0, 0, False)

            # Upgrades
            cartridge_upgrade = []
            fire_rate_upgrade = []
            lifes_upgrade = []
            damage_upgrade = []
            ammo_drop = []
            all_sides_jump_drop = []

            description_seen_list = []

            # Ship score
            ship_score_x = width - 116

            # Ship ammmo
            ship_ammo_y = height - 50

            # Ship cartridge ammo
            ship_cart_y = height - 80

            # Tier 1 aliens
            aliens_tier1 = []

            for i in range(30):
                aliens_tier1.append(AlienTier1(alien_tier1_image, 0, 0, 0, 2, True, 0, False, 0, 0))
                aliens_tier1[i].fill()

            aliens_tier1_len = len(aliens_tier1)

            # Tier 2 aliens
            aliens_tier2 = []
            aliens_tier2_y_lst = []
            aliens_tier2_amount = 25

            for i in range(25):
                aliens_tier2.append(AlienTier2(alien_tier2_image, 175, -500, 5, 5, True, 3, 0, False, 0, False, 0, 0, False))

            # BUILD THE SQUAD!
            for i in range(25):

                if i == 0:
                    aliens_tier2[i].fill()
                else:
                    aliens_tier2[i].squad_count = aliens_tier2[i - 1].squad_count + 1

                if aliens_tier2[i].squad_count < 5:
                    aliens_tier2[i].x = aliens_tier2[i - 1].x + 100
                    aliens_tier2[i].y = aliens_tier2[i - 1].y

                if aliens_tier2[i].squad_count > 4:
                    aliens_tier2[i].squad_count = 0
                    aliens_tier2[i].y = aliens_tier2[i - 1].y + 100

                if aliens_tier2[i].squad_count == 0 and i > 4:
                    aliens_tier2[i].x = aliens_tier2[i - 5].x
                    aliens_tier2[i].y = aliens_tier2[i - 5].y + 100
                    aliens_tier2[i].squad_num = aliens_tier2[i - 5].squad_num + 1

                if aliens_tier2[i - 1].squad_num > 0 and aliens_tier2[i].squad_num == 0 and aliens_tier2[i].squad_count > 0:
                    aliens_tier2[i].squad_num = aliens_tier2[i - 1].squad_num

                aliens_tier2_y_lst.append(aliens_tier2[i].y)

            aliens_tier2_last_y = max(aliens_tier2_y_lst)

            aliens_tier2_len = len(aliens_tier2)

            # Bomber
            bomber = Bomber(bomber_image, 448, -200, 5, 2, True, 1500, 0, False, 0, False, False, False, 0)
            bomber_shot_timer = 0

            # Bomber reticle
            bomber_reticles = []

            # Bomber missile
            missiles = []
            missiles_amount = 0

            for i in range(10):
                bomber_reticles.append(Reticle(bomber_reticle_medium, 0, -500, False, False))
                missiles.append(Missile(0, -500, 10, False, 0, False))

            # Laser rays
            laser_x = 0
            laser_y = 820

            # BOSS
            boss = Boss(boss_image, width // 2 - 256, -300, 5, 0.35, True, 5000, 0, False, 0, False, False, False, 0, False)

            boss_music_playing = False

            boss_cutscene = False

            # Attack type 1
            boss_shot_x = None
            boss_shot_y = None

            # Attack type 2
            boss_attack_timer = 0
            boss_projectile_timer = 0
            boss_shot_timer = 0
            boss_shot_count = 0

            # Attack type 3
            boss_reticles = []
            boss_missiles = []
            boss_missiles_amount = 5
            boss_missiles_exploded = False

            for i in range(5):
                boss_reticles.append(Reticle(bomber_reticle_large, 0, -500, False, False))
                boss_missiles.append(Missile(0, -500, 10, False, 0, False))

            # Attack type randomization variables
            rand_num_start = 1
            rand_num_end = 5

            # Max value of boss_shot_timer on which it must be reset
            boss_shot_timer_max = 60

            # Fourth attack type timer
            boss_fourth_timer = 0

            # Explosion
            boss_explosions = []
            boss_explosion_amount = 0
            all_exploded = False

            for i in range(random.randint(10, 25)):
                boss_explosions.append(BossExplosion(bomber_explosion_large_images, 0, 0))

            # EGG
            egg_picked = False
            egg_random = 0
            egg_list = []
            egg_counter = 0

            # Ship projectiles
            projectile = [Projectile(projectile_image, 2000, 0, False, 0, 0, 0)]
            projectile_timer = 0
            projectile_shoot_timer = 0

            # Black hole
            hole_x = 0
            hole_y = 0
            hole_count = 0

            # Tier 2 Aliens projectiles
            aliens_tier2_projectiles = []
            for i in range(aliens_tier2_len):
                aliens_tier2_projectiles.append(Projectile(projectile_image, 2000, 0, False, 0, 0, 0))

            # Boss projectiles
            boss_projectiles = []

            # Projectile Impact
            impact_x = -100
            impact_y = 0

            # Egg
            egg = mixer.Sound("sound/effect/egg.wav")

            # Silence
            silence = mixer.Sound("sound/effect/silence.wav")

            # Music
            mixer.music.load("sound/music/default.wav")
            mixer.music.set_volume(1) # Default 1
            mixer.music.play(-1)

            # Credits and cutscenes
            credits_x = 10
            credits_y = 768

            show_credits = False
            endgame_cutscene = False

            # Restart
            restart = False
            # DO NOT WRITE restart_pressed = False HERE!

            # Death screen
            draw_death_screen = False
            death_screen_sound_played = False

        # Boundaries:
        if not boss_cutscene and not endgame_cutscene:
            if ship.y < 0 and egg_list == []:
                ship.y = 0
            elif ship.y + 64 > height:
                ship.y = height - 64
            if ship.x < 0:
                ship.x = 0
            elif ship.x + 64 > width:
                ship.x = width - 64

        # Ship projectile loop
        for i in range(len(projectile)):
            if projectile[i].fired:
                projectile[i].move(15, 0)
            else:
                projectile[i].fired = False
                projectile[i].x = 2000

            # Cooldown before shooting
            if projectile_shoot_timer // ship.fire_rate > 0 and not projectile[i].fired:
                projectile_shoot_timer = 0
                projectile_timer += 1

        projectile_shoot_timer += 1

        # Burst timer
        if ship.cartridge_ammo == 0:
            if ship.ammo > 0:
                ship.rel_timer += 1
                if 10 < ship.rel_timer < 15:
                    reload_sound.play()
                if ship.rel_timer > 30:
                    if ship.ammo // ship.cartridge_capacity > 0:
                        ship.cartridge_ammo = ship.cartridge_capacity
                        ship.ammo -= ship.cartridge_capacity
                    else:
                        ship.cartridge_ammo = ship.ammo
                        ship.ammo = 0
                    ship.rel_timer = 0

        # Background moving
        if background_y < 0 and boss.alive:
            background_y += 1

        if background_y == 0:
            background_y = -3072

        # Ship score
        ship_score_x = ship.replace_score(ship_score_x)

        # Ship upgrades
        # Redefinition of description coords
        all_upgrades = cartridge_upgrade + fire_rate_upgrade + lifes_upgrade + damage_upgrade
        all_drops = ammo_drop + all_sides_jump_drop + egg_list

        for i in range(len(all_upgrades)):
            # Cartridge upgrade
            if all_upgrades[i].image == cartridge_upgrade_image:
                all_upgrades[i].redefine_description_coords(ship.x - 40, ship.y + 70)
            # Fire rate upgrade
            elif all_upgrades[i].image == fire_rate_upgrade_image:
                all_upgrades[i].redefine_description_coords(ship.x - 41, ship.y + 70)
            # Lifes upgrade
            elif all_upgrades[i].image == lifes_upgrade_image:
                all_upgrades[i].redefine_description_coords(ship.x - 11, ship.y + 70)
            # Damage upgrade
            elif all_upgrades[i].image == damage_upgrade_image:
                all_upgrades[i].redefine_description_coords(ship.x - 34, ship.y + 70)

            # Movement
            if all_upgrades[i].dropped and not all_upgrades[i].applied:
                all_upgrades[i].move()

            # Picking up
            all_upgrades[i].pick_up(ship)

            # Effect
            if all_upgrades[i].applied and all_upgrades[i].dropped:
                # Cartridge upgrade
                if all_upgrades[i].image == cartridge_upgrade_image:
                    ship.cartridge_capacity += 5
                    all_upgrades[i].dropped = False
                # Fire rate upgrade
                elif all_upgrades[i].image == fire_rate_upgrade_image:
                    if ship.fire_rate > 1:
                        ship.fire_rate -= 0.25
                    all_upgrades[i].dropped = False
                # Lifes upgrade
                elif all_upgrades[i].image == lifes_upgrade_image:
                    ship.lifes += 1
                    all_upgrades[i].dropped = False
                # Damage upgrade
                elif all_upgrades[i].image == damage_upgrade_image:
                    ship.damage += 1
                    all_upgrades[i].dropped = False

                if description_seen_list == []:
                    description_seen_list.append(all_upgrades[i])
                else:
                    if description_seen_list[0].text_timer == 45:
                        description_seen_list.pop(0)
                        description_seen_list.append(all_upgrades[i])

        # Drops
        for i in range(len(all_drops)):
            # Ammo drop
            if all_drops[i].image == ammo_drop_image:
                all_drops[i].redefine_description_coords(ship.x - 15, ship.y + 70)
            # All sides jump drop
            elif all_drops[i].image == all_sides_jump_drop_image:
                if width == 1024 and height == 768:
                    all_drops[i].redefine_description_coords(width - 704, height - 394)
                else:
                    all_drops[i].redefine_description_coords(width - 672, height - 346)

            # Movement
            if all_drops[i].dropped and not all_drops[i].applied and not all_drops[i].image == egg_image:
                all_drops[i].move()
            if all_drops[i].y > height:
                all_drops[i].dropped = False

            # Picking up
            all_drops[i].pick_up(ship)

            # Ammo drop
            if all_drops[i].applied and all_drops[i].dropped and all_drops[i].image == ammo_drop_image:
                ship.ammo += 1000
                all_drops[i].dropped = False
            # All sides jump
            elif all_drops[i].applied and all_drops[i].dropped and all_drops[i].image == all_sides_jump_drop_image:
                ship.all_sides_jump_available = True
                all_drops[i].dropped = False
            # Egg
            elif all_drops[i].applied and all_drops[i].dropped and all_drops[i].image == egg_image:
                egg_picked = True
                egg.play()
                all_drops[i].dropped = False

        # Ship reincarnation
        if ship.lifes > 0 and ship.exploded:
            ship.revive(ship_height)
        elif ship.lifes <= 0:
            draw_death_screen = True
            mixer.music.stop()
            if not death_screen_sound_played:
                death_screen_sound.play()
                death_screen_sound_played = True

        # Ship jump
        ship.jump()

        # Alien tier 1 loop
        if background_y > -2972:

            for i in range(aliens_tier1_len):

                # Draw alien
                draw_alien_tier1 = True

                # Movement
                if aliens_tier1[i].alive:
                    aliens_tier1[i].move()

                    # Invertion
                    aliens_tier1[i].invert()

                    # Projectile collision
                    for j in range(len(projectile)):
                        if aliens_tier1[i].x < projectile[j].x < aliens_tier1[i].x + 32 \
                                and aliens_tier1[i].y > projectile[j].y > aliens_tier1[i].y - 32:
                            projectile[j].fired = False
                            aliens_tier1[i].alive = False
                            ship.score += 100
                            ship.ammo += 2
                            alien_explosion_sound.play()

                            # Upgrade drop
                            if random.randint(0, 1) == 0:
                                rand_num = random.randint(0, 3)

                                # Cartridge upgrade
                                if rand_num == 0:
                                    cartridge_upgrade.append(Upgrade(cartridge_upgrade_image, reload_sound, 0, 0, False, False, 0, "CATRIDGE UPGRADE", ship.x - 32, ship.y + 70))
                                    for ii in range(len(cartridge_upgrade)):
                                        if not cartridge_upgrade[ii].dropped:
                                            cartridge_upgrade[ii].drop(aliens_tier1[i], 4, 4)
                                            break

                                # Fire rate upgrade
                                elif rand_num == 1 and ship.fire_rate > 1:
                                    fire_rate_upgrade.append(Upgrade(fire_rate_upgrade_image, reload_sound, 0, 0, False, False, 0, "FIRE RATE UPGRADE", ship.x - 32, ship.y + 70))
                                    for ii in range(len(fire_rate_upgrade)):
                                        if not fire_rate_upgrade[ii].dropped and ship.fire_rate > 1.0:
                                            fire_rate_upgrade[ii].drop(aliens_tier1[i], 4, 4)
                                            break

                                # Lifes upgrade
                                elif rand_num == 2 and ship.alive:
                                    lifes_upgrade.append(Upgrade(lifes_upgrade_image, life_upgrade_sound, 0, 0, False, False, 0, "MORE LIFES", ship.x - 32, ship.y + 70))
                                    for ii in range(len(lifes_upgrade)):
                                        if not lifes_upgrade[ii].dropped:
                                            lifes_upgrade[ii].drop(aliens_tier1[i], 4, 4)
                                            break

                                # Damage upgrade
                                elif rand_num == 3 and ship.alive:
                                    damage_upgrade.append(Upgrade(damage_upgrade_image, damage_upgrade_sound, 0, 0, False, False, 0, "DAMAGE UPGRADE", ship.x - 32, ship.y + 70))
                                    for ii in range(len(damage_upgrade)):
                                        if not damage_upgrade[ii].dropped:
                                            damage_upgrade[ii].drop(aliens_tier1[i], 4, 4)
                                            break

                    # Collision with ship (The hell? I was able to break those lines all that time?)
                    if ship.x <= aliens_tier1[i].x <= ship.x + 56 \
                            and ship.y <= aliens_tier1[i].y <= ship.y + 64 \
                            and ship.alive and not ship.blinking and not ship.jumping:
                        ship.alive = False
                        ship.lifes -= 1
                        aliens_tier1[i].alive = False
                        ship_explosion_sound.play()

        # Aliens tier 2 loop
        if aliens_tier1 == []:
            # Draw alien
            draw_alien_tier2 = True

            for i in range(aliens_tier2_len):
                if aliens_tier2[i].alive:
                    # Movement
                    aliens_tier2[i].move()

                    # Speed inverting for strafing
                    aliens_tier2[i].invert()

                    # Strafing
                    aliens_tier2[i].strafe()

                    # Squad rebuilding
                    aliens_tier2[i].rebuild(aliens_tier2_last_y)

                    if aliens_tier2[i].squad_num == 0 and aliens_tier2[i].y >= aliens_tier2_last_y + 100:
                        for j in range(aliens_tier2_len):
                            # Renumbering squads
                            aliens_tier2[j].renumber()
                            # Updating last y
                            aliens_tier2_last_y = max(aliens_tier2_y_lst)
                    aliens_tier2[i].rebuild(aliens_tier2_last_y)

                    # Collision of ship with tier 2 aliens
                    if (aliens_tier2[i].x <= ship.x <= aliens_tier2[i].x + 64
                        or aliens_tier2[i].x <= ship.x + 64 <= aliens_tier2[i].x + 64) \
                            and (aliens_tier2[i].y <= ship.y <= aliens_tier2[i].y + 64
                                 or aliens_tier2[i].y <= ship.y + 64 <= aliens_tier2[i].y + 64) \
                            and ship.alive and not ship.blinking:
                        ship.alive = False
                        ship.lifes -= 1
                        aliens_tier2[i].health -= 2
                        impact_x = 2000
                        impact_y = 0
                        ship_explosion_sound.play()

                    # Ship's projectile collision with tier 2 aliens
                    for j in range(len(projectile)):
                        if aliens_tier2[i].x < projectile[j].x < aliens_tier2[i].x + 64 \
                                and aliens_tier2[i].y < projectile[j].y < aliens_tier2[i].y + 64:
                            if aliens_tier2[i].health >= 1:
                                if aliens_tier2[i].health < 3:
                                    aliens_tier2[i].imp_finished = False
                                ship.score += 500
                                aliens_tier2[i].health -= ship.damage
                                impact_x = projectile[j].x
                                impact_y = aliens_tier2[i].y + 64
                                if aliens_tier2[i].health > 0:
                                    impact_sound.play()
                            else:
                                ship.score += 500
                                aliens_tier2[i].health -= 1
                                aliens_tier2[i].alive = False
                                alien_t2_explosion_sound.play()
                            projectile[j].fired = False
                            projectile[j].x = 2000

                    # Skin changing
                    aliens_tier2[i].change_skin()

                    # Death
                    if aliens_tier2[i].health < 1:
                        aliens_tier2[i].alive = False
                        ship.ammo += 15
                        aliens_tier2_amount -= 1
                        alien_t2_explosion_sound.play()

                        # Ammo drop
                        if aliens_tier2_amount == 0 and ammo_drop == []:
                            ammo_drop.append(Upgrade(ammo_drop_image, reload_sound, 0, 0, False, False, 0, "MORE AMMO", ship.x - 32, ship.y + 70))
                            if not ammo_drop[0].dropped:
                                ammo_drop[0].drop(aliens_tier2[i], 20, 20)

                        # Upgrades
                        if random.randint(1, 2) == 1:
                            # Random number that will define what upgrade is going to drop
                            rand_num = random.randint(0, 3)

                            # Cartridge upgrade
                            if rand_num == 0:
                                cartridge_upgrade.append(Upgrade(cartridge_upgrade_image, reload_sound, 0, 0, False, False, 0, "CARTRIDGE UPGRADE", ship.x - 32, ship.y + 70))
                                for ii in range(len(cartridge_upgrade)):
                                    if not cartridge_upgrade[ii].dropped and not cartridge_upgrade[ii].applied:
                                        cartridge_upgrade[ii].drop(aliens_tier2[i], 20, 20)
                                        break
                            # Fire rate upgrade
                            elif rand_num == 1 and ship.fire_rate > 1:
                                fire_rate_upgrade.append(Upgrade(fire_rate_upgrade_image, reload_sound, 0, 0, False, False, 0, "FIRE RATE UPGRADE", ship.x - 32, ship.y + 70))
                                for ii in range(len(fire_rate_upgrade)):
                                    if not fire_rate_upgrade[ii].dropped and not fire_rate_upgrade[ii].applied:
                                        fire_rate_upgrade[ii].drop(aliens_tier2[i], 20, 20)
                                        break

                            # Lifes upgrade
                            elif rand_num == 2 and ship.alive:
                                lifes_upgrade.append(Upgrade(lifes_upgrade_image, life_upgrade_sound, 0, 0, False, False, 0, "MORE LIFES", ship.x - 32, ship.y + 70))
                                for ii in range(len(lifes_upgrade)):
                                    if not lifes_upgrade[ii].dropped and not lifes_upgrade[ii].applied:
                                        lifes_upgrade[ii].drop(aliens_tier2[i], 20, 20)
                                        break

                            # Damage upgrade
                            elif rand_num == 3 and ship.alive:
                                damage_upgrade.append(Upgrade(damage_upgrade_image, damage_upgrade_sound, 0, 0, False, False, 0, "DAMAGE UPGRADE", ship.x - 32, ship.y + 70))
                                for ii in range(len(damage_upgrade)):
                                    if not damage_upgrade[ii].dropped and not damage_upgrade[ii].applied:
                                        damage_upgrade[ii].drop(aliens_tier2[i], 20, 20)
                                        break

                    # Shooting a projectile
                    if random.randint(1, 125) == 1 and not aliens_tier2_projectiles[i].fired and aliens_tier2[i].y >= 0 and ship.alive:
                        aliens_tier2_projectiles[i].fired = True
                        aliens_tier2_projectiles[i].x = aliens_tier2[i].x + 32
                        aliens_tier2_projectiles[i].y = aliens_tier2[i].y + 64
                        alien_t2_gun_sound.play()

                        # Direction downwards
                        if ship.y >= aliens_tier2[i].y:
                            aliens_tier2_projectiles[i].direction = 0
                        # Direction upwards
                        elif ship.y < aliens_tier2[i].y:
                            aliens_tier2_projectiles[i].direction = 1

                aliens_tier2_projectiles[i].set_direction()

                # Projectile collision with ship
                if aliens_tier2_projectiles[i].fired and ship.x <= aliens_tier2_projectiles[i].x <= ship.x + 64 \
                        and ship.y <= aliens_tier2_projectiles[i].y <= ship.y + 64 \
                        and ship.alive and not ship.blinking and not ship.jumping:
                    ship.alive = False
                    aliens_tier2_projectiles[i].fired = False
                    ship.lifes -= 1
                    ship_explosion_sound.play()

        # Bomber
        if aliens_tier2_amount == 0 and ship.lifes >= 1:
            # Bomber movement
            if bomber.y < 60:
                bomber.y += bomber.vel_y
            else:
                # Movement
                bomber.move()
                bomber.strafe()
                bomber.invert()

            # Laser rays movement
            if laser_y > height - 100:
                laser_y -= 2

            if bomber.alive:
                # Collision with ship
                if (bomber.x <= ship.x <= bomber.x + 128
                    or bomber.x <= ship.x + 64 <= bomber.x + 128) \
                        and (bomber.y <= ship.y <= bomber.y + 128
                             or bomber.y <= ship.y + 64 <= bomber.y + 128) \
                        and ship.alive and not ship.blinking:
                    ship.alive = False
                    ship.lifes -= 1
                    bomber.health -= 10
                    impact_x = 2000
                    impact_y = 0
                    ship_explosion_sound.play()

                # Ship's projectiles collision
                for i in range(len(projectile)):
                    if bomber.x < projectile[i].x < bomber.x + 128 \
                            and bomber.y < projectile[i].y < bomber.y + 128:
                        if bomber.health >= 1:
                            if bomber.health < 1500:
                                bomber.imp_finished = False
                            ship.score += 100
                            bomber.health -= ship.damage
                            impact_x = projectile[i].x
                            impact_y = bomber.y + 128
                            if bomber.health > 0:
                                impact_sound.play()
                        # Death
                        else:
                            ship.score += 50000
                            ship.ammo += 2000
                            bomber.health -= ship.damage
                            bomber.alive = False
                            missile_hit.play()

                            # All sides jump drop
                            if all_sides_jump_drop == []:
                                all_sides_jump_drop.append(Upgrade(all_sides_jump_drop_image, damage_upgrade_sound, 0, 0, False, False, 0, "ALL SIDES JUMP ACTIVATED", ship.x - 32, ship.y + 70))
                                if not all_sides_jump_drop[0].dropped:
                                    all_sides_jump_drop[0].drop(bomber, 52, 52)

                        projectile[i].fired = False
                        projectile[i].x = 2000

                # Skin changing
                bomber.change_skin()

                # Laser collision
                if ship.y + 64 > laser_y and ship.alive and not ship.blinking:
                    ship.alive = False
                    ship.lifes -= 1
                    ship_explosion_sound.play()

                # Preventing ship spawning in lasers
                if ship_height != height - 200:
                    ship_height = height - 200

                # Showing ship ammo above lasers
                ship_ammo_y = height - 150
                ship_cart_y = height - 180

                # Health bar
                if bomber.health >= ship.damage:
                    health_bar = pygame.transform.scale(health_bar, (int(round(bomber.health // 11.71875)), 10))

                # Shooting system
                if bomber_shot_timer >= 120 and not bomber.shot_ready:
                    bomber.shot_ready = True
                    bomber_shot_timer = 0
                    bomber.attack_type = random.randint(1, 3) # Default (1, 3)

                    if bomber.attack_type in [1, 2]:
                        for i in range(len(bomber_reticles)):
                            bomber_reticles[i] = Reticle(bomber_reticle_medium, 0, -500, False, False)
                            missiles[i].exploded = False
                    else:
                        for i in range(len(bomber_reticles)):
                            bomber_reticles[i] = Reticle(bomber_reticle_large, 0, -500, False, False)
                            missiles[i].exploded = False

                # Positioning the reticle and shooting
                if bomber.shot_ready:
                    # Positioning the reticle
                    # Attack type 1
                    if bomber.attack_type == 1:
                        for i in range(len(bomber_reticles)):
                            if not bomber_reticles[i].active and not bomber_reticles[i].shot:
                                bomber_reticles[i].set_coordinates(20, width - 212, 190, height - 248)
                                missiles_amount = 10

                    # Attack type 2
                    if bomber.attack_type == 2:
                        if not bomber_reticles[0].active and not bomber_reticles[0].shot:
                            bomber_reticles[0].set_coordinates(20, width - 512, 190, height - 528)
                        for i in range(len(bomber_reticles)):
                            if not bomber_reticles[i].active and not bomber_reticles[i].shot:
                                bomber_reticles[i].set_coordinates(bomber_reticles[0].x, bomber_reticles[0].x + 300, bomber_reticles[0].y, bomber_reticles[0].y + 300)
                                missiles_amount = 10

                    # Attack type 3
                    if bomber.attack_type == 3:
                        for i in range(3):
                            if not bomber_reticles[i].active and not bomber_reticles[i].shot:
                                bomber_reticles[i].set_coordinates(20, width - 340, 190, height - 356)
                                missiles_amount = 3

                    # Shooting the missile
                    for i in range(len(bomber_reticles)):
                        # Type 1 and 2
                        if bomber.attack_type in [1, 2]:
                            if 0 <= bomber.x + 16 - bomber_reticles[i].x <= 5 and not missiles[i].launched and bomber_reticles[i].active:
                                missiles[i].launch(bomber_reticles[i].x + 32, bomber.y + 64, missile_sound)
                        # Type 3
                        if bomber.attack_type == 3:
                            if 0 <= bomber.x - 64 - bomber_reticles[i].x <= 5 and not missiles[i].launched and bomber_reticles[i].active:
                                missiles[i].launch(bomber_reticles[i].x + 96, bomber.y + 128, missile_sound)

                        if missiles[i].launched:
                            # Movement
                            missiles[i].fly()

                            # Missile hit
                            if bomber.attack_type in [1, 2]:
                                # Reticle hit
                                if missiles[i].y >= bomber_reticles[i].y:
                                    missiles[i].launched = False
                                    missiles_amount -= 1
                                    bomber_reticles[i].shot = True
                                    bomber_reticles[i].active = False
                                    missile_hit.play()
                                    if distance(ship.x + 32, bomber_reticles[i].x + 32, ship.y + 32, bomber_reticles[i].y + 32) <= 96\
                                        and ship.alive and not ship.blinking:
                                        ship.alive = False
                                        ship.lifes -= 1
                                        ship_explosion_sound.play()

                                # Ship hit
                                if (missiles[i].x <= ship.x <= missiles[i].x + 64 or missiles[i].x <= ship.x + 64 <= missiles[i].x + 64)\
                                    and (missiles[i].y <= ship.y <= missiles[i].y + 64 or missiles[i].y <= ship.y + 64 <= missiles[i].y + 64)\
                                    and ship.alive and not ship.blinking and not ship.jumping:
                                    ship.alive = False
                                    ship.lifes -= 1
                                    ship_explosion_sound.play()
                            else:
                                # Reticle hit
                                if missiles[i].y >= bomber_reticles[i].y + 64:
                                    missiles[i].launched = False
                                    missiles_amount -= 1
                                    bomber_reticles[i].shot = True
                                    bomber_reticles[i].active = False
                                    missile_hit.play()
                                    if distance(ship.x + 32, bomber_reticles[i].x + 128, ship.y + 32, bomber_reticles[i].y + 128) <= 160\
                                    and ship.alive and not ship.blinking and not ship.jumping:
                                        ship.alive = False
                                        ship.lifes -= 1
                                        ship_explosion_sound.play()

                                # Ship hit
                                if missiles[i].x <= ship.x <= missiles[i].x + 64\
                                    and missiles[i].y <= ship.y <= missiles[i].y + 64\
                                    and ship.alive and not ship.blinking:
                                    ship.alive = False
                                    ship.lifes -= 1
                                    ship_explosion_sound.play()

                if missiles_amount == 0:
                    bomber_shot_timer += 1
                    bomber.shot_ready = False

                # Repositioning ship ammo and ship cartridge ammo height
                if not bomber.alive:
                    # Ship ammmo
                    ship_ammo_y = height - 50

                    # Ship cartridge ammo
                    ship_cart_y = height - 80

        # Boss
        if not bomber.alive and len(all_drops) > 1 and not all_drops[1].dropped and ship.lifes >= 1:

            if boss.alive:
                # Cutcsene
                if boss_cutscene:
                    # Putting the ship in the correct position
                    ship.put_in_position((width // 2) - 32, height - 100)

                # Movement
                # Movement in the cutscene
                if boss.y < 60:
                    boss.y += boss.vel_y
                    boss_cutscene = True

                # Movement out of cutscene
                if not boss_cutscene:
                    boss.move()
                    boss.strafe()
                    boss.invert()

                # Playing music
                if not boss_music_playing:
                    mixer.music.stop()
                    mixer.music.load("sound/music/boss_music.wav")
                    mixer.music.set_volume(0.90)
                    mixer.music.play(-1)
                    boss_music_playing = True

                # Finishing cutscene
                if pygame.mixer.music.get_pos() >= 22700 and boss_cutscene:
                    boss_cutscene = False
                    boss.attack_type = 1
                    boss.shoots = True

                # Collision with ship
                if (boss.x <= ship.x <= boss.x + 512
                or boss.x <= ship.x + 64 <= boss.x + 512) \
                and (boss.y <= ship.y <= boss.y + 289
                or boss.y <= ship.y + 64 <= boss.y + 289) \
                and ship.alive and not ship.blinking:
                    ship.alive = False
                    ship.lifes -= 1
                    boss.health -= 10
                    impact_x = 2000
                    impact_y = 0
                    ship_explosion_sound.play()

                # Ship's projectiles collision
                for i in range(len(projectile)):
                    if boss.x < projectile[i].x < boss.x + 512 \
                    and boss.y < projectile[i].y < boss.y + 289 and projectile[i].fired:
                        
                        # Hitbox system
                        if projectile[i].y < (projectile[i].x - boss.x) * ((projectile[i].x - boss.x) / projectile[i].y) + 235 and projectile[i].x < boss.x + 225:
                            if boss.health >= 1:
                                if boss.health < 5000:
                                    boss.imp_finished = False
                            ship.score += 100
                            impact_x = projectile[i].x
                            impact_y = (projectile[i].x - boss.x) * ((projectile[i].x - boss.x) / projectile[i].y) + 235
                            projectile[i].fired = False
                            projectile[i].x = 2000
                            impact_sound.play()

                            # Damage
                            boss.health -= ship.damage

                        elif projectile[i].y < ((boss.x + 256) - (projectile[i].x - 225)) * (((boss.x + 256) - (projectile[i].x - 225)) / projectile[i].y) + 235 and projectile[i].x > boss.x + 285:
                            if boss.health >= 1:
                                if boss.health < 5000:
                                    boss.imp_finished = False
                            ship.score += 100
                            impact_x = projectile[i].x
                            impact_y = ((boss.x + 256) - (projectile[i].x - 225)) * (((boss.x + 256) - (projectile[i].x - 225)) / projectile[i].y) + 235
                            projectile[i].fired = False
                            projectile[i].x = 2000
                            impact_sound.play()

                            # Damage
                            boss.health -= ship.damage
                            
                        elif boss.x + 225 < projectile[i].x < boss.x + 285:
                            if boss.health >= 1:
                                if boss.health < 5000:
                                    boss.imp_finished = False
                            ship.score += 100
                            impact_x = projectile[i].x
                            impact_y = projectile[i].y
                            projectile[i].x = 2000
                            impact_sound.play()

                            # Double damage
                            boss.health -= ship.damage * 2
                        
                        # Death
                        if boss.health <= ship.damage and boss.alive:
                            ship.score += 150000
                            boss.health -= ship.damage
                            boss.alive = False
                            egg_random = random.randint(1, 10) # Determines if egg should drop after death
                            mixer.music.stop()
                            missile_hit.play()

                # Health bar
                if boss.health >= ship.damage:
                    health_bar = pygame.transform.scale(health_bar, (int(round(boss.health // 9.765625)), 10))

                # Shooting system
                # Getting ready
                if boss_shot_timer >= boss_shot_timer_max and not boss_cutscene:
                    boss.shoots = True
                    boss_shot_timer = 0

                if rand_num_start == 1 and rand_num_end == 1:
                    # Fourth attack timer to determine whether attack of fourth type should end or not
                    if boss_fourth_timer >= 180:
                        rand_num_start = 1
                        rand_num_end = 5

                        boss_shot_timer_max = 60
                        if boss.vel_x < 0:
                            boss.vel_x = -5
                        else:
                            boss.vel_x = 5

                        boss_fourth_timer = 0

                    boss_fourth_timer += 1

                if boss.shoots:
                    # Determines what attack type is going to be used
                    if boss.attack_type == 0:
                        boss.attack_type = random.randint(rand_num_start, rand_num_end)

                    # Attack type 1
                    if boss.attack_type == 1:
                        # Setting the coordinates for projectiles
                        boss_shot_x = boss.x + 10
                        boss_shot_y = boss.y + 184
                        for i in range(49):
                            boss_projectiles.append(Projectile(projectile_image, boss_shot_x, boss_shot_y, False, 0, 0, 0))
                            boss_shot_x += 10
                            if boss_shot_x < boss.x + 256:
                                boss_shot_y += 5
                            elif boss_shot_x > boss.x + 256:
                                boss_shot_y -= 5

                        # Firing the projectiles
                        for i in range(len(boss_projectiles)):
                            boss.shoot(boss_projectiles, i)
                            alien_t2_gun_sound.play()

                    # Attack type 2
                    elif boss.attack_type == 2:
                        # Appending the list with projectiles
                        second_type_x = [boss.x + 97, boss.x + 106, boss.x + 121, boss.x + 130, boss.x + 380, boss.x + 389, boss.x + 404, boss.x + 413]
                        second_type_y = [boss.y + 195, boss.y + 200, boss.y + 190, boss.y + 195, boss.y + 195, boss.y + 200, boss.y + 190, boss.y + 195]
                        if boss_projectiles == []:
                            for i in range(256):
                                boss_projectiles.append(Projectile(projectile_image, second_type_x[random.randint(0, 7)], second_type_y[random.randint(0, 7)], False, 0, 0, 0))

                        # Shooting the projectiles and correcting their coordinates
                        for i in range(len(boss_projectiles)):
                            if not boss_projectiles[i].fired and boss_projectile_timer >= 1:
                                second_type_x = [boss.x + 97, boss.x + 106, boss.x + 121, boss.x + 130, boss.x + 380, boss.x + 389, boss.x + 404, boss.x + 413]
                                second_type_y = [boss.y + 195, boss.y + 200, boss.y + 190, boss.y + 195, boss.y + 195, boss.y + 200, boss.y + 190, boss.y + 195]
                                boss_projectiles[i].x = second_type_x[random.randint(0, 7)]
                                boss_projectiles[i].y = second_type_y[random.randint(0, 7)]
                                boss.shoot(boss_projectiles, i)
                                boss_shot_count += 1
                                boss_projectile_timer = 0
                                alien_t2_gun_sound.play()
                                break

                        # Determine if all projectiles are shot
                        if boss_projectiles[-1].fired:
                            boss.salvo_finished = True

                        # Cooldown before shooting
                        for i in range(len(boss_projectiles)):
                            if boss_attack_timer // 2 > 0 and not projectile[i].fired:
                                boss_attack_timer = 0
                                boss_projectile_timer += 1

                        boss_attack_timer += 1

                    # Attack type 3
                    elif boss.attack_type == 3:

                        # Positioning the reticles
                        for i in range(len(boss_reticles)):
                            if not boss_reticles[i].active and not boss_reticles[i].shot:
                                boss_reticles[i].set_coordinates(148, width - 425, 350, height - 276)

                        # Shooting the missile
                        for i in range(len(boss_reticles)):
                            if 0 <= boss.x + 128 - boss_reticles[i].x <= 5 and not boss_reticles[i].shot and not boss_missiles[i].launched:
                                boss_missiles[i].launch(boss_reticles[i].x + 96, boss.y + 289, missile_sound)

                        for i in range(len(boss_missiles)):
                            # Reticle hit
                            if boss_missiles[i].launched and boss_missiles[i].y >= boss_reticles[i].y + 64 and boss_reticles[i].x + 128 <= boss_missiles[i].x + 32 <= boss_reticles[i].x + 133 and not boss_reticles[i].shot:
                                boss_missiles[i].launched = False
                                boss_missiles_amount -= 1
                                boss_reticles[i].shot = True
                                boss_reticles[i].active = False
                                missile_hit.play()
                                if distance(ship.x + 32, boss_reticles[i].x + 128, ship.y + 32, boss_reticles[i].y + 128) <= 160\
                                and ship.alive and not ship.blinking and not ship.jumping:
                                    ship.alive = False
                                    ship.lifes -= 1
                                    ship_explosion_sound.play()

                            # Ship hit
                            if boss_missiles[i].x <= ship.x <= boss_missiles[i].x + 64\
                                and boss_missiles[i].y <= ship.y <= boss_missiles[i].y + 64\
                                and boss_missiles[i].launched and ship.alive and not ship.blinking:
                                ship.alive = False
                                ship.lifes -= 1
                                ship_explosion_sound.play()

                            for i in range(len(boss_missiles)):
                                if not boss_missiles[i].exploded:
                                    boss_missiles_exploded = False
                                    break
                                else:
                                    boss_missiles_exploded = True

                    # Attack type 4
                    elif boss.attack_type == 4:
                        rand_num_start = 1
                        rand_num_end = 1

                        boss_shot_timer_max = 50
                        if boss.vel_x > 0:
                            boss.vel_x = 1
                        else:
                            boss.vel_x = -1

                    # Attack type 5
                    elif boss.attack_type == 5:
                        if boss_projectiles == []:
                            for i in range(256):
                                boss_projectiles.append(Projectile(projectile_image, 0, 0, False, 0, 0, 0))

                        # Shooting the projectiles and correcting their coordinates
                        for i in range(len(boss_projectiles)):
                            if not boss_projectiles[i].fired and boss_projectile_timer >= 1:
                                boss_projectiles[i].x = boss.x + 256
                                boss_projectiles[i].y = boss.y + 289
                                boss.shoot(boss_projectiles, i)
                                boss_shot_count += 1
                                boss_projectile_timer = 0
                                alien_t2_gun_sound.play()
                                break

                        # Determine if all projectiles are shot
                        if boss_projectiles[-1].fired:
                            boss.salvo_finished = True

                        # Cooldown before shooting
                        for i in range(len(boss_projectiles)):
                            if boss_attack_timer // 2 > 0 and not projectile[i].fired:
                                boss_attack_timer = 0
                                boss_projectile_timer += 1

                        boss_attack_timer += 1

                    # Nullification of attack type
                    if (boss_projectiles == [] and boss_missiles_amount <= 0 and boss_missiles_exploded) or boss.attack_type not in [2, 3, 5] or boss.salvo_finished\
                        or (rand_num_start == 1 and rand_num_end == 1):
                        boss.attack_type = 0
                        boss.salvo_finished = False
                        boss_missiles_amount = 5
                        boss.shoots = False

                        for i in range(5):
                            boss_reticles[i] = Reticle(bomber_reticle_large, 0, -500, False, False)
                            boss_missiles[i] = Missile(0, -500, 10, False, 0, False)

        if boss.exploded and not boss.alive and egg_list == []:
            if egg_random == 1:
                egg_list.append(Upgrade(egg_image, silence, 0, 0, False, False, 0, "EGG! RUN!", ship.x - 32, ship.y + 70))
                if not egg_list[0].dropped:
                    mixer.music.stop()
                    egg_list[0].drop(boss, 224, 112)

        # Boss projectiles
        for i in range(len(boss_projectiles)):
            # Movement
            if boss_projectiles[i].fired:
                boss_projectiles[i].move(10, 1)

                # Projectile collision with ship
                if boss_projectiles[i].fired and ship.x <= boss_projectiles[i].x <= ship.x + 64 \
                        and ship.y <= boss_projectiles[i].y <= ship.y + 64 \
                        and ship.alive and not ship.blinking and not ship.jumping:
                    ship.alive = False
                    boss_projectiles[i].fired = False
                    ship.lifes -= 1
                    ship_explosion_sound.play()

        # Boss missiles
        for i in range(len(boss_missiles)):
            # Movement
            if boss_missiles[i].launched:
                boss_missiles[i].fly()

        if not boss.shoots:
            boss_shot_timer += 1

        # Last y list
        aliens_tier2_y_lst = []
        for i in range(aliens_tier2_len):
            aliens_tier2_y_lst.append(aliens_tier2[i].y)

        # Credits
        if not boss.alive:
            # Moving the text
            if show_credits:
                if credits_y >= -1425:
                    credits_y -= 0.5

            # Moving the player
            if (not ship.y < -70 and egg_list == [] and boss.exploded) or (ship.y < -10 and boss.exploded and not egg_list == []):
                ship.put_in_position((width // 2) - 32, -100)
                if not endgame_cutscene:
                    if not egg_list == []:
                        egg_list[0].image = pygame.transform.rotate(egg_list[0].image, -135.00)
                    mixer.music.stop()
                    mixer.music.load("sound/music/endgame.wav")
                    mixer.music.set_volume(1)
                    mixer.music.play()
                endgame_cutscene = True
            if endgame_cutscene:
                show_credits = True
                if egg_list != [] and egg_list[0].x < 1224:
                    egg_list[0].x += 3

        # Egg counter
        if egg_counter >= 35:
            end_everything = True
            run = False

        # Clearing dead tier 1 enemies
        for i in range(aliens_tier1_len):
            if not aliens_tier1[i].alive and aliens_tier1[i].exploded or aliens_tier1[i].y > height:
                aliens_tier1.pop(i)
                aliens_tier1_len -= 1
                break

        # Clearing shot ship projectiles
        for i in range(len(projectile)):
            if projectile[i].y < -10:
                projectile.pop(i)
                break

        # Clearing boss projectiles
        for i in range(len(boss_projectiles)):
            if boss_projectiles[i].y > height + 10 or not boss_projectiles[i].fired:
                boss_projectiles.pop(i)
                break

        # Draws stuff
        draw_things()

while not end_everything:
    if not game_started:
        menu_stuff()
    if game_started:
        main()

if end_everything:
    pygame.quit()
