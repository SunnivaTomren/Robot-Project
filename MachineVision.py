# pose_stream.py
from picamera2 import Picamera2
from flask import Flask, Response
import cv2, time
import mediapipe as mp
import atexit

# ---------------------------
# MediaPipe setup (once)
# ---------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# Make sure we release MediaPipe on exit
def _cleanup_pose():
    try:
        pose.close()
    except Exception:
        pass

atexit.register(_cleanup_pose)

# ---------------------------
# Camera setup
# ---------------------------
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    controls={"FrameDurationLimits": (33333, 33333)}  # ~30 FPS
)
picam2.configure(config)
picam2.start()
time.sleep(0.2)

# ---------------------------
# Flask app
# ---------------------------
app = Flask(__name__)

def gen():
    """
    MJPEG generator: grabs a frame, runs MediaPipe Pose, draws landmarks,
    overlays 'Hand is raised!' when right wrist is above right elbow,
    and streams as JPEGs.
    """
    while True:
        # Capture RGB from the camera, convert to BGR for OpenCV drawing/encoding
        rgb = picam2.capture_array()
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        # MediaPipe wants RGB input
        results = pose.process(rgb)

        if results.pose_landmarks:
            # Draw pose on the BGR frame for display
            mp_drawing.draw_landmarks(
                bgr,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(thickness=2),
            )

            # Simple raised-hand check (right side)
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

            if right_wrist.y < right_elbow.y:
                cv2.putText(
                    bgr, "Hand is raised!", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA
                )
                # Also log to console (optional)
                print("Hand is raised!")

        # JPEG-encode and yield
        ok, jpg = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
               jpg.tobytes() + b"\r\n")

@app.route("/")
def index():
    # Simple page that shows the stream
    return "<html><body style='margin:0;background:#000'><img style='width:100%;height:auto' src='/video_feed' /></body></html>"

@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, threaded=True)
    finally:
        try:
            picam2.close()
        except Exception:
            pass
        _cleanup_pose()
