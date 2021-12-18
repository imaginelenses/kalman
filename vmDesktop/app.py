from os import name, stat
from flask import Flask, request
import pyautogui as pg

import csv
import logging

from filter import State

# Define log file
LOG_FILE = 'app.log'

# Configure logger to log into log file
logging.basicConfig(filename=LOG_FILE, filemode='w')

# Disable pg failsafe (fail when cursor tries to move beyond screen)
pg.FAILSAFE = False

# Time interval 200ms
with open('readings.csv', 'w', newline='') as readings:
    writer = csv.DictWriter(readings, fieldnames=['x', 'a_mu'])
    writer.writeheader()

# FLASK APP
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route("/move/<float(signed=true):x>")
def move(x):
    """ Time update """
    # State extrapolation
    a_TU = State.a_MU
    v_TU = State.v_MU
    d_TU = State.d_MU
  
    # Covarience extrapolation
    p_TU_ACC = State.p_MU_ACC + State.Q_ACC
    p_TU_VEL = State.p_MU_VEL + State.Q_VEL
    p_TU_DIS = State.p_MU_DIS + State.Q_DIS

    """ Measurement Update """
    # Kalman Gain
    k_ACC = p_TU_ACC / (p_TU_ACC + State.R_ACC)
    k_VEL = p_TU_VEL / (p_TU_VEL + State.R_VEL)
    k_DIS = p_TU_DIS / (p_TU_DIS + State.R_DIS)

    # State update
    State.a_MU = a_TU + (k_ACC * (x - a_TU))
    v = State.u_avk + (State.a_MU * 0.2)
    State.v_MU = v_TU + (k_VEL * (v - v_TU))
    dis = (State.u_avk * 0.2) + (0.5 * State.a_MU * 0.04)
    State.d_MU = d_TU + (k_DIS * (dis - d_TU))

    # Covarience update
    State.p_MU_ACC = (1 - k_ACC) * p_TU_ACC
    State.p_MU_VEL = (1 - k_VEL) * p_TU_VEL
    State.p_MU_DIS = (1 - k_DIS) * p_TU_DIS

    # Displacement
    s_ak = (State.u_ak * 0.2) + (0.5 * State.a_MU * 0.04)
    s_avk = (State.u_avk * 0.2) + (0.5 * State.a_MU * 0.04)
    
    State.u_ak = State.u_ak + (State.a_MU * 0.2)
    State.u_avk = State.v_MU

    try:
        pg.moveRel((State.d_avdk - State.d_MU) * 10000000, 0)
        # pg.moveRel(x, 0)
    except:
        print('Error pg move')

    with open('readings.csv', 'a', newline='') as readings:
        writer = csv.DictWriter(readings, fieldnames=['x', 'a_mu'])
        writer.writerow({'x': x, 'a_mu': State.a_MU})

    State.d_ak = s_ak
    State.d_avk = s_avk
    State.d_avdk = State.d_MU

    return 'Move'

def serve():
    app.run(host='0.0.0.0', port='8080')

if __name__ == '__main__':
    serve()