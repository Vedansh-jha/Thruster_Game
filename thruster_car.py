import pygame
import math

thrust_effect = 10
gravity_constant = 9.8
angle = 0
angular_velocity = 0
thruster_center = ()
force_center = [0, 0]
force_left = [0, 0]
force_right = [0, 0]

def platform_collision():
    global center_y

    for x, y, w, h in platforms:

        platform_top = y
        ship_bottom = center_y + RECT_H/2

        if (
            x <= center_x <= x + w
            and
            ship_bottom >= platform_top
            and
            ship_bottom <= platform_top + 20
        ):
            center_y = platform_top - RECT_H/2
            return True

    return False


def on_ground():
    global center_y, GROUND_Y
    if center_y >= GROUND_Y:
        return True
    else:
        return False

def net_effect():
    global center_x, center_y
    global force_center, force_left, force_right
    global angle, angular_velocity

    vector_x = force_center[0] + force_left[0] + force_right[0]
    vector_y = force_center[1] + force_left[1] + force_right[1]

    torque = force_left[1] - force_right[1]

    alpha = torque / 50

    angular_velocity += alpha
    angular_velocity *= 0.98

    angle += angular_velocity

    center_x -= vector_x
    center_y -= vector_y

    force_center[0] = 0
    force_center[1] = 0

    force_left[0] = 0
    force_left[1] = 0

    force_right[0] = 0
    force_right[1] = 0

def main_booster():
    global center_y, center_x, angle, force_center

    rad = math.radians(angle)
    # center_y - thrust_effect * math.cos(-rad)
    # center_x = center_x - thrust_effect * math.sin(-rad)
    force_center[0] = thrust_effect * math.sin(-rad)
    force_center[1] = thrust_effect * math.cos(-rad)

def left_booster():
    global center_y, center_x, angle, force_left

    rad = math.radians(angle)
    # center_y - thrust_effect * math.cos(-rad)
    # center_x = center_x - thrust_effect * math.sin(-rad)
    force_left[0] = thrust_effect * math.sin(-rad - math.pi/4)
    force_left[1] = thrust_effect * math.cos(-rad - math.pi/4)
    print(force_left[0], " ", force_left[1])

def right_booster():
    global center_y, center_x, angle, force_right

    rad = math.radians(angle)
    # center_y - thrust_effect * math.cos(-rad)
    # center_x = center_x - thrust_effect * math.sin(-rad)
    force_right[0] = thrust_effect * math.sin(-rad + math.pi/4)
    force_right[1] = thrust_effect * math.cos(-rad + math.pi/4)
    # print(force_right[0], " ", force_right[1])

def gravity():
    global center_x, center_y, GROUND_Y, base
    if center_y >= base:
        return
    else:
        center_y = center_y + gravity_constant

def draw_car(angle):
    global RECT_W, RECT_H, center_x, center_y, thruster_center

    r = math.sqrt((RECT_W/2)**2 + (RECT_H/2)**2)
    center_thruster_distance = RECT_H/2

    phi = math.atan2(RECT_H/2, RECT_W/2)

    rad = math.radians(angle)

    a = (
        center_x + r * math.cos(rad + math.pi - phi),
        center_y + r * math.sin(rad + math.pi - phi)
    )

    b = (
        center_x + r * math.cos(rad + phi),
        center_y + r * math.sin(rad + phi)
    )

    c = (
        center_x + r * math.cos(rad - phi),
        center_y + r * math.sin(rad - phi)
    )

    d = (
        center_x + r * math.cos(rad + math.pi + phi),
        center_y + r * math.sin(rad + math.pi + phi)
    )

    thruster_center = (center_x + center_thruster_distance * math.cos(rad + math.pi/2), 
                        center_y + center_thruster_distance * math.sin(rad + math.pi/2)
                    )
    # print(f"Thruster x - {thruster_center[0]}, Thruster y - {thruster_center[1]}")

    pygame.draw.polygon(screen, WHITE, [a, b, c, d])

def draw_booster(id):
    global rect_x, RECT_W, RECT_H, rect_y, thruster_center, angle

    x = 0
    offset = [0, RECT_W / 2, -RECT_W / 2]

    x = offset[id]


    rad = math.radians(angle)
    # pos_x = center_x + RECT_W // 2
    # pos_x = thruster_center[0] + x
    # nozzle_y = center_y + RECT_H/2
    # nozzle_y = thruster_center[1] 

    pos_x = (
    thruster_center[0]
    + x * math.cos(rad)
    )

    nozzle_y = (
        thruster_center[1]
        + x * math.sin(rad)
    )  

    # Main exhaust
    pygame.draw.line(
        screen,
        BLUE,
        (pos_x, nozzle_y),
        (pos_x + 40 * math.cos(rad + math.pi/2), nozzle_y + 40 * math.sin(rad + math.pi/2)),
        6
    )
  
        # Side streaks
    r = math.sqrt(10**2 + 30**2)
    phi = math.atan2(10, 30)
    pygame.draw.line(
        screen,
        BLUE,
        (pos_x - 5, nozzle_y),
        (pos_x + r * math.cos(rad + math.pi/2 + phi), nozzle_y + r * math.sin(rad + math.pi/2 + phi)),
        2
    )

    pygame.draw.line(
        screen,
        BLUE,
        (pos_x + 5, nozzle_y),
        (pos_x + r * math.cos(rad + math.pi/2 - phi), nozzle_y + r * math.sin(rad + math.pi/2 - phi)),
        2
    )


        

pygame.init()

WIDTH, HEIGHT = 2000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)

GROUND_Y = HEIGHT - 100
GROUND_X = WIDTH/2

platforms = [
    (150, 450, 200, 15),
    (500, 350, 200, 15),
    (900, 250, 250, 15),
    (1300, 400, 200, 15),
    (1700, 300, 250, 15)
]

RECT_W = 160
RECT_H = 80

rect_x = (WIDTH - RECT_W) // 2
rect_y_original = GROUND_Y - RECT_H
rect_y = GROUND_Y - RECT_H - 20

base = GROUND_Y - RECT_H/2
center_x = GROUND_X
center_y = base

center_boost_active = False
left_boost_active = False
right_boost_active = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_s):
                center_boost_active = True
            if(event.key == pygame.K_a):
                left_boost_active = True
            if(event.key == pygame.K_d):
                right_boost_active = True

        elif event.type == pygame.KEYUP:
            if(event.key == pygame.K_s):
                center_boost_active = False
            if(event.key == pygame.K_a):
                left_boost_active = False
            if(event.key == pygame.K_d):
                right_boost_active = False

    if center_boost_active: 
        main_booster()
    if left_boost_active: 
        left_booster()
    if right_boost_active: 
        right_booster()
    net_effect()
        
    # if not on_ground():
    if not platform_collision():
        gravity()

    if center_y > base:
        center_y = base

    screen.fill(BLACK)

    # Ground
    pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    for platform in platforms:
        pygame.draw.rect(
            screen,
            WHITE,
            platform
        )
    
    draw_car(angle)

    # Block
    # rect_surface = pygame.Surface((RECT_W, RECT_H), pygame.SRCALPHA)
    # rect_surface.fill(WHITE)

    # rotated_surface = pygame.transform.rotate(rect_surface, angle)

    # rotated_rect = rotated_surface.get_rect(
    #     center=(rect_x + RECT_W / 2,
    #             rect_y + RECT_H / 2)
    # )

    # screen.blit(rotated_surface, rotated_rect)

    if center_boost_active:
        draw_booster(0)
    if left_boost_active: 
        draw_booster(2)
    if right_boost_active: 
        draw_booster(1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()