from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub


class Robot:
    def __init__(self):
        # Initialize the hub
        self.hub = PrimeHub()

        # Initialize the motors
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.rear_motor = Motor(Port.B)
        self.color_sensor = ColorSensor(Port.C)

        # Initialize the drive base
        self.drive_base = DriveBase(self.left_motor, self.right_motor, 56, 114)
        self.stair_count = 0
        self.current_state = "climbing"

    def update(self):
        """Update the robot state and perform actions based on current state."""
        if self.current_state == "climbing":
            self.move()
            # Check if we've completed the climbing sequence
            if self.stair_count > 5:  # Adjust threshold as needed
                self.current_state = "done"
                self.drive_base.stop()
                self.rear_motor.stop()
        elif self.current_state == "done":
            # Robot has finished its task
            self.drive_base.stop()
            self.rear_motor.stop()

    def move(self):
        """Move the robot up the stairs and back down."""
        color = self.color_sensor.color()
        print(color)
        if color == Color.BLACK:
            self.stair_count = self.stair_count + 1

        print(self.stair_count)

        if self.stair_count < 3:
            self.drive_base.drive(500, 0)
            self.rear_motor.run(500)
        elif self.stair_count >= 3 and self.stair_count < 4:
            self.drive_base.drive(0, 0)
            self.rear_motor.run(0)

            self.stair_count = self.stair_count + 1
        else:
            self.drive_base.drive(50, 0)
            self.rear_motor.run(5)