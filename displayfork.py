import omni.replicator.core as rep
import omni.usd
import omni.kit

# Create a new stage
stage = omni.usd.get_context().new_stage()

# Define the path to the fork file
FORK_USD = r"C:\Users\vipuser\Desktop\source\fork.fbx"  # Ensure the path is correct

# Import and position the fork object
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

camera = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length, position=cam_position, rotation=cam_rotation, f_stop=f_stop)

# Will render 1024x1024 images
render_product = rep.create.render_product(camera, (1024, 1024))

# Function to load the fork
fork()
