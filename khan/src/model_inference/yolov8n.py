from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("https://ultralytics.com/images/bus.jpg")

for obj in results.names:
    print(f"{obj}: {results[obj].tolist()}")

success = model.export(format="onnx")
