import cv2
import requests
import numpy as np
from ultralytics import YOLO

# ===========================
# Configuration
# ===========================
# Replace with the ESP32 IP address printed on the Serial Monitor
ESP32_IP = "192.168.1.100"
STREAM_URL = f"http://{ESP32_IP}:81/stream"

def main():
    print(f"Loading YOLO model...")
    # Load YOLOv8 model (downloads 'yolov8n.pt' on first run)
    model = YOLO("yolov8n.pt") 

    print(f"Connecting to ESP32 stream at {STREAM_URL}")
    try:
        # We use short timeout for initial connection, but stream is infinite
        res = requests.get(STREAM_URL, stream=True, timeout=5)
    except Exception as e:
        print(f"Failed to connect to stream: {e}")
        return

    if res.status_code != 200:
        print(f"Failed to fetch stream. Status code: {res.status_code}")
        return

    bytes_data = bytes()
    for chunk in res.iter_content(chunk_size=1024):
        bytes_data += chunk
        
        # JPEG start and end signatures
        a = bytes_data.find(b'\xff\xd8')
        b = bytes_data.find(b'\xff\xd9')
        
        if a != -1 and b != -1:
            # We have a full frame
            jpg = bytes_data[a:b+2]
            bytes_data = bytes_data[b+2:]
            
            # Decode the JPEG into an OpenCV image
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            if frame is not None:
                # Run YOLOv8 object detection
                results = model(frame, verbose=False)
                
                # Render results on the frame
                annotated_frame = results[0].plot()
                
                # Display the frame
                cv2.imshow("ESP32-CAM Object Detection", annotated_frame)
                
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
