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

        # Take off more gradually with lower height
        print("Taking off!")
        for y in range(20):  # More steps for smoother takeoff
            cf.commander.send_hover_setpoint(0, 0, 0, y / 80)  # Max height 5cm
            time.sleep(0.2)

        # Stabilize at lower height
        print("Going to hover position...")
        for _ in range(20):  # Longer stabilization period
            cf.commander.send_hover_setpoint(0, 0, 0, 0.05)  # Hold at 5cm
            time.sleep(0.2)

        # Direct switch to TinyMPC with continuous commands
        print("Switching to TinyMPC...")
        cf.commander.send_hover_setpoint(0, 0, 0, 0.05)  # Keep commanding while switching
        cf.param.set_value('stabilizer.controller', '5')
        time.sleep(0.1)  # Quick switch
        
        print("Holding with TinyMPC...")
        for _ in range(30):  # Longer hold period
            cf.commander.send_hover_setpoint(0, 0, 0, 0.05)  # Stay at 5cm
            time.sleep(0.1)

        # Switch back to PID while maintaining commands
        print("Switching back to PID...")
        cf.commander.send_hover_setpoint(0, 0, 0, 0.05)
        cf.param.set_value('stabilizer.controller', '1')
        time.sleep(0.1)

        # Land
        print("Landing...")
        for y in range(10):
            cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 100)
            time.sleep(0.2)

        cf.commander.send_stop_setpoint()
        time.sleep(0.1)

if __name__ == '__main__':
    #time.sleep(10.0)
    simple_hover()

# import logging
# import time
# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.utils import uri_helper
# from cflib.crazyflie.log import LogConfig

# URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# def simple_hover():
#     print("Initializing drivers...")
#     cflib.crtp.init_drivers()

#     with SyncCrazyflie(URI, cf=Crazyflie()) as scf:
#         cf = scf.cf

#         # Split logging into two configs
#         lg_state = LogConfig(name='State', period_in_ms=100)
#         lg_state.add_variable('stabilizer.thrust', 'uint16_t')
#         lg_state.add_variable('stabilizer.roll', 'float')
#         lg_state.add_variable('stabilizer.pitch', 'float')
#         lg_state.add_variable('stabilizer.yaw', 'float')
#         lg_state.add_variable('stateEstimate.z', 'float')

#         lg_motors = LogConfig(name='Motors', period_in_ms=100)
#         lg_motors.add_variable('motor.m1', 'uint32_t')
#         lg_motors.add_variable('motor.m2', 'uint32_t')
#         lg_motors.add_variable('motor.m3', 'uint32_t')
#         lg_motors.add_variable('motor.m4', 'uint32_t')

#         def log_state_callback(timestamp, data, logconf):
#             print(f"Height: {data['stateEstimate.z']:.2f}m, "
#                   f"Thrust: {data['stabilizer.thrust']}, "
#                   f"Roll: {data['stabilizer.roll']:.2f}, "
#                   f"Pitch: {data['stabilizer.pitch']:.2f}, "
#                   f"Yaw: {data['stabilizer.yaw']:.2f}")

#         def log_motors_callback(timestamp, data, logconf):
#             print(f"Motors: M1: {data['motor.m1']}, M2: {data['motor.m2']}, "
#                   f"M3: {data['motor.m3']}, M4: {data['motor.m4']}")

#         cf.log.add_config(lg_state)
#         cf.log.add_config(lg_motors)
#         lg_state.data_received_cb.add_callback(log_state_callback)
#         lg_motors.data_received_cb.add_callback(log_motors_callback)
#         lg_state.start()
#         lg_motors.start()

#         # Reset estimator and verify height
#         print("Resetting estimator...")
#         cf.param.set_value('kalman.resetEstimation', '1')
#         time.sleep(0.1)
#         cf.param.set_value('kalman.resetEstimation', '0')
#         time.sleep(2)

#         # Set the default controller (PID)
#         print("Setting PID controller...")
#         cf.param.set_value('stabilizer.controller', '1')
#         time.sleep(1.0)

#         print("Taking off!")
#         for y in range(10):
#             cf.commander.send_hover_setpoint(0, 0, 0, y / 200)  # Much slower ascent
#             time.sleep(0.2)  # More time between commands

#         print("Hovering!")
#         for _ in range(20):
#             cf.commander.send_hover_setpoint(0, 0, 0, 0.05)  # Only 5cm height!
#             time.sleep(0.1)

#         # Switch to TinyMPC more gradually
#         print("START: Switching controller task")
#         cf.param.set_value('usd.logging', '1')
#         time.sleep(2.0)  # More time before switch
        
#         print("Switching to TinyMPC...")
#         cf.param.set_value('stabilizer.controller', '5')
#         time.sleep(3.0)  # More time after switch

#         # Hold position for shorter time initially
#         sleep_time = 5.0  # Just 5 seconds for testing
#         print(f"Holding with TinyMPC for {sleep_time:.2f} seconds...")
#         time.sleep(sleep_time)

#         cf.param.set_value('usd.logging', '0')
#         time.sleep(1.0)

#         # Switch back to PID and land
#         print("END: Switching to controller 1")
#         cf.param.set_value('stabilizer.controller', '1')
#         time.sleep(2.0)

#         print("Landing...")
#         for y in range(10):
#             cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 200)
#             time.sleep(0.2)

#         cf.commander.send_stop_setpoint()
#         time.sleep(0.1)

# if __name__ == '__main__':
#     simple_hover()