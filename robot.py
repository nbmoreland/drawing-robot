from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub
import umath


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

    def update_position(self, x, y):
        """Update the robot's current position."""
        print(f"Updating position to ({x}, {y})...")
        self.current_position = (x, y)

    def move_to_position(self, target_x, target_y, step_size=10):
        """Move the robot to the target (x, y) position one step at a time."""
        current_x, current_y = self.current_position

        # Calculate the direction to the target
        delta_x = target_x - current_x
        delta_y = target_y - current_y
        distance_to_target = sqrt(delta_x**2 + delta_y**2)

        if distance_to_target < step_size:
            # If within one step of the target, move directly to the target
            step_x, step_y = target_x, target_y
        else:
            # Calculate step size in the direction of the target
            step_ratio = step_size / distance_to_target
            step_x = current_x + delta_x * step_ratio
            step_y = current_y + delta_y * step_ratio

        # Calculate the angle to turn toward the next step
        target_angle = degrees(atan2(step_y - current_y, step_x - current_x))
        angle_to_turn = target_angle - self.current_heading

        # Turn to face the step
        print(f"Turning by {angle_to_turn:.2f} degrees to face step...")
        self.drive_base.turn(angle_to_turn)

        # Update the current heading
        self.current_heading = target_angle

        # Drive one step forward
        step_distance = sqrt((step_x - current_x)**2 + (step_y - current_y)**2)
        print(f"Driving {step_distance:.2f} mm to step ({step_x}, {step_y})...")
        self.drive_base.straight(step_distance)

        # Update the robot's position
        self.update_position(step_x, step_y)
    
    def move(self):
        """Move the marker to the starting vertex without drawing."""
        if not self.vertices:
            print("No vertices defined!")
            self.current_state = "done"
            return

        if self.current_vertex == 0:
            # Move incrementally toward the starting vertex
            x, y = self.vertices[0]
            if self.current_position != (x, y):
                print("Moving incrementally to starting vertex ({}, {})...".format(x, y))
                self.move_to_position(x, y)
            else:
                print("Reached starting vertex.")
                self.marker_motor.run_target(100, -10)  # Lower marker for drawing
                self.current_state = "draw"

    def draw(self):
        """Trace the polygon by moving to each vertex incrementally."""
        if self.current_vertex < len(self.vertices) - 1:
            x, y = self.vertices[self.current_vertex]
            if self.current_position != (x, y):
                print("Drawing incrementally to vertex ({}, {})...".format(x, y))
                self.move_to_position(x, y)
            else:
                print("Reached vertex ({}, {}).".format(x, y))
                self.current_vertex += 1
        else:
            self.marker_motor.run_target(100, 0)  # Lift marker
            self.current_state = "done"


    def done(self):
        """Finish the drawing."""
        print("Drawing complete!")
        self.hub.speaker.beep()
