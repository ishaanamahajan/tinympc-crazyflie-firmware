import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.high_level_commander import HighLevelCommander

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def main():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        hlcommander = HighLevelCommander(cf)  # Create high-level commander
        
        # PID setup (1 second)
        print("Setting up PID controller...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1)

        # Takeoff (2.1 seconds)
        print("Taking off with PID...")
        hlcommander.takeoff(1.0, 2.0)  # Use high-level commander
        time.sleep(2.1)
        
        # Go to hover position (2 seconds)
        print("Going to hover position...")
        hlcommander.go_to(0, 0, 1.0, 0, 2.0)  # Use high-level commander
        time.sleep(2.0)

        # Switch to TinyMPC and hold (7 seconds)
        print("Switching to TinyMPC controller...")
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(2.0)
        print("Holding with TinyMPC...")
        time.sleep(5.0)

        # Switch back to PID (1 second)
        print("Switching back to PID for landing...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1.0)

        # Landing sequence (4 seconds)
        print("Landing...")
        hlcommander.go_to(0, 0, 0.1, 0, 2.0)  # Use high-level commander
        time.sleep(2.0)
        hlcommander.land(0.0, 2.0)  # Use high-level commander
        time.sleep(2.0)

        print("Stopping motors...")
        cf.commander.send_stop_setpoint()
        print("Flight test complete!")

if __name__ == '__main__':
    main()