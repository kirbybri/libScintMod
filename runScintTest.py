#!/usr/bin/python

import subprocess
import os
import sys
import time
import pickle
from libScintMod import fget_scint_reg
from libScintMod import fget_scint_reg_retry
from libScintMod import fset_scint_reg
from libScintMod import fset_scint_hv
from libScintMod import fset_scint_threshold
from libScintMod import fget_scint_scaler
from libScintMod import fset_scint_hv_custom
from libScintMod import fset_scint_th_custom
from libScintMod import checkRegInterface

##VARIOUS GLOBAL VARIABLES
wait0=60.0/500.0 #original
#wait0=120.0/500.0
#wait0=10.0/500.0
T0=4.0*65536.0/63.5e6
#wait = T0*2.0
wait=wait0
if (T0>wait0):
    wait=T0*2.0+wait0

#put readout into known state, disable triggers
def doInitialize(hs,lane,defaultTh,defaultHV):
    laneNum = int(lane)
    defaultThNum = int(defaultTh)
    defaultHVNum = int(defaultHV)
    if (hs != "-a") and (hs != "-b") and (hs != "-c") and (hs != "-d"):
        return None
    if laneNum < 1 or laneNum > 2 :
        return None
    if defaultThNum < 0 or defaultThNum > 4095 :
        return None
    if defaultHVNum < 0 or defaultHVNum > 255 :
        return None

    fset_scint_reg(hs,lane,47,4) # set Reg 2F such that T0=4ms
    fset_scint_reg(hs,lane,47,4) # set Reg 2F such that T0=4ms
    fset_scint_reg(hs,lane,39,0) # set Reg 39 dec masks all asics for readout such that no ASIC produces readable hits- that way pdaq wont generate QT data 
    fset_scint_reg(hs,lane,39,0) # set Reg 39 dec masks all asics for readout such that no ASIC produces readable hits- that way pdaq wont generate QT data 

    #set default HV + DACs
    EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    fset_scint_hv_custom(hs,lane,EntireAsics,EntireCHs,defaultHVNum)
    fset_scint_th_custom(hs,lane,EntireAsics,EntireCHs,defaultThNum)

def getScalerVsDAC(hs,lane,asic,ch,defaultTh):
    #test inputs
    laneNum = int(lane)
    asicNum = int(asic)
    chNum = int(ch)
    defaultThNum = int(defaultTh)
    if (hs != "-a") and (hs != "-b") and (hs != "-c") and (hs != "-d"):
        return None
    if laneNum < 1 or laneNum > 2 :
        return None
    if asicNum < 0 or asicNum > 9 :
        return None
    if chNum < 0 or chNum > 14 :
        return None
    if defaultThNum < 0 or defaultThNum > 4095 :
        return None
    if checkRegInterface(hs,lane) == False:
        print "Skipping scaler vs DAC measurement for\t" + str(hs) + "\tlane " + str(laneNum) + "\tASIC " + str(asicNum) + "\tch " + str(chNum)
        return None

    scalerVsDac = []
    numRW = 2
    numTest = 3

    #measure scaler vs threshold DAC value
    print "Measuring scaler vs DAC for lane " + str(laneNum) + "\tASIC " + str(asicNum) + " ch " + str(chNum)
    for th in range (3575,3550,-1):
    #for th in range (3700,3500,-1):
        #set threshold multiple times to deal with flakey interface
        for regRW in range(0,numRW,1):
            fset_scint_threshold(hs,laneNum,asicNum,chNum,th)

        #test scalers multiple times to check for inconsistent results
        freqs = []
        for test in range(0,numTest,1):
            scalers = None
            for regRW in range(0,numRW,1):
                time.sleep(wait);#wait for counters to settle
                scalers=fget_scint_scaler(hs,laneNum,asicNum)
            if scalers == None:
                print "Failed to read trigger scaler, DAC " + str(th) 
                continue 
            freq=scalers/T0/1000.0; #in kHz
            #freqs.append(freq)
            freqs.append(scalers)
            print "DAC " + str(th) + "\tRate " +  str(freq)
        scalerVsDac.append( [th,freqs] )

    #return threshold to default value
    for regRW in range(0,numRW,1):
        fset_scint_threshold(hs,laneNum,asicNum,chNum,defaultThNum)

    if len(scalerVsDac) == 0 :
        return None
    return scalerVsDac

def runTest():
    #test constants
    link = '-b'
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #stop if register interface is broken
    checkRegInterface(link,lane)
    if checkRegInterface(link,lane) == False:
        return None
    #check if sane register values returned
    checkRegs(link,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(link,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data

    #multi-channel scaler vs DAC study
    #for asic in [0,1,2,3,4,5,6,7,8,9]:
    for asic in [0]:
        for ch in [0]:
            scalerVsDac = getScalerVsDAC(link,lane,asic,ch,defaultTh)
            if scalerVsDac != None :
                results[(link,lane,asic,ch,defaultTh,defaultHV)] = scalerVsDac
    
    #save results dictionary and close file
    outputFile = open('scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runDacScan():
    #test constants
    link = '-a'
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #initialize
    for link in ['-a']:
        for lane in [1,2]:
            #stop if register interface is broken
            checkRegInterface(link,lane)
            if checkRegInterface(link,lane) == False:
                continue
            #initialize threshold + HV to effecitivelt OFF
            doInitialize(link,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data
    #multi-channel scaler vs DAC study
    for link in ['-a']:
        for lane in [1,2]:
            #stop if register interface is broken
            checkRegInterface(link,lane)
            if checkRegInterface(link,lane) == False:
                continue
            for asic in [0]:
                for ch in [0]:
                    scalerVsDac = getScalerVsDAC(link,lane,asic,ch,defaultTh)
                    if scalerVsDac != None :
                        results[(link,lane,asic,ch,defaultTh,defaultHV)] = scalerVsDac
    
    #save results dictionary and close file
    outputFile = open('outputDacScan_scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runHVTest():
    #test constants
    link = '-a'
    lane = 1
    defaultTh = 0
    defaultHV = 255
    numRW = 2

    #stop if register interface is broken
    checkRegInterface(link,lane)
    if checkRegInterface(link,lane) == False:
        return None
    #check if sane register values returned
    checkRegs(link,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(link,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data

    #single schannel scalers at various HV DAC
    for asic in [0]:
        for ch in [0]:
            for hvDac in (50,0):
                print "Testing HV DAC " + str(hvDac)
                for regRW in range(0,numRW,1):
                    fset_scint_hv(link,lane,asic,ch,hvDac)
                scalerVsDac = getScalerVsDAC(link,lane,asic,ch,defaultTh)
                if scalerVsDac != None :
                    results[(link,lane,asic,ch,defaultTh,hvDac)] = scalerVsDac
                #return to default HV DAC value
                for regRW in range(0,numRW,1):
                    fset_scint_hv(link,lane,asic,ch,hvDac)

    #save results dictionary and close file
    outputFile = open('hvScan_scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runTrigTest():
    #test constants
    link = '-a'
    defaultTh = 3400
    defaultHV = 0
    numRW = 2

    #stop if register interface is broken
    #checkRegInterface(link,1)
    #if checkRegInterface(link,1) == False:
    #    return None
    #checkRegInterface(link,2)
    #if checkRegInterface(link,2) == False:
    #    return None

    #turn off eveything
    EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    for regRW in range(0,numRW,1):
        fset_scint_hv_custom(link,1,EntireAsics,EntireCHs,255)
        fset_scint_th_custom(link,1,EntireAsics,EntireCHs,0)
        fset_scint_hv_custom(link,2,EntireAsics,EntireCHs,255)
        fset_scint_th_custom(link,2,EntireAsics,EntireCHs,0)

    #turn on single ASICs
    #EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireCHs=[0,8]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    for regRW in range(0,numRW,1):
        fset_scint_hv_custom(link,1,EntireAsics,EntireCHs,0)
        fset_scint_th_custom(link,1,EntireAsics,EntireCHs,3000)
        fset_scint_hv_custom(link,2,EntireAsics,EntireCHs,0)
        fset_scint_th_custom(link,2,EntireAsics,EntireCHs,3000)

    #turn on single channel in each lane
    #for regRW in range(0,numRW,1):
    #    fset_scint_hv(link,1,0,0,0)
    #    fset_scint_threshold(link,1,0,0,3700)

def runInitialize():
    #test constants
    link = '-b'
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #stop if register interface is broken 
    #checkRegInterface(link,lane)
    if checkRegInterface(link,lane) == False:
        return None 
    #check if sane register values returned
    checkRegs(link,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(link,lane,defaultTh,defaultHV)

def checkRegs(hs,lane):
    laneNum = int(lane)
    if (hs != "-a") and (hs != "-b") and (hs != "-c") and (hs != "-d"):
        return None
    if laneNum < 1 or laneNum > 2 :
        return None

    for test in range(0,10,1):
        regNum = int(test)
        rval1=fget_scint_reg_retry(hs,lane,regNum)
        #rval1=fget_scint_reg(hs,lane,regNum)
        rstr = "REG NUM" + "\t" + str(regNum) + "\t" + "REG VAL" + "\t" + str(rval1)
        print rstr

def main():
    print("START TEST SCRIPT")
    #checkRegs("-b",1)
    #runInitialize()
    runTest()
    #runHVTest()
    #runDacScan()
    #runTrigTest()
    print("DONE TEST SCRIPT")

if __name__ == '__main__':
    main()

