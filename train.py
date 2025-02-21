from ultralytics import YOLO


model = YOLO("yolo11n.pt")

train_results = model.train(
    data="data.yaml",  
    epochs=80, 
    imgsz=640,  
    device="cpu", 
)

metrics = model.val()

results = model("cit.jpg")
results[0].show()

path = model.export(format="onnx")  