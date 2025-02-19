import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')


def simple_hover():
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf

        # Store initial height
        initial_height = None

        # Set up height logging
        lg_state = LogConfig(name='State', period_in_ms=100)
        lg_state.add_variable('stateEstimate.z', 'float')
        lg_state.add_variable('stabilizer.pitch', 'float')  # Added pitch monitoring
        lg_state.add_variable('stabilizer.roll', 'float')  
        lg_state.add_variable('stabilizer.yaw', 'float')

        def log_state_callback(timestamp, data, logconf):
            nonlocal initial_height
            current_height = data['stateEstimate.z']
            
            if initial_height is None:
                initial_height = current_height
                print(f"Initial height set to: {initial_height:.2f}m")
            
            relative_height = current_height - initial_height
            print(f"Relative height: {relative_height:.2f}m, Pitch: {data['stabilizer.pitch']:.2f}, Roll: {data['stabilizer.roll']:.2f}")

        cf.log.add_config(lg_state)
        lg_state.data_received_cb.add_callback(log_state_callback)
        lg_state.start()

        # Wait to get initial height
        print("Getting initial height...")
        time.sleep(2.0)

        # Reset estimator
        print("Resetting estimator...")
        cf.param.set_value('kalman.initialZ', '0.0')
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2.0)

        # Switch to TinyMPC
        print("Setting TinyMPC controller...")
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(0.2)

        # Try to hover with TinyMPC
        print("Attempting hover with TinyMPC...")
        target_height = 0.03  # 3cm
        for _ in range(50):  # 5 seconds
            cf.commander.send_hover_setpoint(0, 0, 0, initial_height)
            time.sleep(0.1)

        # Land
        print("Landing...")
        cf.commander.send_stop_setpoint()

if __name__ == '__main__':
    simple_hover()