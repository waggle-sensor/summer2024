from ultralytics import YOLO 


model_fire = YOLO("summer2024/ryan/Datasets/fire_m.pt")

model_yolo = YOLO("summer2024/ryan/Datasets/yolov8n.pt")

inpt = input("Put a link or a downloaded image here: ")
models = [model_fire, model_yolo]
results = []
for model in models:
    result = model(f"{inpt}")
    results.extend(result)

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result1.jpg")  # save to disk

   