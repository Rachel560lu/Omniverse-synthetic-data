import omni.replicator.core as rep

# Function to randomize properties of the luggage group
def randomize_luggage_group():
    group_path = "/scene/Meshes/Sketchfab_model/Luggage_obj_cleaner_materialmerger_gles"
    group_instance = rep.get.prims(path_pattern=group_path)
    
    with group_instance:
        rep.modify.pose(
            #position=rep.distribution.uniform((-100, 0, -100), (100, 0, 100)),  # Randomize position
            rotation=rep.distribution.uniform((0, 0, 0), (0, 360, 0)),          # Randomize rotation
            #scale=rep.distribution.uniform((0.8,0.8,0.8),(1.2,1.2,1.2))
        )
    return group_instance.node            
            
    

# Camera and lighting setup (add your camera and lighting setup here)
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

#camera1 = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length, position=cam_position, rotation=cam_rotation, f_stop=f_stop)
#camera2 = rep.create.camera(focus_distance=focus_distance2, focal_length=focal_length2, position=cam_position2, rotation=cam_rotation2, f_stop=f_stop)

# Render products setup
#render_product1 = rep.create.render_product(camera1, (1024, 1024))
#render_product2 = rep.create.render_product(camera2, (512, 512))

render_product = rep.create.render_product('/scene/Camera', (512,512))

# Set up the writer to specify the output directory
output_dir = r"C:\Users\vipuser\Desktop\generated_dataset\test"
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(output_dir=output_dir, rgb=True, bounding_box_2d_tight=True)
#writer.attach([render_product1, render_product2]) 
writer.attach(render_product)

# Randomize scene and run orchestrator
#randomize_luggage_group()
rep.randomizer.register(randomize_luggage_group)
with rep.trigger.on_frame(num_frames=10):
	rep.randomizer.randomize_luggage_group()
	
rep.orchestrator.run()

print(f"Datasets saved to: {output_dir}")
