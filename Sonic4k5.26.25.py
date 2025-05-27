from ursina import *
import math

class Sonic(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Body
        self.body = Entity(parent=self, model='sphere', color=color.blue, scale=0.8, position=(0, 0, 0))
        # Head
        self.head = Entity(parent=self, model='sphere', color=color.blue, scale=1.0, position=(0, 1.0, 0))
        # Arms
        self.left_arm = Entity(parent=self, model='cube', color=color.blue, scale=(0.2, 0.5, 0.2), position=(-0.5, 0.5, 0))
        self.right_arm = Entity(parent=self, model='cube', color=color.blue, scale=(0.2, 0.5, 0.2), position=(0.5, 0.5, 0))
        # Legs
        self.left_leg = Entity(parent=self, model='cube', color=color.blue, scale=(0.2, 0.5, 0.2), position=(-0.3, -0.5, 0))
        self.right_leg = Entity(parent=self, model='cube', color=color.blue, scale=(0.2, 0.5, 0.2), position=(0.3, -0.5, 0))
        # Shoes
        self.left_shoe = Entity(parent=self, model='cube', color=color.red, scale=(0.3, 0.1, 0.3), position=(-0.3, -1.0, 0))
        self.right_shoe = Entity(parent=self, model='cube', color=color.red, scale=(0.3, 0.1, 0.3), position=(0.3, -1.0, 0))
        # Spikes on head
        self.spike1 = Entity(parent=self.head, model='cone', color=color.blue, scale=(0.3, 0.6, 0.3), position=(0, 0.3, -0.5), rotation=(30, 0, 0))
        self.spike2 = Entity(parent=self.head, model='cone', color=color.blue, scale=(0.3, 0.6, 0.3), position=(-0.2, 0.3, -0.5), rotation=(30, -15, 0))
        self.spike3 = Entity(parent=self.head, model='cone', color=color.blue, scale=(0.3, 0.6, 0.3), position=(0.2, 0.3, -0.5), rotation=(30, 15, 0))
        # Facial features
        self.left_eye = Entity(parent=self.head, model='sphere', color=color.white, scale=0.1, position=(-0.15, 0.1, 0.4))
        self.right_eye = Entity(parent=self.head, model='sphere', color=color.white, scale=0.1, position=(0.15, 0.1, 0.4))
        self.nose = Entity(parent=self.head, model='sphere', color=color.black, scale=0.05, position=(0, 0, 0.5))
        self.velocity = Vec3(0, 0, 0)
        self.on_ground = True

app = Ursina()

# Constants for physics and movement
acceleration = 20  # units per second squared
max_speed = 10  # units per second
deceleration = 10  # units per second squared
jump_velocity = 5  # units per second
gravity = 9.8  # units per second squared

# Player entity
player = Sonic(position=(0, 0, 0))

# Camera setup to follow the player
camera.position = player.position - player.forward * 10 + Vec3(0, 5, 0)
camera.look_at(player)

# UI element - Start button near the top center
start_button = Button(text='Start Game', scale=0.1, position=(0, 0.9))
game_started = False

def start_game():
    global game_started
    game_started = True
    start_button.visible = False
    print("Game started!")

start_button.on_click = start_game

# Ground for reference
ground = Entity(model='plane', scale=(10, 1, 10), color=color.green, position=(0, -1, 0))

def update():
    if not game_started:
        return

    # Handle horizontal movement
    input_dir = Vec2(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s'])
    if input_dir.length() > 0:
        input_dir = input_dir.normalized()
        acceleration_vector = Vec3(input_dir.x, 0, input_dir.y) * acceleration
        player.velocity += acceleration_vector * time.dt

        # Cap horizontal speed
        horizontal_speed = (player.velocity.x**2 + player.velocity.z**2)**0.5
        if horizontal_speed > max_speed:
            ratio = max_speed / horizontal_speed
            player.velocity.x *= ratio
            player.velocity.z *= ratio
    else:
        # Decelerate
        horizontal_velocity = Vec2(player.velocity.x, player.velocity.z)
        speed = horizontal_velocity.length()
        if speed > 0:
            decel = min(deceleration * time.dt, speed)
            direction = horizontal_velocity.normalized()
            player.velocity.x -= direction.x * decel
            player.velocity.z -= direction.y * decel

    # Apply gravity
    if not player.on_ground:
        player.velocity.y -= gravity * time.dt

    # Update position
    player.position += player.velocity * time.dt

    # Check collision with ground
    if player.position.y <= 0:
        player.position.y = 0
        player.velocity.y = 0
        player.on_ground = True
    else:
        player.on_ground = False

    # Rotate player to face movement direction
    horizontal_speed = (player.velocity.x**2 + player.velocity.z**2)**0.5
    if horizontal_speed > 0:
        player.rotation_y = math.degrees(math.atan2(player.velocity.x, player.velocity.z))

    # Update camera to follow the player
    camera.position = player.position - player.forward * 10 + Vec3(0, 5, 0)
    camera.look_at(player)

def input(key):
    if key == 'space' and player.on_ground:
        player.velocity.y = jump_velocity

app.run()
