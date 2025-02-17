import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def main():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        
        print("Setting up TinyMPC controller...")
        # Switch to TinyMPC controller
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(2)  # Give more time to initialize
        print("Controller set to TinyMPC")

        print("Taking off...")
        for y in range(10):
            cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
            print(f"Height setpoint: {y/25}")
            time.sleep(0.2)  # Slower takeoff

        print("Hovering...")
        for _ in range(50):  # Longer hover time
            cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
            time.sleep(0.1)

        print("Landing...")
        for y in range(10):
            cf.commander.send_hover_setpoint(0, 0, 0, (10-y) / 25)
            time.sleep(0.2)  # Slower landing

        cf.commander.send_stop_setpoint()

if __name__ == '__main__':
    main()