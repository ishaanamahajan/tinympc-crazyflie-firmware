import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def main():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        
        # Set up logging
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')
        lg_stab.add_variable('stabilizer.thrust', 'float')

        def log_stab_callback(timestamp, data, logconf):
            print(f"Roll: {data['stabilizer.roll']:.2f} Pitch: {data['stabilizer.pitch']:.2f} "
                  f"Yaw: {data['stabilizer.yaw']:.2f} Thrust: {data['stabilizer.thrust']:.2f}")

        cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        print("Connected:", cf.is_connected())
        print("Initial params:")
        print("Controller:", cf.param.get_value('stabilizer.controller'))
        #print("Thrust ratio:", cf.param.get_value('stabilizer.thrust_ratio'))
        
        # Start with PID controller
        print("\nSetting up PID controller...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1)

        # Take off with PID
        print("\nTaking off with PID...")
        for y in range(40):
            height = y / 10
            print(f"Setting height to {height}")
            cf.commander.send_hover_setpoint(0, 0, 0, height)
            time.sleep(1.0)
        
        # Check if we're connected and controller is set
        print(f"Connected: {cf.is_connected()}")
        controller = cf.param.get_value('stabilizer.controller')
        print(f"Current controller: {controller}")

        # Go to hover position
        print("Going to hover position...")
        for _ in range(20):
            cf.commander.send_hover_setpoint(0, 0, 0, 0.8)
            time.sleep(1.0)

        # Switch to TinyMPC
        print("\nSwitching to TinyMPC controller...")
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(1.0)
        print("Controller now:", cf.param.get_value('stabilizer.controller'))
        
        # Hold with TinyMPC
        print("Holding with TinyMPC...")
        for i in range(500):
            cf.commander.send_hover_setpoint(0, 0, 0, 0.8)
            if i % 10 == 0:
                print(f"TinyMPC Hover - iteration {i}")
                print(f"Current controller: {cf.param.get_value('stabilizer.controller')}")
            time.sleep(0.1)

        # Switch back to PID
        print("\nSwitching back to PID for landing...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1.0)
        print("Controller now:", cf.param.get_value('stabilizer.controller'))

        # Land with PID
        print("Landing...")
        for y in range(40):
            height = (40-y) / 100
            cf.commander.send_hover_setpoint(0, 0, 0, height)
            time.sleep(0.1)

        print("Sending stop command...")
        cf.commander.send_stop_setpoint()
        print("Flight test complete!")

if __name__ == '__main__':
    main()