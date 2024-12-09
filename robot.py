from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub
import math
from time import sleep


class Robot:
    def __init__(self):
        # Initialize the hub
        self.hub = PrimeHub()

        # Initialize the motors
        self.left_motor = Motor(Port.F)
        self.right_motor = Motor(Port.D)
        self.marker_motor = Motor(Port.A)

        # Initialize the drive base
        self.drive_base = DriveBase(self.left_motor, self.right_motor, 56, 114)
        self.drive_base.use_gyro(True)

        # Drawing area dimensions (in mm)
        self.width = 150  # 15 cm
        self.height = 100  # 10 cm

        # Initialize the states
        self.states = ["init", "move", "draw", "done"]
        self.current_state = "init"

        # Polygon vertices
        self.vertices = [(0, 0), (self.width, 0), (self.width, self.height),
                         (0, self.height), (0, 0)]  # Tracing the paper for now

        # Initialize the current vertex
        self.current_vertex = 0  # Start at the first vertex

        self.current_position = (0, 0)  # Initialize the current position
        self.current_heading = 0  # Initialize the current heading

    def update(self):
        """Update the robot based on the current state."""
        if self.current_state == "init":
            self.init()
        elif self.current_state == "move":
            self.move()
        elif self.current_state == "draw":
            self.draw()
        elif self.current_state == "done":
            self.done()

    def init(self):
        """Initialize the robot."""
        print("Initializing...")
        self.drive_base.reset()  # Reset the drive base
        self.marker_motor.run_target(100, 0)  # Lift marker
        self.current_state = "move"

    def update_position(self, speed, time_delta):
        """Update the robot's position based on speed and elapsed time."""
        dx = speed * math.cos(math.radians(self.current_heading)) * time_delta
        dy = speed * math.sin(math.radians(self.current_heading)) * time_delta
        x, y = self.current_position
        self.current_position = (x + dx, y + dy)

    def move_to_position(self, x_target, y_target):
        """Move to the specified (x, y) using continuous driving."""
        x, y = self.current_position
        dx = x_target - x
        dy = y_target - y
        target_distance = math.sqrt(dx**2 + dy**2)
        target_angle = math.degrees(math.atan2(dy, dx))

        # Turn to face the target
        turn_angle = target_angle - self.current_heading
        self.drive_base.turn(turn_angle)
        self.current_heading = target_angle  # Update heading after the turn

        # Start driving towards the target
        speed = 100  # Speed in mm/s
        while target_distance > 10:  # Stop when within 10mm of the target
            self.drive_base.drive(speed, 0)  # Drive straight
            sleep(0.1)  # Allow time for movement
            self.update_position(speed, 0.1)  # Update position
            x, y = self.current_position
            dx = x_target - x
            dy = y_target - y
            target_distance = math.sqrt(dx**2 + dy**2)

        self.drive_base.stop()  # Stop when the target is reached

    def move(self):
        """Move the marker to the starting vertex without drawing."""
        if not self.vertices:
            print("No vertices defined!")
            self.current_state = "done"
            return

        if self.current_vertex == 0:
            # Move to the starting vertex from outside the drawing area
            x, y = self.vertices[0]
            print("Moving to starting vertex ({}, {})...".format(x, y))
            self.move_to_position(x, y)
            self.marker_motor.run_target(100, -10)  # Lower marker for drawing
            self.current_state = "draw"

    def draw(self):
        """Trace the polygon by moving to each vertex."""
        if self.current_vertex < len(self.vertices) - 1:
            x_target, y_target = self.vertices[self.current_vertex + 1]
            print(f"Drawing line to vertex ({x_target}, {y_target})...")
            self.move_to_position(x_target, y_target)
            self.current_vertex += 1
        else:
            self.marker_motor.run_target(100, 0)  # Lift marker
            self.current_state = "done"

    def done(self):
        """Finish the drawing."""
        print("Drawing complete!")
        self.hub.speaker.beep()
