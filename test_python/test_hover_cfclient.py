import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def simple_hover():
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
        cf = scf.cf

        # Store state data globally
        global current_state
        current_state = {
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'height': 0
        }

        # Split logging into two configs
        lg_state = LogConfig(name='State', period_in_ms=100)
        lg_state.add_variable('stabilizer.thrust', 'uint16_t')
        lg_state.add_variable('stabilizer.roll', 'float')
        lg_state.add_variable('stabilizer.pitch', 'float')
        lg_state.add_variable('stabilizer.yaw', 'float')
        lg_state.add_variable('stateEstimate.z', 'float')

        lg_motors = LogConfig(name='Motors', period_in_ms=100)
        lg_motors.add_variable('motor.m1', 'uint32_t')
        lg_motors.add_variable('motor.m2', 'uint32_t')
        lg_motors.add_variable('motor.m3', 'uint32_t')
        lg_motors.add_variable('motor.m4', 'uint32_t')

        def log_state_callback(timestamp, data, logconf):
            current_state['roll'] = data['stabilizer.roll']
            current_state['pitch'] = data['stabilizer.pitch']
            current_state['yaw'] = data['stabilizer.yaw']
            current_state['height'] = data['stateEstimate.z']
            print(f"Height: {data['stateEstimate.z']:.2f}m, "
                  f"Thrust: {data['stabilizer.thrust']}, "
                  f"Roll: {data['stabilizer.roll']:.2f}, "
                  f"Pitch: {data['stabilizer.pitch']:.2f}, "
                  f"Yaw: {data['stabilizer.yaw']:.2f}")

        def log_motors_callback(timestamp, data, logconf):
            print(f"Motors: M1: {data['motor.m1']}, M2: {data['motor.m2']}, "
                  f"M3: {data['motor.m3']}, M4: {data['motor.m4']}")

        cf.log.add_config(lg_state)
        cf.log.add_config(lg_motors)
        lg_state.data_received_cb.add_callback(log_state_callback)
        lg_motors.data_received_cb.add_callback(log_motors_callback)
        lg_state.start()
        lg_motors.start()

        # After starting logs but before takeoff, get initial height
        print("Getting initial height reading...")
        time.sleep(2.0)  # Wait for some readings to come in
        
        if current_state['height'] > 0:
            initial_height = current_state['height']
            height_offset = -initial_height  # If we're at -28m, this will be +28m
            print(f"Initial height: {initial_height:.2f}m, applying offset: {height_offset:.2f}m")
        else:
            print("Warning: Could not get initial height readings!")
            height_offset = 28.0  # Fallback value if we can't get readings

        # Reset estimator and verify height
        print("Resetting estimator...")
        cf.param.set_value('kalman.initialZ', '0.0')  # Initialize height to 0
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(5.0)  # Give more time for estimator to stabilize

        # Set initial PID controller
        print("Setting PID controller...")
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(2.0)

        # Take off VERY gradually with tiny steps
        print("Taking off!")
        target_height = 0.05  # Only go up 5cm
        start_height = height_offset  # Start from where we are
        end_height = height_offset + target_height  # Go up by 5cm from there

        # Takeoff
        for y in range(15):
            progress = y / 50.0  # Goes from 0 to 1
            current_height = start_height + (progress * target_height)
            cf.commander.send_hover_setpoint(0, 0, 0, current_height)
            time.sleep(0.1)

            #add emergency stop if roll or pitch is too high
            if abs(current_state['roll']) > 60 or abs(current_state['pitch']) > 60:
                print("Emergency stop - excessive angle!")
                cf.commander.send_stop_setpoint()
                return

        # # Stay at the same height
        # print("Maintaining hover position...")
        # for _ in range(20):
        #     cf.commander.send_hover_setpoint(0, 0, 0, hover_height)  # Same height as end of takeoff
        #     time.sleep(0.2)



        # Update all other hover commands with the offset
        # print("Switching to TinyMPC...")
        # cf.commander.send_hover_setpoint(0, 0, 0, hover_height)
        # cf.param.set_value('stabilizer.controller', '5')
        # time.sleep(0.1)
        
        # print("Holding with TinyMPC...")
        # for _ in range(30):
        #     cf.commander.send_hover_setpoint(0, 0, 0, hover_height)
        #     time.sleep(0.1)

        # print("Switching back to PID...")
        # cf.commander.send_hover_setpoint(0, 0, 0, hover_height)
        # cf.param.set_value('stabilizer.controller', '1')
        # time.sleep(0.1)

        # Land with offset
        # print("Landing...")
        # for y in range(10):
        #     progress = y / 10.0  # Goes from 0 to 1
        #     current_height = end_height - (progress * target_height)
        #     cf.commander.send_hover_setpoint(0, 0, 0, current_height)
        #     time.sleep(0.2)

        # cf.commander.send_stop_setpoint()
        # time.sleep(0.1)

if __name__ == '__main__':
    #time.sleep(10.0)
    simple_hover()

