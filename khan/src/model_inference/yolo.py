from ultralytics import YOLO

model_v8n = YOLO("yolov8n.pt")

# perform object detection on the same image
image = "https://ultralytics.com/images/bus.jpg"
results_v8n = model_v8n(image)

# output objects detected and the confidence scores
print("YOLOv8n output:")
for obj in results_v8n.names:
    print(f"{obj}: {results_v8n[obj].tolist()}")


# success_v10 = model_v10.export(format="onnx")
