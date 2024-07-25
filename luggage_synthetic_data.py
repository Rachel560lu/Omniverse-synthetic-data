import omni.replicator.core as rep

camera_positions = [
    (-500, 200, -500),
    (500, 500, 500),
    (0, 300, 0),
    (250, 400, -200),
    (-300, 250, 100)
]
            
# Create a camera with initial setup
camera = rep.create.camera(focus_distance=200, f_stop=0.5)
# Create a render product with the camera
render_product = rep.create.render_product(camera, (1024, 1024))



#render_product = rep.create.render_product('/scene/Camera', (512,512))

# Set up the writer to specify the output directory
output_dir = r"C:\Users\vipuser\Desktop\generated_dataset\test2"
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(output_dir=output_dir, rgb=True, bounding_box_2d_tight=True)
#writer.attach([render_product1, render_product2]) 
writer.attach(render_product)

# Randomize scene and run orchestrator
#randomize_luggage_group()
#rep.randomizer.register(randomize_luggage_group)
with rep.trigger.on_frame(num_frames=50):
    with camera:
        rep.modify.pose(
            position=rep.distribution.choice(camera_positions),  # Randomize position
            look_at=(0, 0, 0)  # Assuming the camera looks at the origin (0,0,0)
        )
        
rep.orchestrator.run()

print(f"Datasets saved to: {output_dir}")
