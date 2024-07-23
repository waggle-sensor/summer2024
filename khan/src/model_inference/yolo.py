from ultralytics import YOLO, YOLOv10

model_v8n, model_v10 = YOLO("yolov8n.pt"), YOLOv10.from_pretrained('jameslahm/yolov10t')

# perform object detection on the same image
image = "https://ultralytics.com/images/bus.jpg"
results_v8n, results_v10 = model_v8n(image), model_v10(image)

# output objects detected and the confidence scores
print("YOLOv8n output:")
for obj in results_v8n.names:
    print(f"{obj}: {results_v8n[obj].tolist()}")

print("\nYOLOv10 output:")
for obj in results_v10.names:
    print(f"{obj}: {results_v10[obj].tolist()}")

success_v10 = model_v10.export(format="onnx")
