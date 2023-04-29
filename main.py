
from ursina import *
from ursina.shaders import lit_with_shadows_shader
def sinus(value): return math.sin(math.radians(value))              # make a sin function that works with degrees
def cosinus(value): return math.cos(math.radians(value))            # same for cos
def dist(a_pos, b_pos): return math.sqrt((b_pos[0] - a_pos[0]) ** 2 + (b_pos[1] - a_pos[1]) ** 2 + (b_pos[2] - a_pos[2]) ** 2)

'=================================================================='

app = Ursina()
window.fullscreen = True
aspect = window.aspect_ratio
ec = EditorCamera()

# generic sky Entity
sky = Sky()

# make some ground
#ground = Entity(model='circle', texture='grass', rotation=(90, 0, 0), scale=100, position=(0, -1.5, 0), collider='mesh')           # no shader so that fog can work.
ground = Entity(model='crat', tecture='crat_img', rotation=(0, 0, 0), scale=100, position=(0, -10.5, 0))           # no shader so that fog can work.

# make the crane
base = Entity(model='base', texture="TEXTURE_SET", scale=1, collider='mesh')
fork = Entity(model='fork', texture="TEXTURE_SET", scale=1, collider='mesh', parent=base)
arm = Entity(model='arm', texture="TEXTURE_SET", scale=1, collider='box', parent=fork)
cub = Entity(model='cube', texture="grass", scale=0.5, collider='mesh', parent=arm, position=(10, -0.5, 0))

'=================================================================='
# make some ui elements
other_meter = Entity(parent=camera.ui, model='quad', scale=(.075, .5), texture='TEXTURE_SET', position=(0.475 * window.aspect_ratio, -0.25))
part_meter = Text(parent=camera.ui, position=(0.38*aspect, 0.1, -0.01), text="Hello: ", color=color.green)
base.bricks = []

'**********************************************************************************************************************'
def update():

    """Objects Update"""
    base.bricks.append(Entity(model='cube', color=(fork.rotation_y*0.0000008, 0, cosinus(fork.rotation_y), 0.2), scale=0.5, collider='mesh',  position=cub.world_position, world_rotation=cub.world_rotation))

    fork.rotation_y -= 2+2*sinus(-arm.rotation_z)
    if fork.rotation_y > -360: fork.rotation_y += 360

    arm.rotation_z -= 0.05 + 0.1*sinus(-arm.rotation_z)
    if arm.rotation_z <= -90:
        if not base.bricks[-1].world_y < 0:
            for brick in base.bricks:
                brick.world_y -= 0.2
                brick.world_x *= 1.01
                brick.world_z *= 1.01

        else:
            arm.rotation_z += 90
            for brick in base.bricks: destroy(brick)

            base.bricks.clear()

    """UI Update"""
    part_meter.text = "pt count is : " + str(len(base.bricks))


app.run()
