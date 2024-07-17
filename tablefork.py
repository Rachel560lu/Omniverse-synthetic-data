import omni.replicator.core as rep
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
    
    
    # Import and position the table object

def table():
    table = rep.create.from_usd(TABLE_USD, semantics=[('class', 'table')])

    with table:
        rep.modify.pose(
            position=(-135.39745, 0, -140.25696),
            rotation=(0,-90,-90),
        )
    return table
    
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

    
# Will render 1024x1024 images and 512x512 images
render_product  = rep.create.render_product(camera1, (1024, 1024))
render_product2  = rep.create.render_product(camera2, (512, 512))


def cutlery_props(size=5):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(current_cultery), size=size, mode='point_instance')

        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-212, 76.2, -187), (-62, 76.2, -94)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return instances.node

with rep.trigger.on_frame(num_frames=50):
    rep.randomizer.table()
    rep.randomizer.rect_lights(1)
    rep.randomizer.dome_lights(1)
    rep.randomizer.cutlery_props(5)

table()
