from robot import Robot

# Initialize the robot
robot = Robot()

def main():
    """Main loop to update the robot and manage the state machine."""
    while robot.current_state != "done":
        robot.update()
        
if __name__ == "__main__":
    main()