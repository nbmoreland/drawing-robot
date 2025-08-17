# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LEGO SPIKE Prime robot control application using the Pybricks library. The robot appears to be designed for navigating stairs using motor control and color sensor feedback.

## Architecture

### Core Components

1. **main.py**: Entry point that initializes a Robot instance and runs a state machine loop until the robot reaches a "done" state.

2. **robot.py**: Contains the `Robot` class that interfaces with the LEGO SPIKE Prime hardware:
   - Uses Pybricks library for hardware control
   - Implements a DriveBase with left/right motors for movement
   - Has a rear motor for additional control
   - Uses a color sensor to detect black surfaces (stairs)
   - Tracks stair count to control movement phases

### Hardware Configuration

- **Hub**: PrimeHub (LEGO SPIKE Prime)
- **Motors**:
  - Left motor: Port A
  - Right motor: Port F (counter-clockwise)
  - Rear motor: Port B
- **Sensors**:
  - Color sensor: Port C
- **DriveBase**: Configured with wheel diameter 56mm and axle track 114mm

## Key Implementation Details

The robot currently implements a stair-climbing behavior:
- Detects black surfaces using the color sensor
- Maintains a stair count to track progress
- Has different movement phases based on stair count:
  - < 3 stairs: Full speed forward (500) with rear motor
  - 3-4 stairs: Stop completely
  - > 4 stairs: Slow movement (50) with minimal rear motor

Note: The current implementation has an incomplete state machine - the `Robot` class has no `current_state` or `update()` method as referenced in main.py.

## Development Commands

To run the application on the SPIKE Prime hub:
```bash
python main.py
```

Note: This code is designed to run on the LEGO SPIKE Prime hub with Pybricks firmware, not on a regular computer.