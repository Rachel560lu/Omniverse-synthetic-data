 import omni.replicator.core as rep
import omni.usd
import omni.kit

# Create a new stage
stage = omni.usd.get_context().new_stage()

# Lightning setup for Rectangular light and Dome light 
def rect_lights(num=2):
    lights = rep.create.light(
        light_type="rect",
        temperature=rep.distribution.normal(6500, 500),
        intensity=rep.distribution.normal(0, 5000),
        position=(-131,150,-134),
        rotation=(-90,0,0),
        scale=rep.distribution.uniform(50, 100),
        count=num
    )
    return lights.node

def dome_lights(num=1):
    lights = rep.create.light(
        light_type="dome",
        temperature=rep.distribution.normal(6500, 500),
        intensity=rep.distribution.normal(0, 1000),
        position=(0,0,0),
        rotation=(270,0,0),
        count=num
    )
    return lights.node

# Define the paths to the USD files
TABLE_USD = r"C:\Users\vipuser\Desktop\source\Desk.usd"  # Converted from Desk.fbx to Desk.usd
FORK_USD = r"C:\Users\vipuser\Desktop\source\fork.usd"  # Converted from fork.fbx to fork.usd

# Function to import and position the table
def table():
    table = rep.create.from_usd(TABLE_USD, semantics=[('class', 'table')])
    with table:
        rep.modify.pose(
            position=(-135.39745, 0, -140.25696),
            rotation=(0, 0, 0),
        )
    return table

# Function to import and position the fork
def fork():
    fork = rep.create.from_usd(FORK_USD, semantics=[('class', 'fork')])
    with fork:
        rep.modify.pose(
            position=(0, 0, 0),  # Adjust position as needed
            rotation=(0, 0, 0),  # Adjust rotation as needed
        )
    return fork

# Camera setup
focus_distance = 50
focal_length = 35
cam_position = (10, 10, 10)
cam_rotation = (0, 0, 0)
f_stop = 2.8

focus_distance2 = 70
focal_length2 = 50
cam_position2 = (20, 20, 20)
cam_rotation2 = (10, 10, 10)

camera1 = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length, position=cam_position, rotation=cam_rotation, f_stop=f_stop)
camera2 = rep.create.camera(focus_distance=focus_distance2, focal_length=focal_length2, position=cam_position2, rotation=cam_rotation2, f_stop=f_stop)

# Render products setup
render_product1 = rep.create.render_product(camera1, (1024, 1024))
render_product2 = rep.create.render_product(camera2, (512, 512))

# Function to randomize cutlery props (if needed)
current_cutlery = r"C:\Users\vipuser\Desktop\source\fork.usd"  # Use raw string for the path

def cutlery_props(size=5):
    cutlery_files = rep.utils.get_usd_files(current_cutlery)
    print(f"Cutlery files found: {cutlery_files}")  # Debugging line to check the files found
    instances = rep.randomizer.instantiate(cutlery_files, size=size, mode='point_instance')
    with instances:
        rep.modify.pose(
            position=rep.distribution.uniform((-212, 76.2, -187), (-62, 76.2, -94)),
            rotation=rep.distribution.uniform((-90, -180, 0), (-90, 180, 0)),
        )
    return instances.node

# Function to load and position both objects
def load_scene():
    table()
    fork()

# Trigger the randomizations
with rep.trigger.on_frame(num_frames=50):
    load_scene()
    rect_lights(1)
    dome_lights(1)
    cutlery_props(5)
