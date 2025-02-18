import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.high_level_commander import HighLevelCommander

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def main():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf
        hlc = HighLevelCommander(cf)

        # Set up logging
        lg_state = LogConfig(name='State', period_in_ms=100)
        lg_state.add_variable('stabilizer.roll', 'float')
        lg_state.add_variable('stabilizer.pitch', 'float')
        lg_state.add_variable('stateEstimate.z', 'float')

        lg_motors = LogConfig(name='Motors', period_in_ms=100)
        lg_motors.add_variable('motor.m1', 'uint32_t')
        lg_motors.add_variable('motor.m2', 'uint32_t')
        lg_motors.add_variable('motor.m3', 'uint32_t')
        lg_motors.add_variable('motor.m4', 'uint32_t')

        def log_state_callback(timestamp, data, logconf):
            print(f"Height: {data['stateEstimate.z']:.2f} "
                  f"Roll: {data['stabilizer.roll']:.2f} "
                  f"Pitch: {data['stabilizer.pitch']:.2f}")

        def log_motors_callback(timestamp, data, logconf):
            print(f"Motors: {data['motor.m1']} {data['motor.m2']} "
                  f"{data['motor.m3']} {data['motor.m4']}")

        cf.log.add_config(lg_state)
        cf.log.add_config(lg_motors)
        lg_state.data_received_cb.add_callback(log_state_callback)
        lg_motors.data_received_cb.add_callback(log_motors_callback)
        lg_state.start()
        lg_motors.start()

        try:
            # Force PID controller
            print("\nSetting PID controller...")
            cf.param.set_value('stabilizer.controller', '1')
            time.sleep(1.0)

            # Simple takeoff and land sequence
            print("Taking off with PID...")
            hlc.takeoff(0.2, 3.0)  # 20cm height, 3s duration
            time.sleep(3.5)

            print("Holding position...")
            time.sleep(2.0)

            print("Landing...")
            hlc.land(0.0, 2.0)
            time.sleep(2.0)

            print("Test complete!")

        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Emergency landing...")
            cf.commander.send_setpoint(0, 0, 0, 0)
            time.sleep(0.1)

if __name__ == '__main__':
    main()