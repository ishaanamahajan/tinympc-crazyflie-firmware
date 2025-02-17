import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.high_level_commander import HighLevelCommander

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Control parameters (matching original script)
frequency = 500     # control frequency
trajLength = 1405   # for delay time 
trajIter = 1        # number of laps
trajHold = 2        # 1 is most aggressive

def main():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        hlc = HighLevelCommander(cf)

        # Set up logging
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')

        def log_stab_callback(timestamp, data, logconf):
            print(f"Height: {data['stateEstimate.z']:.2f} "
                  f"Roll: {data['stabilizer.roll']:.2f} "
                  f"Pitch: {data['stabilizer.pitch']:.2f}")

        cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        # Initial takeoff sequence with PID
        print("\nSetting PID controller...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1.0)

        print("Taking off...")
        hlc.takeoff(1.0, 2.0)  # Same height and duration as original
        time.sleep(2.1)  # Matching original sleep time

        print("Going to hover position...")
        hlc.go_to(0.0, 0.0, 1.0, 0.0, 2.0)  # Same position and duration as original
        time.sleep(2.0)

        # Switch to TinyMPC
        print("START: Switching controller task")
        cf.param.set_value('usd.logging', '1')
        cf.param.set_value('stabilizer.controller', '5')

        # Calculate sleep time using same formula as original
        sleep_time = trajIter * trajLength * trajHold / frequency
        print(f"Holding with TinyMPC for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

        cf.param.set_value('usd.logging', '0')
        time.sleep(1.0)

        # Switch back to PID and land
        print("END: Switching to controller 1")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(2.0)

        print("Going to landing position...")
        hlc.go_to(0.0, 0.0, 0.1, 0.0, 2.0)  # Same as original
        time.sleep(2.0)

        print("Landing...")
        hlc.land(0.02, 2.0)  # Same parameters as original
        time.sleep(2.0)

        print("Flight test complete!")

if __name__ == '__main__':
    main()