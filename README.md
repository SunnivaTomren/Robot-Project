# Robot Project – "Dumb Servant"
<h3>
In this Robot Project, the robot will act as a "Dumb Servant", meaning the robot will drive around and serve people chocolate.  
The goal of this project is to learn how to use a Raspberry Pi 4B to create an autonomous servant robot, by using diffrent sensors, electronics and programming.
</h3>

 ## Software Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd robotproject
```

### 2. Install Dependencies

Connect to your Raspberry Pi via SSH:
```bash
ssh pi@<your-raspberry-pi-ip>
```

Install the required Python packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-picamera2 i2c-tools

# Install Python dependencies
pip3 install flask mediapipe opencv-python adafruit-circuitpython-pca9685
```

### 3. Enable I2C and Camera

Enable I2C and Camera interfaces on your Raspberry Pi:
```bash
sudo raspi-config
```
Navigate to:
- Interface Options > I2C > Enable
- Interface Options > Camera > Enable

Reboot after making these changes:
```bash
sudo reboot
```

## Running the Project

### 1. Start the Machine Vision Server

The machine vision component runs a Flask server that streams the camera feed with pose detection:

```bash
python3 MachineVision.py
```

This will start a web server at `http://<your-raspberry-pi-ip>:5000`. You can view the camera feed with pose detection in your web browser.

### 2. Control the Servo

The servo control script demonstrates basic movement patterns:

```bash
python3 Servo1.py
```

This will run through a sequence of servo positions:
- Center position (1500μs pulse)
- Minimum position (500μs pulse, ~0°)
- Center position (1500μs pulse, ~90°)
- Maximum position (2500μs pulse, ~180°)
- Returns to center

More complex scripts will be added to readme when finished

## The Robots functionality 

### Machine Vision
<p>
The robot uses machine vision to identify a person.  
To achieve this, I will use a combination of OpenCV and YOLO for real-time person detection. 
By using YOLO the robot can also detect where every bodypart including nose, eyes and mouth on the person, by using this we can know when a person "raises it's hand", meaning "I want a chocolate".
</p> 

## Approaching and Serving function

- The robot is equipped with DC-motors to move around autonomously int he room using distance measurement to avoid conflicts.  
- By default, it will roam randomly around the room until it recognizes a person.
- Once a person is detected, the robot will:
  1. Approach the person, maintaining a safe distance using distance measurement sensors.
  2. If the person raises their hand, the robot will serve a piece of chocolate.
- The chocolate is stored in a bag/container (3D-printed mounted on the robot. 
- Using servo motors and sensors, the robot will reach for a piece of chocolate in it's bag/container, and then present the chocolate to the person.
- Once the person takes the chocolate, the robot continous to default mode.

## Componets used
<p>
To build this robot, you will need the following components.  
Each part serves an important role in allowing the robot to see, move, and interact with people.
</p>

### Core Components
- Raspberry Pi 4 Model B (2 GB RAM) — acts as the brain of the robot, running all AI and control logic.  
- MicroSD card — stores the operating system and project files.  
- Power supply (5 V / 3 A) — provides stable power to the Raspberry Pi and connected components.

### Machine Vision
- Python — programming language used to control all modules.  
- OpenCV — enables computer vision and image processing.  
- YOLO (You Only Look Once) — detects people and objects in real time.

### Motion & Control
- L298N Motor Driver — allows the Raspberry Pi to control DC motors for forward, reverse, and turning motion.  
- DC Motors — drive the wheels to move the robot around.  
- Wheels + Chassis — provide physical support and mobility. (3D-models in solidworks/blender)
- PCA9685 Servo Controller — controls multiple servo motors using PWM signals.  
- Servo Motors (MG90S) — move the robot’s arm to serve chocolate.

### Sensors
- Ultrasonic Distance Sensor (HC-SR04) — measures distance to keep a safe gap between the robot and a person.  
- Camera Module — captures video for person detection with YOLO and OpenCV.

### Power & Electronics
- Battery pack / Power bank — powers the robot when not connected to an outlet.  
- Jumper wires & Breadboard — used for connecting all components and testing circuits.

### Mechanical / Physical
- Chocolate container or bag — holds chocolates for serving.  
- Arm mechanism — delivers the chocolate using servo-controlled movement.


