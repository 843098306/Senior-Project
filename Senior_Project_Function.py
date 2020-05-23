import pandas as pd
import numpy as np
import random
from random import expovariate as nexttime
import matplotlib.pyplot as plt
import sys
import cv2
import glob
sys.path.append('../../Python')
from time import time as t
import seaborn as sns
import os
import math 
import sympy
import datetime as dt
from sympy import *

# ArrivalRate: The rate of people coming to the station to pick up bikes
# LeaveRate: The rate of people coming to the station to return bikes
# BikesInUseInitial: Initial number of bikes in use
# BikesAtStationInitial: Initial number of bikes at the station
# Capacaity: Capacity of the station
# n: number of time steps
def BirthDeathsimulate(ArrivalRate,LeaveRate,BikesInUseInitial,BikesAtStationInitial,Capacaity,n):
    BikesInUseList = []
    BikesAtStationList = []
    WaitListPick = []
    WaitListReturn = []
    Time = []

    BikesInUseList.append(BikesInUseInitial)
    BikesAtStationList.append(BikesAtStationInitial)
    WaitListPick.append(0)
    WaitListReturn.append(0)
    Time.append(0)

    BikesInUse = BikesInUseInitial
    BikesAtStation = BikesAtStationInitial
    WaitPick = 0
    WaitReturn = 0

    for i in range(n):
        prob = random.random()
        event = nexttime(ArrivalRate + LeaveRate*BikesInUse) 
        Time.append(event + Time[-1]) # record time index
        ArrivalProb = ArrivalRate/(ArrivalRate + LeaveRate*BikesInUse)
        
        # A person arrive to pick up a bike
        if(prob >= ArrivalProb):
            if(BikesAtStation < Capacaity):
                if(WaitPick > 0):
                    # No Reduce in BikeInUse since someone returns a bike that is picked up by person in pick up wait list
                    WaitPick = WaitPick - 1
                else:
                    BikesAtStation = BikesAtStation + 1
                    BikesInUse = BikesInUse - 1
            else:
                if(BikesAtStation == Capacaity):
                    if(WaitPick > 0):
                        # Same as above
                        WaitPick = WaitPick - 1
                    else:
                        if(BikesInUse > 0):
                            BikesInUse = BikesInUse - 1
                            WaitReturn = WaitReturn + 1
    
        # A person arrive to return a bike
        else:
            if(BikesAtStation > 0):
                BikesInUse = BikesInUse + 1
                if(WaitReturn > 0):
                    WaitReturn = WaitReturn - 1
                else:
                    BikesAtStation = BikesAtStation - 1
            else:
                if(WaitReturn > 0):
                    WaitReturn = WaitReturn - 1
                    BikesInUse = BikesInUse + 1
                else:
                    # Set the maximum of waiting list of picking to 10
                    if(WaitPick < 10):
                        WaitPick = WaitPick + 1
    
        BikesInUseList.append(BikesInUse)
        BikesAtStationList.append(BikesAtStation)
        WaitListPick.append(WaitPick)
        WaitListReturn.append(WaitReturn)    
    return Time,BikesInUseList,BikesAtStationList,WaitListPick,WaitListReturn

# See BirthDeathsimulate Function
def Simplesimulate(ArrivalRate,LeaveRate,BikesInUseInitial,BikesAtStationInitial,Capacaity,n):
    BikesInUseList = []
    BikesAtStationList = []
    WaitListPick = []
    WaitListReturn = []
    Time = []

    BikesInUseList.append(BikesInUseInitial)
    BikesAtStationList.append(BikesAtStationInitial)
    WaitListPick.append(0)
    WaitListReturn.append(0)
    Time.append(0)

    BikesInUse = BikesInUseInitial
    BikesAtStation = BikesAtStationInitial
    WaitPick = 0
    WaitReturn = 0
    ArrivalProb = ArrivalRate/(ArrivalRate + LeaveRate)

    for i in range(n):
        prob = random.random()
        event = nexttime(ArrivalRate + LeaveRate)
        Time.append(event + Time[-1])
    
        if(prob >= ArrivalProb):
            if(BikesAtStation < Capacaity):
                if(WaitPick > 0):
                    # No Reduce in BikeInUse since someone returns a bike that is picked up by person in pick up wait list
                    WaitPick = WaitPick - 1
                else:
                    BikesAtStation = BikesAtStation + 1
                    BikesInUse = BikesInUse - 1
            else:
                if(BikesAtStation == Capacaity):
                    if(WaitPick > 0):
                        # Same as above
                        WaitPick = WaitPick - 1
                    else:
                        if(BikesInUse > 0):
                            BikesInUse = BikesInUse - 1
                            WaitReturn = WaitReturn + 1
    

        else:
            if(BikesAtStation > 0):
                BikesInUse = BikesInUse + 1
                if(WaitReturn > 0):
                    WaitReturn = WaitReturn - 1
                else:
                    BikesAtStation = BikesAtStation - 1
            else:
                if(WaitReturn > 0):
                    WaitReturn = WaitReturn - 1
                    BikesInUse = BikesInUse + 1
                else:
                    # Set the maximum of waiting list of picking to 10
                    if(WaitPick < 10):
                        WaitPick = WaitPick + 1
    
        BikesInUseList.append(BikesInUse)
        BikesAtStationList.append(BikesAtStation)
        WaitListPick.append(WaitPick)
        WaitListReturn.append(WaitReturn)    
    return Time,BikesInUseList,BikesAtStationList,WaitListPick,WaitListReturn

# List: An array of state at each time index, usually it is the state of waiting list (e.g. 0,1,2,3...,n)
# Time: Time index
def time_distribution_cal(List,Time):
    output = {}
    for i in range(len(Time) - 1):
        num = List[i]
        if num in output:
            output[num] = output[num] + (Time[i+1]-Time[i])
        else:
            output[num] = (Time[i+1]-Time[i])
    return output;

# WaitList: An array of state at each time index, usually it is the state of waiting list (e.g. 0,1,2,3...,n)
# Time: Time index
def calculate_waittime(Time,WaitList):
    length = len(Time)
    sum = 0
    for i in range(length - 1):
        sum += WaitList[i]*(Time[i+1]-Time[i])
        
    return sum

def calculate_waitpeople(WaitList):
    length = len(WaitList)
    sum = 0
    for i in range(length - 1):
        if(WaitList[i+1]>=WaitList[i]):
            sum += WaitList[i+1] - WaitList[i]        
    return sum

def simulate_avg(ArrivalRate,LeaveRate,BikesInUseInitial,BikesAtStationInitial,Capacaity):
    data = pd.DataFrame(columns= ["Wait_Pick","Wait_Return"])
    for i in range(1,100):
        Time,BikesInUseList,BikesAtStationList,WaitListPick,WaitListReturn = BirthDeathsimulate(ArrivalRate,LeaveRate,BikesInUseInitial,BikesAtStationInitial,Capacaity)
        time = Time[-1]
        waitp_sumtime = calculate_waittime(Time,WaitListPick)
        waitp_sumpeople = calculate_waitpeople(WaitListPick)
        if(waitp_sumpeople == 0):
            waitp_avg = 0
        else:
            waitp_avg = waitp_sumtime/waitp_sumpeople
        
        waitr_sumtime = calculate_waittime(Time,WaitListReturn)
        waitr_sumpeople = calculate_waitpeople(WaitListReturn)
        if(waitr_sumpeople == 0):
            waitr_avg = 0
        else:
            waitr_avg = waitr_sumtime/waitr_sumpeople

        line = {}
        line["Wait_Pick"] = waitp_avg
        line["Wait_Return"] = waitr_avg
        data1 = pd.DataFrame([line])
        data = pd.concat([data,data1],sort =False)
    return data

# d: An array of values
# target: Weight factor, default setting to 1.
def normalize(d, target=1.0):
    raw = sum(d.values())
    factor = target/raw
    return {key:value*factor for key,value in d.items()}

# format: variable name
# *values: its value
def printf(format, *values):
    print(format % values )

# lambdav: input lambda value - arrival rate
# mue: input mu value - return rate
# b: total number of bikes in the system
# CWait: maximum size of waiting list
def calculatex_0(lambdav,mue,b = 30,Cwait = 10):
    x = symbols('x')
    exp1 = 0
    exp2 = 0
    for i in range(b+1):
        exp1 += x*lambdav**i/(mue**(i)*factorial(i))
    
    for j in range(1,Cwait+1):
        exp2 += x*lambdav**(b + j)/(mue**(b+j)*b**(j)*factorial(b))

    Ec = Eq(exp1 + exp2,1)
    sol = solve(Ec,x)
    x_0 = sol[0]
    return x_0

# t: total number of bikes
# u: input mu value - return rate
# c: maximum size of waiting list
# x: x_0 calculated by calculatex_0
# lambda3: input lambda value - arrival rate
def calwaittimestationary(t,u,c,x,lambdae):
    Dict1 = {}
    Dict2 = {}
    test = {}
    waitatzero = 0
    waitpicksum = 0
    waitreturnsum = 0
    
    for i in range(t):
        temp = x*(lambdae**i)/(math.factorial(i)*u**i)
        waitatzero += temp
        
    for i in range(c + 1):
        n = float(lambdae**(i + t)/(math.factorial(t)*math.pow(t,i)*math.pow(u,t+i)))
        Dict1[i] = n*x*i
        test[i] = n*x
        waitpicksum += Dict1[i]
    
    for i in range(0,10):
        r = lambdae**(i)/(math.pow(u,i)*math.factorial(i))
        Dict2[i] = (10 - i)*r*x
        waitreturnsum +=  Dict2[i]
        
    test[0] += waitatzero
    waittotal = waitpicksum+waitreturnsum
    return waittotal,test

# lambdav: input lambda value - arrival rate
def calculatewaittimelist(lambdav):
    temp = []
    for i in range(5,36):
        x_0 = calculatex_0(lambdav = lambdav,mue = 1/i, b = 30 , Cwait = 10)
        waittotal,test = calwaittimestationary(30,1/i,10,x_0,lambdav)
        temp.append(waittotal)

    return temp 
















