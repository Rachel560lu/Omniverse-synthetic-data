import omni.replicator.core as rep

# Define the uniform distribution for camera positions
# The camera will be placed randomly within the defined ranges for x, y, z
position_distribution = rep.distribution.uniform((-1000, 200, -1000), (1000, 1000, 1000))

# Create a new layer
with rep.new_layer():

    # Create camera with random position
    camera = rep.create.camera(focus_distance=200, f_stop=0.5)

    # Add Default Light
    distance_light = rep.create.light(rotation=(315, 0, 0), intensity=3000, light_type="distant")

    # Create a cube object
    cube = rep.create.cube(semantics=[('class', 'cube')], position=(0, 0, 0))

    # Create a render product linked to the camera
    render_product = rep.create.render_product(camera, (1024, 1024))

    # Initialize and attach writer for output
    output_dir = r"C:\Users\vipuser\Desktop\generated_dataset"
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir=output_dir, rgb=True, bounding_box_2d_tight=True)
    writer.attach([render_product])

    # Randomize camera position for each frame using uniform distribution
    with rep.trigger.on_frame(num_frames=50):
        with camera:
            rep.modify.pose(
                position=position_distribution,  # Randomize position using uniform distribution
                look_at=(0, 0, 0)  # Assuming the camera looks at the origin (0, 0, 0)
            )

# Run the orchestrator (if necessary)
# rep.orchestrator.run()

print(f"Datasets saved to: {output_dir}")
