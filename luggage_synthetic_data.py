import omni.replicator.core as rep

# Function to randomize properties of the luggage group
def randomize_luggage_group():
    group_path = "/scene/Meshes/Sketchfab_model/Luggage_obj_cleaner_materialmerger_gles"
    group_instance = rep.get_prim_at_path(group_path)
    
    if group_instance:
        with group_instance:
            rep.modify.pose(
                position=rep.distribution.uniform((-100, 0, -100), (100, 0, 100)),  # Randomize position
                rotation=rep.distribution.uniform((0, 0, 0), (0, 360, 0)),          # Randomize rotation
            )

# Camera and lighting setup (add your camera and lighting setup here)

# Set up the writer to specify the output directory
output_dir = r"C:\Users\vipuser\Desktop\generated_dataset"
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(output_dir=output_dir)

# Randomize scene and run orchestrator
randomize_luggage_group()
rep.orchestrator.run()

print(f"Datasets saved to: {output_dir}")
