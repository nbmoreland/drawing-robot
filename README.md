# LEGO SPIKE Prime Stair-Climbing Robot

A Python-based autonomous stair-climbing robot built with LEGO SPIKE Prime and programmed using the Pybricks library. The robot uses color detection to identify stairs and automatically adjusts its climbing behavior based on progress.

## 🎯 Project Overview

This project implements an intelligent stair-climbing robot that can:
- Detect stairs using a color sensor (black surfaces indicate stairs)
- Autonomously climb multiple stairs with adaptive speed control
- Track progress through stair counting
- Gracefully transition between climbing phases
- Stop automatically after completing the climbing sequence

## 🛠️ Hardware Requirements

### LEGO Components
- **LEGO SPIKE Prime Hub** (or compatible LEGO Education hub)
- **3x LEGO Motors**:
  - Left drive motor
  - Right drive motor  
  - Rear auxiliary motor (for additional climbing support)
- **1x Color Sensor** for stair detection
- LEGO Technic parts for robot chassis construction

### Port Configuration
| Component | Port | Notes |
|-----------|------|-------|
| Left Motor | A | Drive motor for left side |
| Right Motor | F | Drive motor for right side (counter-clockwise) |
| Rear Motor | B | Auxiliary motor for climbing assistance |
| Color Sensor | C | Detects black surfaces (stairs) |

## 📦 Software Requirements

- **Pybricks firmware** installed on your SPIKE Prime hub
  - Download from [pybricks.com](https://pybricks.com/)
  - Follow the [installation guide](https://pybricks.com/install/)
- **Python 3.x** (comes with Pybricks)
- **Pybricks library** (pre-installed with Pybricks firmware)

## 🚀 Installation & Setup

1. **Install Pybricks Firmware**
   ```bash
   # Visit https://pybricks.com/install/
   # Follow instructions for your operating system
   ```

2. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/drawing-robot.git
   cd drawing-robot
   ```

3. **Connect your SPIKE Prime hub**
   - Turn on the hub
   - Connect via USB or Bluetooth
   - Use Pybricks Code or VS Code with Pybricks extension

4. **Upload the code**
   - Open the project in your Pybricks environment
   - Upload `main.py` and `robot.py` to the hub

## 🤖 How It Works

### Architecture

The robot uses a state machine architecture with two main components:

1. **`main.py`** - Entry point that initializes the robot and runs the main control loop
2. **`robot.py`** - Contains the `Robot` class with all hardware interfaces and behavior logic

### State Machine

The robot operates in two states:

- **`climbing`** - Active climbing mode with three phases:
  - Phase 1 (0-2 stairs): Fast climbing at full speed
  - Phase 2 (3-4 stairs): Pause/transition phase
  - Phase 3 (5+ stairs): Slow, careful climbing
- **`done`** - Terminal state when climbing is complete

### Climbing Algorithm

```python
1. Initialize robot with all motors and sensors
2. Start in "climbing" state
3. While not done:
   a. Read color sensor
   b. If black detected → increment stair counter
   c. Adjust speed based on stair count:
      - < 3 stairs: Speed 500, rear motor 500
      - 3-4 stairs: Stop (transition phase)
      - > 4 stairs: Speed 50, rear motor 5
   d. Check if complete (>5 stairs) → transition to "done"
4. Stop all motors
```

### DriveBase Configuration
- **Wheel diameter**: 56mm
- **Axle track**: 114mm (distance between wheels)
- These values are crucial for accurate movement calculations

## 💻 Usage

### Basic Operation

1. **Position the robot** at the base of the stairs
2. **Run the program**:
   ```python
   python main.py
   ```
3. The robot will automatically:
   - Start climbing when it detects black surfaces
   - Adjust speed based on progress
   - Stop after climbing 5+ stairs

### Console Output

The robot provides real-time feedback:
```
Color.BLACK
1
Color.BLACK
2
...
```

## 🎨 Customization

### Adjusting Climbing Behavior

Modify thresholds in `robot.py`:

```python
# Change completion threshold (default: 5 stairs)
if self.stair_count > 5:  # Adjust this value
    self.current_state = "done"

# Modify speed phases
if self.stair_count < 3:  # Phase 1 threshold
    self.drive_base.drive(500, 0)  # Adjust speed
elif self.stair_count >= 3 and self.stair_count < 4:  # Phase 2
    self.drive_base.drive(0, 0)  # Pause phase
else:  # Phase 3
    self.drive_base.drive(50, 0)  # Slow speed
```

### Color Detection

Change the target color for stair detection:
```python
if color == Color.BLACK:  # Change to Color.RED, Color.BLUE, etc.
    self.stair_count = self.stair_count + 1
```

### Motor Configuration

Adjust motor ports or directions:
```python
self.left_motor = Motor(Port.A)  # Change port
self.right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)  # Change direction
```

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Robot doesn't move | Check motor connections and battery level |
| Color sensor not detecting | Ensure sensor is close to surface (~1cm) |
| Robot turns instead of going straight | Calibrate wheel diameter and axle track values |
| Motors running in wrong direction | Add `Direction.COUNTERCLOCKWISE` parameter |
| Program won't upload | Ensure Pybricks firmware is installed |

### Debug Mode

Add verbose logging by modifying `robot.py`:
```python
def move(self):
    color = self.color_sensor.color()
    print(f"Color: {color}, Stair count: {self.stair_count}, State: {self.current_state}")
    # ... rest of code
```

## 📊 Performance Specifications

- **Maximum climbing speed**: 500 mm/s
- **Minimum climbing speed**: 50 mm/s
- **Stair detection**: Black surfaces (customizable)
- **Completion threshold**: 5+ stairs (adjustable)
- **Response time**: Real-time color detection

## 🧩 Project Structure

```
drawing-robot/
├── main.py          # Entry point and main control loop
├── robot.py         # Robot class with hardware interfaces
├── README.md        # This file
└── CLAUDE.md        # Development guide for AI assistants
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

### Development Guidelines

1. Follow the existing code style
2. Test on actual hardware before submitting PRs
3. Update documentation for any new features
4. Keep the state machine pattern for consistency

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Pybricks](https://pybricks.com/) - Python for LEGO hubs
- LEGO Education SPIKE Prime platform
- Inspired by competitive robotics challenges

## 📚 Resources

- [Pybricks Documentation](https://docs.pybricks.com/)
- [LEGO SPIKE Prime](https://education.lego.com/en-us/products/lego-education-spike-prime-set/45678)
- [Python Robotics Tutorials](https://pybricks.com/learn/)

## 🚧 Future Enhancements

- [ ] Add obstacle detection
- [ ] Implement backward climbing
- [ ] Add gyroscope for balance control
- [ ] Create web-based control interface
- [ ] Add data logging for climb analytics
- [ ] Implement adaptive learning for different stair types

---

**Note**: This robot is designed for educational purposes and LEGO SPIKE Prime competitions. Always supervise the robot during operation to prevent damage to the hardware.