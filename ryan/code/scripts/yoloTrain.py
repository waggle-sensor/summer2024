from ultralytics import YOLO 


model_fire = YOLO("Datasets/fire_l.pt")

model_yolo = YOLO("Datasets/yolov8n.pt")


models = [model_fire, model_yolo]
results = []
for model in models:
    result = model("https://blog.piercecountywa.gov/pcsdblotter/files/2023/06/Capture-1024x537.jpg")
    results.extend(result)

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk

   