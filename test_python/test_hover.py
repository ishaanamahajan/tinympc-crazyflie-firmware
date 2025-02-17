import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def main():
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        
        print("Setting up TinyMPC controller...")
        # Switch to TinyMPC controller
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(1)

        print("Taking off...")
        # Initial height
        for y in range(10):
            cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
            time.sleep(0.1)

        # Hover for a while
        print("Hovering...")
        for _ in range(20):
            cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
            time.sleep(0.1)

        # Land
        print("Landing...")
        for y in range(10):
            cf.commander.send_hover_setpoint(0, 0, 0, (10-y) / 25)
            time.sleep(0.1)

        cf.commander.send_stop_setpoint()

if __name__ == '__main__':
    main()