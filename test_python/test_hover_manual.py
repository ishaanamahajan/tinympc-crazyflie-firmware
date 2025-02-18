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

        # Set up logging - ALL MOTORS
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        lg_stab.add_variable('motor.m1', 'uint32_t')
        lg_stab.add_variable('motor.m2', 'uint32_t')
        lg_stab.add_variable('motor.m3', 'uint32_t')
        lg_stab.add_variable('motor.m4', 'uint32_t')

        def log_stab_callback(timestamp, data, logconf):
            print(f"Height: {data['stateEstimate.z']:.2f} "
                  f"Roll: {data['stabilizer.roll']:.2f} "
                  f"Pitch: {data['stabilizer.pitch']:.2f} "
                  f"Motors: {data['motor.m1']} {data['motor.m2']} "
                  f"{data['motor.m3']} {data['motor.m4']}")

        cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        # Initial takeoff sequence with PID
        print("\nSetting PID controller...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(1.0)

        print("Taking off...")
        hlc.takeoff(0.5, 2.0)  # Lower height (50cm) for initial testing
        time.sleep(2.1)

        print("Going to hover position...")
        hlc.go_to(0.0, 0.0, 0.5, 0.0, 2.0)  # Stay at 50cm
        time.sleep(3.0)  # More time to stabilize

        # Switch to TinyMPC more gradually
        print("START: Switching controller task")
        cf.param.set_value('usd.logging', '1')
        time.sleep(2.0)  # More time before switch
        
        print("Switching to TinyMPC...")
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(3.0)  # More time after switch

        # Hold position for shorter time initially
        sleep_time = 5.0  # Just 5 seconds for testing
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