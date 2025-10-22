import time, sys, board, busio
from adafruit_pca9685 import PCA9685

print("=== START ===", flush=True)
print("Python:", sys.version, flush=True)
print("board from:", board.__file__, flush=True)

# Init I2C + PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x40)
pca.frequency = 50
print("PCA9685 ready @ 0x40, freq=50Hz", flush=True)

# helper: microseconds -> 16-bit duty for a 20,000 µs (50 Hz) frame
def us_to_dc(us):
    dc = int((us / 20000.0) * 65535)
    print(f"pulse={us}us -> duty={dc}", flush=True)
    return dc

ch = pca.channels[0]

# Move to default (center) position
ch.duty_cycle = us_to_dc(1500)
print("Default position (center); sleep 2s...", flush=True)
time.sleep(2)


# move to min position (possible 0°)
ch.duty_cycle = us_to_dc(500)
print("Min position (possible 0°/500us); sleep 2s...", flush=True)
time.sleep(2)

# move to center position (90°)
ch.duty_cycle = us_to_dc(1500)
print("Center position (90°/1500us); sleep 2s...", flush=True)
time.sleep(2)

# move to max position (possible 180°)
ch.duty_cycle = us_to_dc(2500)
print("Max position (possible 180°/2500us); sleep 2s...", flush=True)
time.sleep(2)

# Return to center after test
ch.duty_cycle = us_to_dc(1500)
print("Back to center; sleep 2s...", flush=True)
time.sleep(2)