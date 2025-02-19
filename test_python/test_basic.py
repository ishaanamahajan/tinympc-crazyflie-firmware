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

        def log_state_callback(timestamp, data, logconf):
            nonlocal initial_height
            current_height = data['stateEstimate.z']
            
            if initial_height is None:
                initial_height = current_height
                print(f"Initial height set to: {initial_height:.2f}m")
            
            relative_height = current_height - initial_height
            print(f"Relative height: {relative_height:.2f}m")

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

        # Just PID controller
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(0.1)

        # Super simple: just try to hover 3cm above initial height
        print("Attempting hover...")
        target_height = 0.03  # 3cm
        for _ in range(50):  # 5 seconds
            cf.commander.send_hover_setpoint(0, 0, 0, initial_height )
            time.sleep(0.1)

        # Land
        print("Landing...")
        cf.commander.send_stop_setpoint()

if __name__ == '__main__':
    simple_hover()


# """
# Simple example that connects to a Crazyflie and runs a hover sequence.
# Adapted from the official Bitcraze example.
# """
# import logging
# import time
# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.utils import uri_helper
# from cflib.crazyflie.log import LogConfig

# URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# # Only output errors from the logging framework
# logging.basicConfig(level=logging.ERROR)

# def simple_hover():
#     # Initialize the low-level drivers
#     cflib.crtp.init_drivers()

#     with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
#         cf = scf.cf

#         # Store state data globally
#         global current_state
#         current_state = {
#             'roll': 0,
#             'pitch': 0,
#             'yaw': 0,
#             'height': 0,
#             'initial_height': None  # Store initial height
#         }

#         lg_state = LogConfig(name='State', period_in_ms=100)
#         lg_state.add_variable('stabilizer.thrust', 'uint16_t')
#         lg_state.add_variable('stabilizer.roll', 'float')
#         lg_state.add_variable('stabilizer.pitch', 'float')
#         lg_state.add_variable('stabilizer.yaw', 'float')
#         lg_state.add_variable('stateEstimate.z', 'float')

#         def log_state_callback(timestamp, data, logconf):
#             current_state['roll'] = data['stabilizer.roll']
#             current_state['pitch'] = data['stabilizer.pitch']
#             current_state['yaw'] = data['stabilizer.yaw']
#             current_state['height'] = data['stateEstimate.z']
            
#             # Set initial height if not set
#             if current_state['initial_height'] is None:
#                 current_state['initial_height'] = data['stateEstimate.z']
#                 print(f"Initial height set to: {current_state['initial_height']:.2f}m")
            
#             # EMERGENCY STOP if height change is too large
#             height_change = abs(data['stateEstimate.z'] - current_state['initial_height'])
#             if height_change > 0.10:  # If we move more than 10cm
#                 print(f"EMERGENCY STOP - Height change too large: {height_change:.2f}m")
#                 cf.commander.send_stop_setpoint()
#                 return

#             print(f"Height: {data['stateEstimate.z']:.2f}m, "
#                   f"Thrust: {data['stabilizer.thrust']}, "
#                   f"Roll: {data['stabilizer.roll']:.2f}, "
#                   f"Pitch: {data['stabilizer.pitch']:.2f}, "
#                   f"Yaw: {data['stabilizer.yaw']:.2f}")

#         # Reset estimator first
#         print("Resetting estimator...")
#         cf.param.set_value('kalman.initialZ', '0.0')
#         cf.param.set_value('kalman.resetEstimation', '1')
#         time.sleep(0.1)
#         cf.param.set_value('kalman.resetEstimation', '0')
#         time.sleep(2.0)

#         # Set initial PID controller
#         cf.param.set_value('stabilizer.controller', '1')
#         time.sleep(0.1)

#         cf.log.add_config(lg_state)
#         lg_state.data_received_cb.add_callback(log_state_callback)
#         lg_state.start()

#         # Wait for initial height reading
#         time.sleep(1.0)

#         # Define our target height and steps
#         TARGET_HEIGHT = 0.03  # Reduced to 3cm maximum height
#         STEPS = 30  # More steps for smoother motion
        
#         print('Taking off...')
#         print(f"DEBUG - Target height above ground: {TARGET_HEIGHT:.2f}m")
#         for y in range(STEPS):
#             height = (y / STEPS) * TARGET_HEIGHT
#             print(f"DEBUG - Commanding height: {height:.2f}m")
#             cf.commander.send_hover_setpoint(0, 0, 0, height)
#             time.sleep(0.2)  # Slower updates

#         cf.param.set_value('stabilizer.controller', '5')
#         time.sleep(0.1)

#         print('Hovering...')
#         print(f"DEBUG - Hover height: {TARGET_HEIGHT:.2f}m")
#         for _ in range(20):  # Hover for 2 seconds
#             cf.commander.send_hover_setpoint(0, 0, 0, TARGET_HEIGHT)
#             time.sleep(0.1)

#         print('Landing...')
#         for y in range(STEPS):
#             height = TARGET_HEIGHT * (1 - y / STEPS)
#             print(f"DEBUG - Landing height: {height:.2f}m")
#             cf.commander.send_hover_setpoint(0, 0, 0, height)
#             time.sleep(0.2)  # Slower updates

#         cf.commander.send_stop_setpoint()
#         time.sleep(0.1)

# if __name__ == '__main__':
#     simple_hover()