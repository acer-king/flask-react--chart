# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:12:37 2021

@author: ericp
"""

import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import math


#########################################################

#########################################################

#########################################################
vars = {}


def getDatas():
    results = []
    Case = 1
    if Case == 1:
        #    df_Mission = pd.read_excel('Data\CYCLE_WLTC.xlsx')
        #    Tps                     = np.zeros((len(df_Mission),1))
        #    Speed                   = np.zeros((len(df_Mission),1))
        #    for i in range(0,len(df_Mission)):
        #        Tps[i][0]=df_Mission['Time (s)'][i]
        #        Speed[i][0]=df_Mission['Speed (m/s)'][i]
        #
        df_Mission = pd.read_excel('Data\CYCLE_WLTC.xlsx')
        ProfilDuration = df_Mission['Time (s)'][len(df_Mission)-1]
        StepTime = 0.1
        N = round(ProfilDuration/StepTime)
        TimeVector = np.linspace(0, ProfilDuration, N, endpoint=True)
        Tps = np.zeros((len(TimeVector), 1))
        for i in range(0, len(TimeVector)):
            Tps[i][0] = TimeVector[i]
        Speed = np.zeros((len(TimeVector), 1))
        Speed_interp = interp1d(
            df_Mission['Time (s)'], df_Mission['Speed (m/s)'], bounds_error=False)
        for i in range(0, len(TimeVector)):
            Speed[i][0] = Speed_interp(TimeVector[i])

    elif Case == 2:
        df_Mission = pd.read_excel('Data\CYCLE_NEDC.xlsx')
        ProfilDuration = df_Mission['Time (s)'][len(df_Mission)-1]
        StepTime = 0.1
        N = round(ProfilDuration/StepTime)
        TimeVector = np.linspace(0, ProfilDuration, N, endpoint=True)
        Tps = np.zeros((len(TimeVector), 1))
        for i in range(0, len(TimeVector)):
            Tps[i][0] = TimeVector[i]
        Speed = np.zeros((len(TimeVector), 1))
        Speed_interp = interp1d(
            df_Mission['Time (s)'], df_Mission['Speed (m/s)'], bounds_error=False)
        for i in range(0, len(TimeVector)):
            Speed[i][0] = Speed_interp(TimeVector[i])

    elif Case == 3:
        df_Mission = pd.read_excel('Data\CYCLE_TRACK.xlsx')
        ProfilDuration = df_Mission['Time (s)'][len(df_Mission)-1]
        StepTime = 0.1
        N = round(ProfilDuration/StepTime)
        TimeVector = np.linspace(0, ProfilDuration, N, endpoint=True)
        Tps = np.zeros((len(TimeVector), 1))
        for i in range(0, len(TimeVector)):
            Tps[i][0] = TimeVector[i]
        Speed = np.zeros((len(TimeVector), 1))
        Speed_interp = interp1d(
            df_Mission['Time (s)'], df_Mission['Speed (m/s)'], bounds_error=False)
        for i in range(0, len(TimeVector)):
            Speed[i][0] = Speed_interp(TimeVector[i])

    Tps_filtered = np.zeros((len(Speed), 1))
    Speed_filtered = np.zeros((len(Speed), 1))
    ForceMotiveRequested = np.zeros((len(Speed), 1))
    PowerMotiveRequested = np.zeros((len(Speed), 1))
    PowerMotorRequested = np.zeros((len(Speed), 1))
    PowerBatteryRequested = np.zeros((len(Speed), 1))
    EnergyBatteryRequestedWs = np.zeros((len(Speed), 1))
    EnergyBatteryRequestedkWh = np.zeros((len(Speed), 1))
    dVdt = np.zeros((len(Speed), 1))

    FilterParam = 150
    for i in range(FilterParam, len(Speed)):
        Speed_filtered[i][0] = np.mean(
            df_Mission['Speed (m/s)'][i-FilterParam:i])
    #    Tps_filtered[i][0]=df_Mission['Time (s)'][i];

    if Case == 1:
        Te_Main = 0.1

    if Case == 2:
        Te_Main = 0.1

    if Case == 3:
        Te_Main = 0.1
    #
    # if Case ==3:
    #    Speed = Speed_filtered
    #    Te_Main = 0.01;
    #
    # if Case ==4:
    #    Speed = Speed_filtered
    #    Te_Main = 0.01;
    #
    # if Case ==5:
    #    Speed = Speed_filtered
    #    Te_Main = 0.01;
    #
    # if Case ==6:
    #    Speed = Speed_filtered
    #    Te_Main = 0.01;
    #
    #

    #plt.plot( Tps_filtered, Speed_filtered)

    # Vehicle Parameters _ User Inputs
    # --------------------------------
    # Vehicle Mass         [kg]
    global vars
    m_veh = vars['vihicleMass'] if vars else 1500
    RWheel = vars['wheelRadius'] if vars else 0.314  # Wheel radius [m]
    Fro = vars['rollingRsistance'] if vars else 0.01  # Rolling Resistance [--]
    SCX = vars['scx'] if vars else 0.83  # SCX  [--]
    alpha_deg = vars['roadAngle'] if vars else 0    # Road Angle  [deg]
    # Signle SPeed Ratio [#]
    Gear_Ratio_EM = vars['singleSpeedRadius6'] if vars else 6.31

    # Powertrain Efficiencies Parameters _ User Inputs
    # --------------------------------
    # Transmission Efficiency  [--]
    etaTransmission = vars['tranEfficiency'] if vars else 0.95
    # Inverter Efficiency  [--]
    etaInverter = vars['inverterEfficiency'] if vars else 0.97
    # Motor Efficiency  [--]
    etaMotor = vars['motorEfficiency'] if vars else 0.95

    # Number of Reprtition of the Mission Profile _ User Inputs
    # --------------------------------
    NbCycles = vars['numberCycle'] if vars else 3  # Number of Cycles [--]

    # Generic Parameters Not to appear in the User Interface
    # --------------------------------
    g = 9.8     # accélération field     [m²/s]
    rho = 1.184  # Air density [kg/m3]
    vWind = 0  # Wind speed |m/s]
    alpha = alpha_deg*3.14/180  # Road Angle [rad]

    TpsCycle = Tps
    SpeedCycle = Speed

    if NbCycles >= 2:

        SpeedCyclePrev = Speed
        SpeedCycleNext = Speed

        SpeedCycle = np.concatenate((SpeedCyclePrev, SpeedCycleNext), axis=0)
        TpsCyclePrev = np.zeros((len(Speed), 1))
        TpsCycleNext = np.zeros((len(Speed), 1))

        for i in range(0, len(Speed)):
            TpsCyclePrev[i][0] = Tps[i]

        for i in range(0, len(Speed)):
            TpsCycleNext[i][0] = Tps[i]+Tps[len(Speed)-1][0]

        TpsCycle = np.concatenate((TpsCyclePrev, TpsCycleNext), axis=0)

        for i in range(1, NbCycles-1):
            TpsCyclePrev = TpsCycle
            TpsCycleNext = np.zeros((len(Speed), 1))
            SpeedCyclePrev = SpeedCycle

            for i in range(0, len(Speed)):
                TpsCycleNext[i][0] = Tps[i] + \
                    TpsCyclePrev[len(TpsCyclePrev)-1][0]

            TpsCycle = np.concatenate((TpsCyclePrev, TpsCycleNext), axis=0)
            SpeedCycle = np.concatenate(
                (SpeedCyclePrev, SpeedCycleNext), axis=0)

    results.append((TpsCycle, SpeedCycle))

    Speed_filtered = np.zeros((len(SpeedCycle), 1))
    ForceMotiveRequested = np.zeros((len(SpeedCycle), 1))
    PowerMotiveRequested = np.zeros((len(SpeedCycle), 1))
    PowerMotorRequested = np.zeros((len(SpeedCycle), 1))
    PowerBatteryRequested = np.zeros((len(SpeedCycle), 1))
    EnergyBatteryRequestedWs = np.zeros((len(SpeedCycle), 1))
    EnergyBatteryRequestedkWh = np.zeros((len(SpeedCycle), 1))
    EnergyRegenBatteryRequestedWs = np.zeros((len(SpeedCycle), 1))
    EnergyRegenBatteryRequestedkWh = np.zeros((len(SpeedCycle), 1))
    EnergyNetBatteryRequestedkWh = np.zeros((len(SpeedCycle), 1))
    dVdt = np.zeros((len(SpeedCycle), 1))
    Distance = np.zeros((len(SpeedCycle), 1))
    Distance = np.zeros((len(SpeedCycle), 1))
    nRot_EM_in_Radpersec = np.zeros((len(SpeedCycle), 1))
    nRot_EM_in_RPM = np.zeros((len(SpeedCycle), 1))
    Torque_EM = np.zeros((len(SpeedCycle), 1))

    for i in range(1, len(SpeedCycle)):
        dVdt[i][0] = (SpeedCycle[i][0]-SpeedCycle[i-1][0])/Te_Main
        ForceMotiveRequested[i][0] = (m_veh*dVdt[i][0] + m_veh*g*Fro*(1+3.6/100*SpeedCycle[i][0])*np.cos(
            alpha) + m_veh*g*np.sin(alpha) + 0.5*rho*SCX*(SpeedCycle[i][0]+vWind)*SpeedCycle[i][0]+vWind)
        PowerMotiveRequested[i][0] = ForceMotiveRequested[i][0] * \
            SpeedCycle[i][0]
        PowerMotorRequested[i][0] = PowerMotiveRequested[i][0]/etaTransmission
        PowerBatteryRequested[i][0] = PowerMotorRequested[i][0] / \
            etaInverter / etaMotor
        Distance[i][0] = Distance[i-1][0] + SpeedCycle[i-1][0]*Te_Main
        nRot_EM_in_Radpersec[i][0] = (
            SpeedCycle[i][0] / RWheel) * Gear_Ratio_EM
        nRot_EM_in_RPM[i][0] = (
            SpeedCycle[i][0] / RWheel)*Gear_Ratio_EM*30/np.pi
        Torque_EM[i][0] = PowerMotorRequested[i][0] / \
            (nRot_EM_in_Radpersec[i][0]+10)
        if PowerBatteryRequested[i][0] > 0:
            EnergyBatteryRequestedWs[i][0] = EnergyBatteryRequestedWs[i -
                                                                      1][0]+Te_Main*PowerBatteryRequested[i][0]
        else:
            EnergyBatteryRequestedWs[i][0] = EnergyBatteryRequestedWs[i-1][0]

        if PowerBatteryRequested[i][0] < 0:
            EnergyRegenBatteryRequestedWs[i][0] = EnergyRegenBatteryRequestedWs[i -
                                                                                1][0]+Te_Main*PowerBatteryRequested[i][0]
        else:
            EnergyRegenBatteryRequestedWs[i][0] = EnergyRegenBatteryRequestedWs[i-1][0]

        EnergyBatteryRequestedkWh[i][0] = EnergyBatteryRequestedWs[i][0]/1000/3600
        EnergyRegenBatteryRequestedkWh[i][0] = EnergyRegenBatteryRequestedWs[i][0]/1000/3600
        EnergyNetBatteryRequestedkWh[i][0] = EnergyBatteryRequestedkWh[i][0] + \
            EnergyRegenBatteryRequestedkWh[i][0]

    results.append(TpsCycle)

    results.append(PowerMotiveRequested.tolist())

    results.append(PowerBatteryRequested.tolist())

    results.append(EnergyBatteryRequestedkWh.tolist())

    # Fonction Loop Profiles
    NbCycles = 3
    TpsCycle = Tps
    SpeedCycle = Speed

    def MissionProfileCar(Tps, Speed, NbCycles):

        if NbCycles == 1:
            TpsCycle = Tps
            SpeedCycle = Speed

        if NbCycles >= 2:

            SpeedCyclePrev = Speed
            SpeedCycleNext = Speed

            SpeedCycle = np.concatenate(
                (SpeedCyclePrev, SpeedCycleNext), axis=0)
            TpsCyclePrev = np.zeros((len(Speed), 1))
            TpsCycleNext = np.zeros((len(Speed), 1))

            for i in range(0, len(Speed)):
                TpsCyclePrev[i][0] = Tps[i]

            for i in range(0, len(Speed)):
                TpsCycleNext[i][0] = Tps[i]+Tps[len(Speed)-1][0]

            TpsCycle = np.concatenate((TpsCyclePrev, TpsCycleNext), axis=0)

            for i in range(1, NbCycles-1):
                TpsCyclePrev = TpsCycle
                TpsCycleNext = np.zeros((len(Speed), 1))
                SpeedCyclePrev = SpeedCycle

                for i in range(0, len(Speed)):
                    TpsCycleNext[i][0] = Tps[i] + \
                        TpsCyclePrev[len(TpsCyclePrev)-1][0]

                TpsCycle = np.concatenate((TpsCyclePrev, TpsCycleNext), axis=0)
                SpeedCycle = np.concatenate(
                    (SpeedCyclePrev, SpeedCycleNext), axis=0)

        return TpsCycle, SpeedCycle

    TpsCycle_, SpeedCycle_ = MissionProfileCar(Tps, Speed, NbCycles)
    print(TpsCycle_.flatten())
    results = (list(TpsCycle_.flatten()), list(SpeedCycle_.flatten()))
    return results
