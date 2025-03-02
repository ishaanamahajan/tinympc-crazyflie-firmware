/**
 * ,---------,       ____  _ __
 * |  ,-^-,  |      / __ )(_) /_______________ _____  ___
 * | (  O  ) |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
 * | / ,--´  |    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
 *    +------`   /_____/_/\__/\___/_/   \__,_/ /___/\___/
 *
 * Crazyflie control firmware
 *
 * Copyright (C) 2019 Bitcraze AB
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, in version 3.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 *
 * controller_lqr.c - App layer application of a quaternion-based LQR.
 * This is one of the best existing LQR controllers you can find online
 * for Crazyflie.
 */


#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#include "app.h"

#include "FreeRTOS.h"
#include "task.h"

#include "controller.h"
#include "physicalConstants.h"
#include "log.h"
#include "param.h"
#include "num.h"
#include "math3d.h"

// Edit the debug name to get nice debug prints
#define DEBUG_MODULE "CONTROLLER_LQR"
#include "debug.h"

void appMain() {
  DEBUG_PRINT("Waiting for activation ...\n");

  while(1) {
    vTaskDelay(M2T(2000));

    // Remove the DEBUG_PRINT.
    // DEBUG_PRINT("Hello World!\n");
  }
}

#define NX  13  // no. state variable s       [position (3), attitude (4), body velocity (3), angular rate (3)]
#define NXt 12  // no. state error variables  [position (3), attitude (3), body velocity (3), angular rate (3)]
#define NU  4   // no. control input          [thrust, torque_x, torque_y, torque_z] scaled by UINT16_MAX
#define LQR_RATE RATE_50_HZ  // control frequency

static float K[NU][NXt] = {
  {-0.000001f,0.000009f,53000.0f,-0.000031f,-0.000007f,-0.000009f,-0.000001f,0.000006f,30000.0f,-0.000000f,0.000000f,-0.000000f},
  {4.874978f,-101.188832f,-0.000000f,659.749216f,31.851603f,3.390918f,4.665786f,-96.773025f,0.000000f,57.101199f,2.762597f,1.742091f},
  {101.025950f,-4.877204f,-0.000000f,31.865278f,658.744522f,8.592149f,96.620276f,-4.667871f,-0.000000f,2.763709f,57.019366f,4.412653f},
  {8.746378f,-3.485695f,-0.000000f,23.035438f,57.786754f,157.328755f,8.404659f,-3.349809f,-0.000000f,2.021870f,5.070811f,80.561687f},
};

static float x_error[NXt];  
static float control_input[NU];

// Struct for logging position information
static bool isInit = false;


void controllerOutOfTreeInit(void) {
  if (isInit) {
    return;
  }

  isInit = true;
}

bool controllerOutOfTreeTest() {
  // Always return true
  return true;
}

void controllerOutOfTree(control_t *control, const setpoint_t *setpoint, const sensorData_t *sensors, const state_t *state, const uint32_t tick) {
  // Control frequency
  if (!RATE_DO_EXECUTE(LQR_RATE, tick)) {
    return;
  }
  // Positon error, [m]
  x_error[0] = state->position.x - 1*setpoint->position.x;
  x_error[1] = state->position.y - 1*setpoint->position.y;
  x_error[2] = state->position.z - 1*setpoint->position.z;

  // Body velocity error, [m/s]                          
  x_error[6] = state->velocity.x - 1*setpoint->velocity.x;
  x_error[7] = state->velocity.y - 1*setpoint->velocity.y;
  x_error[8] = state->velocity.z - 1*setpoint->velocity.z;

  // Angular rate error, [rad/s]
  x_error[9]  = radians(sensors->gyro.x - 1*setpoint->attitudeRate.roll);   
  x_error[10] = radians(sensors->gyro.y - 1*setpoint->attitudeRate.pitch);
  x_error[11] = radians(sensors->gyro.z - 1*setpoint->attitudeRate.yaw);

  // struct quat attitude_g = qeye();  // goal attitude
  // struct quat attitude_g = mkquat(setpoint->attitudeQuaternion.x, 
  //                                 setpoint->attitudeQuaternion.y, 
  //                                 setpoint->attitudeQuaternion.z, 
  //                                 setpoint->attitudeQuaternion.w);  // do not have quat cmd

  struct vec desired_rpy = mkvec(radians(setpoint->attitude.roll), 
                                 radians(setpoint->attitude.pitch), 
                                 radians(setpoint->attitude.yaw));
  struct quat attitude_g = rpy2quat(desired_rpy);

  struct quat attitude = mkquat(
    state->attitudeQuaternion.x,
    state->attitudeQuaternion.y,
    state->attitudeQuaternion.z,
    state->attitudeQuaternion.w);  // current attitude

  struct quat attitude_gI = qinv(attitude_g);  
  struct quat q_error = qnormalize(qqmul(attitude_gI, attitude));
  struct vec phi = quat2rp(q_error);  // quaternion to Rodriquez parameters
  
  // Attitude error
  x_error[3] = phi.x;
  x_error[4] = phi.y;
  x_error[5] = phi.z;

  // Matrix multiplication, compute control input
  for (int i = 0; i < STABILIZER_NR_OF_MOTORS; i++){
    control_input[i] = 0;

    for (int j = 0; j < NXt; j++) {
      control_input[i] += -K[i][j] * x_error[j];
    }
  }

  // Compensate for gravity 
  control_input[0] += (setpoint->thrust + 0.03f * GRAVITY_MAGNITUDE) * UINT16_MAX;

  if (setpoint->mode.z == modeDisable) {
    control->thrustSi = 0.0f;
    control->torque[0] =  0.0f;
    control->torque[1] =  0.0f;
    control->torque[2] =  0.0f;
  } else {
    control->thrustSi = control_input[0];  // [UINT16_MAX * N]
    control->torqueX = control_input[1];   // [N.m]
    control->torqueY = control_input[2];
    control->torqueZ = control_input[3];
  } 
  control->controlMode = controlModeForceTorqueScaled;
  
  // DEBUG_PRINT("%d.%.6d", (int)K[0][2], (int)((K[0][2]-(int)K[0][2])*1000000));
  // DEBUG_PRINT("K[0][2] = %f",(double)K[0][2]);

  // control->thrustSi = 0.0f;
  // control->torque[0] =  0.0f;
  // control->torque[1] =  0.0f;
  // control->torque[2] =  0.0f;  
}

/**
 * Tunning variables for the full state quaternion LQR controller
 */
PARAM_GROUP_START(ctrlLQR)
/**
 * @brief K gain
 */
PARAM_ADD(PARAM_FLOAT, k11, &K[0][0])
PARAM_ADD(PARAM_FLOAT, k21, &K[1][0])
PARAM_ADD(PARAM_FLOAT, k31, &K[2][0])
PARAM_ADD(PARAM_FLOAT, k41, &K[3][0])

PARAM_ADD(PARAM_FLOAT, k12, &K[0][1])
PARAM_ADD(PARAM_FLOAT, k22, &K[1][1])
PARAM_ADD(PARAM_FLOAT, k32, &K[2][1])
PARAM_ADD(PARAM_FLOAT, k42, &K[3][1])

PARAM_ADD(PARAM_FLOAT, k13, &K[0][2])
PARAM_ADD(PARAM_FLOAT, k23, &K[1][2])
PARAM_ADD(PARAM_FLOAT, k33, &K[2][2])
PARAM_ADD(PARAM_FLOAT, k43, &K[3][2])

PARAM_ADD(PARAM_FLOAT, k14, &K[0][3])
PARAM_ADD(PARAM_FLOAT, k24, &K[1][3])
PARAM_ADD(PARAM_FLOAT, k34, &K[2][3])
PARAM_ADD(PARAM_FLOAT, k44, &K[3][3])

PARAM_ADD(PARAM_FLOAT, k15, &K[0][4])
PARAM_ADD(PARAM_FLOAT, k25, &K[1][4])
PARAM_ADD(PARAM_FLOAT, k35, &K[2][4])
PARAM_ADD(PARAM_FLOAT, k45, &K[3][4])

PARAM_ADD(PARAM_FLOAT, k16, &K[0][5])
PARAM_ADD(PARAM_FLOAT, k26, &K[1][5])
PARAM_ADD(PARAM_FLOAT, k36, &K[2][5])
PARAM_ADD(PARAM_FLOAT, k46, &K[3][5])

PARAM_ADD(PARAM_FLOAT, k17, &K[0][6])
PARAM_ADD(PARAM_FLOAT, k27, &K[1][6])
PARAM_ADD(PARAM_FLOAT, k37, &K[2][6])
PARAM_ADD(PARAM_FLOAT, k47, &K[3][6])

PARAM_ADD(PARAM_FLOAT, k18, &K[0][7])
PARAM_ADD(PARAM_FLOAT, k28, &K[1][7])
PARAM_ADD(PARAM_FLOAT, k38, &K[2][7])
PARAM_ADD(PARAM_FLOAT, k48, &K[3][7])

PARAM_ADD(PARAM_FLOAT, k19, &K[0][8])
PARAM_ADD(PARAM_FLOAT, k29, &K[1][8])
PARAM_ADD(PARAM_FLOAT, k39, &K[2][8])
PARAM_ADD(PARAM_FLOAT, k49, &K[3][8])

PARAM_ADD(PARAM_FLOAT, k110, &K[0][9])
PARAM_ADD(PARAM_FLOAT, k210, &K[1][9])
PARAM_ADD(PARAM_FLOAT, k310, &K[2][9])
PARAM_ADD(PARAM_FLOAT, k410, &K[3][9])

PARAM_ADD(PARAM_FLOAT, k111, &K[0][10])
PARAM_ADD(PARAM_FLOAT, k211, &K[1][10])
PARAM_ADD(PARAM_FLOAT, k311, &K[2][10])
PARAM_ADD(PARAM_FLOAT, k411, &K[3][10])

PARAM_ADD(PARAM_FLOAT, k112, &K[0][11])
PARAM_ADD(PARAM_FLOAT, k212, &K[1][11])
PARAM_ADD(PARAM_FLOAT, k312, &K[2][11])
PARAM_ADD(PARAM_FLOAT, k412, &K[3][11])

PARAM_GROUP_STOP(ctrlLQR)

/**
 * Logging variables for the command and reference signals for the
 * LQR controller
 */

LOG_GROUP_START(ctrlLQR)

LOG_ADD(LOG_FLOAT, e_x, &x_error[0])
LOG_ADD(LOG_FLOAT, e_y, &x_error[1])
LOG_ADD(LOG_FLOAT, e_z, &x_error[2])

LOG_ADD(LOG_FLOAT, e_roll,  &x_error[3])
LOG_ADD(LOG_FLOAT, e_pitch, &x_error[4])
LOG_ADD(LOG_FLOAT, e_yaw,   &x_error[5])

LOG_ADD(LOG_FLOAT, e_vx, &x_error[6])
LOG_ADD(LOG_FLOAT, e_vy, &x_error[7])
LOG_ADD(LOG_FLOAT, e_vz, &x_error[8])

LOG_ADD(LOG_FLOAT, e_vroll,  &x_error[9])
LOG_ADD(LOG_FLOAT, e_vpitch, &x_error[10])
LOG_ADD(LOG_FLOAT, e_vyaw,   &x_error[11])

LOG_GROUP_STOP(ctrlLQR)