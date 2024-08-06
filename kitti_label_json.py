import os
import json
import argparse
from PIL import Image

OUT_LABELS_DIR = "labels"

KEY_PEDESTRIAN = "Pedestrian"
KEY_CYCLIST = "Cyclist"
KEY_CAR = "Car"
KEY_DONT_CARE = "DontCare"

CLAZZ_NUMBERS = {
    KEY_PEDESTRIAN: 0,
    KEY_CYCLIST: 1,
    KEY_CAR: 2,
    KEY_DONT_CARE: 3
}

def get_sample_id(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]

def resolve_clazz_number_or_none(clazz, use_dont_care):
    if clazz == KEY_CYCLIST:
        return CLAZZ_NUMBERS[KEY_CYCLIST]
    if clazz == KEY_PEDESTRIAN:
        return CLAZZ_NUMBERS[KEY_PEDESTRIAN]
    if clazz == KEY_CAR:
        return CLAZZ_NUMBERS[KEY_CAR]
    if use_dont_care and clazz == KEY_DONT_CARE:
        return CLAZZ_NUMBERS[KEY_DONT_CARE]
    return None

def convert_to_yolo_bbox(bbox, size):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (bbox[0] + bbox[1]) / 2.0
    y = (bbox[2] + bbox[3]) / 2.0
    w = bbox[1] - bbox[0]
    h = bbox[3] - bbox[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def read_real_image_size(img_path):
    return Image.open(img_path).size

def parse_sample(lbl_path, img_path, use_dont_care):
    with open(lbl_path) as json_file:
        data = json.load(json_file)
        yolo_labels = []
        print(f"Data from {lbl_path}: {data}")  # Debug: Check JSON structure
        
        if isinstance(data, dict):
            items = data.items()
        elif isinstance(data, list):
            items = enumerate(data)
        else:
            print(f"Unexpected data type in {lbl_path}")
            return yolo_labels

        for obj_id, obj in items:
            print(f"Object ID: {obj_id}, Object: {obj}")  # Debug: Check each object
            if isinstance(obj, dict):  # Ensure obj is a dictionary
                clazz_number = resolve_clazz_number_or_none(obj.get('class'), use_dont_care)
                if clazz_number is not None:
                    size = read_real_image_size(img_path)
                    bbox = (
                        float(obj["bbox2_left"]),
                        float(obj["bbox2_right"]),
                        float(obj["bbox2_top"]),
                        float(obj["bbox2_bottom"])
                    )
                    yolo_bbox = convert_to_yolo_bbox(bbox, size)
                    yolo_label = (clazz_number,) + yolo_bbox
                    yolo_labels.append(yolo_label)
            else:
                print(f"Skipping non-dictionary object: {obj}")
    return yolo_labels

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generates labels for training darknet on KITTI.")
    parser.add_argument("label_dir", help="Directory containing the JSON label files.")
    parser.add_argument("image_2_dir", help="Directory containing the image files.")
    parser.add_argument("--training-samples", type=float, default=0.8, help="Percentage of the samples to be used for training between 0.0 and 1.0.")
    parser.add_argument("--use-dont-care", action="store_true", help="Include 'DontCare' labels.")
    args = parser.parse_args()
    if args.training_samples < 0 or args.training_samples > 1:
        print("Invalid argument for --training-samples. Expected a percentage value between 0.0 and 1.0.")
        exit(-1)
    return args

def main():
    args = parse_arguments()

    if not os.path.exists(OUT_LABELS_DIR):
        os.makedirs(OUT_LABELS_DIR)

    print("Generating darknet labels...")
    sample_img_paths = []
    for dir_path, _, files in os.walk(args.label_dir):
        for file_name in files:
            if file_name.endswith(".json"):
                lbl_path = os.path.join(dir_path, file_name)
                sample_id = get_sample_id(lbl_path)
                img_path = os.path.join(args.image_2_dir, f"{sample_id}.png")
                sample_img_paths.append(img_path)
                yolo_labels = parse_sample(lbl_path, img_path, args.use_dont_care)
                with open(os.path.join(OUT_LABELS_DIR, f"{sample_id}.txt"), "w") as yolo_label_file:
                    for lbl in yolo_labels:
                        yolo_label_file.write(f"{lbl[0]} {lbl[1]} {lbl[2]} {lbl[3]} {lbl[4]}\n")

    print("Writing training and test sample ids...")
    first_test_sample_index = int(args.training_samples * len(sample_img_paths))
    with open("kitti_train.txt", "w") as train_file:
        for sample_index in range(first_test_sample_index):
            train_file.write(f"{sample_img_paths[sample_index]}\n")
    with open("kitti_test.txt", "w") as test_file:
        for sample_index in range(first_test_sample_index, len(sample_img_paths)):
            test_file.write(f"{sample_img_paths[sample_index]}\n")

if __name__ == "__main__":
    main()
