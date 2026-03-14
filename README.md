# ESP32-CAM Object Recognition

This project contains two components for an end-to-end Object Recognition system:
1. **ESP32-CAM Firmware**: Captures video from an AI Thinker ESP32-CAM board and serves it over WiFi as a Motion JPEG (MJPEG) stream.
2. **Python Server**: Connects to the ESP32-CAM stream and runs real-time object detection using a lightweight YOLOv8 model.

## Folder Structure
- `/esp32_app/`: PlatformIO project for the ESP32-CAM.
- `/server/`: Python scripts and `requirements.txt` for the detection server.

## Hardware Required
- AI Thinker ESP32-CAM board
- FTDI Programmer (to upload code to ESP32-CAM)
- USB Camera (Optional, for testing YOLO locally without ESP32)

---

## 1. Setup the ESP32-CAM

1. Open the `/esp32_app` folder in VS Code with the **PlatformIO** extension installed.
2. In `esp32_app/src/main.cpp`, modify the following lines with your WiFi network credentials:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
3. Connect your ESP32-CAM to your PC via an FTDI programmer. Remember to jump GPIO 0 to GND when programming.
4. Click the **Upload** button in PlatformIO.
5. Once uploaded, remove the jumper from GPIO 0 to GND, open the **Serial Monitor** (115200 baud), and press the Reset button on the ESP32-CAM.
6. The Serial Monitor will print out the IP address assigned to the ESP32 once it connects to your WiFi. Note this IP address down (e.g., `192.168.1.100`).

---

## 2. Setup the Python Server

1. Open a terminal and navigate to the `/server` folder:
   ```bash
   cd server
   ```
2. Create and activate a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Open `/server/main.py` and update the `ESP32_IP` variable with the IP address you noted from the ESP32-CAM Serial Monitor:
   ```python
   ESP32_IP = "192.168.1.100"
   ```
5. Run the detection script:
   ```bash
   python main.py
   ```
6. A window will open displaying the live feed from your ESP32-CAM with YOLOv8 object detection bounding boxes drawn over it. Press `q` to close the window.
