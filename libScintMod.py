#!/usr/bin/python

#adapted from original code by Isar

import subprocess
import os
import sys
import time

#regWait = 0.05
regWait = 0.01
debug = True

#get SCROD register value
def fget_scint_reg(hs, lane, reg):
    laneNum = int(lane)
    if laneNum < 1 or laneNum > 2 :
        print("Invalid lane number")
        return None
    regNum = int(reg)
    reghex = 0x7600 + (laneNum-1)*2048 + 2 + regNum
    s1="reghs";
    s2=" %s fee32 %s" %(hs,hex(reghex));
    proc=subprocess.Popen([s1+s2," "],shell=True,stdout=subprocess.PIPE);
    line=proc.communicate();
    time.sleep(regWait)

    if int(len(line)) != 2:
        print("DID NOT READ REG")
        return None

    if line[0] == '':
        print("DID NOT READ REG")
        return None
    ss1=line[0][12:20];
    return int(ss1,16);

def fget_scint_reg_retry(hs, lane, reg):
    maxTry = 10
    val = None
    for test in range(0,maxTry,1):
        val = fget_scint_reg(hs, lane, reg)
        if val != None:
            break
    return val

def checkRegInterface(hs, lane):
    return True
    #check trigger alive
    sys.stdout.flush()
    rval1 = fget_scint_reg_retry(hs, lane, 0)
    if rval1 == None:
        print("----COULD NOT CHECK REGISTER INTERFACE----------")
        return False
    time.sleep(1)
    rval2 = fget_scint_reg_retry(hs, lane, 0)
    if rval2 == None:
        print("----COULD NOT CHECK REGISTER INTERFACE----------")
        return False
    sys.stdout.flush()
    if (rval1==rval2): #PROBLEM - trigger dead - ask user to restart trigger
        print("----DEAD TRIG - RESTART TRIGGER on TTD1----------")
        return False
    print("----REGISTER INTERFACE OK----------")
    return True

#set SCROD register value
def fset_scint_reg(hs,lane,reg,val):
    x=int(reg/16)
    y=reg & 15;

    r=(val & 0xf000) / 0x1000;
    t=(val & 0x0f00) / 0x0100;
    q=(val & 0x00f0) / 0x0010;
    w=(val & 0x000f) / 0x0001; 
    
    #print lane, reg, val, x, y, r
    s="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s)' | ~/hsprogs/reghs %s stream -" %(hex(0xf2),hex(lane*16+0xA), hex(0xf*16+x),hex(y*16+r),hex(t*16+q),hex(w*16+0x8),hex(0xf2),hex(lane*16+0xA), hex(0xf*16+x),hex(y*16+r),hex(t*16+q),hex(w*16+0x8),hs)
    #print s
    os.system(s);
    time.sleep(regWait)

#get channel scaler variable
def fget_scint_scaler(hs,lane,dc):
    laneNum = int(lane)
    if laneNum < 1 or laneNum > 2 :
        print("Invalid lane number")
        return None
    dcNum = int(dc)
    if dcNum < 0 or dcNum > 9 :
        print("Invalid lane number")
        return None
    gpL=10 
    gpH=40
    #q=fget_scint_reg(hs,lane,gpL+dc);
    #w=fget_scint_reg(hs,lane,gpH+dc);
    q = fget_scint_reg_retry(hs,laneNum,gpL+dcNum)
    w = fget_scint_reg_retry(hs,laneNum,gpH+dcNum)
    if (q == None) or (w == None):
        print "FAILED TO READ SCINT SCALER"
        return None
    return q+w*65536

#set channel threshold DAC value
def fset_scint_threshold(hs,lane,dc,ch,THval):
    rH=((ch*2) & 0xf0) / 0x10
    rL=((ch*2) & 0x0f) / 0x01
    t=(THval & 0x0f00) / 0x0100
    q=(THval & 0x00f0) / 0x0010 
    w=(THval & 0x000f) / 0x0001

    s1="%s, %s, %s,%s,%s,%s" %(hex(0xf2),hex(lane*16+0xB), hex(dc*16+rH),hex(rL*16+0),hex(t*16+q),hex(w*16+0x8))
    s="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s, %s)' | ~/hsprogs/reghs %s stream -" %(s1,s1,hs)
    ##print s
    os.system(s);
    time.sleep(regWait)

#set channel HV trim DAC value
def fset_scint_hv(hs,lane,dc,ch,DACval):
    q=(DACval & 0x00f0) / 0x0010;
    w=(DACval & 0x000f) / 0x0001;
    s1="%s, %s, %s,%s,%s,%s" %(hex(0xf2),hex(lane*16+0xC), hex(0x0*16+dc),hex(ch*16+0),hex(0*16+q),hex(w*16+0x8));
    s="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s, %s)' | ~/hsprogs/reghs %s stream -" %(s1,s1,hs)
    #print s
    os.system(s);
    time.sleep(regWait)

#loop over ASIC + channels
def fset_scint_hv_custom(hs,lane,dcs,chs,val):
  for Iasic in dcs:
    for Ich in chs:
      if debug == True:
        print( "Set HV\t",str(hs),"\t",str(lane),"\t",str(Iasic),"\t",str(Ich),"\t",str(val))
      fset_scint_hv(hs,lane,Iasic,Ich,val);
      fset_scint_hv(hs,lane,Iasic,Ich,val);

def fset_scint_th_custom(hs,lane,dcs,chs,thval):
  for Iasic in dcs:
    for Ich in chs:
      if debug == True:
        print( "Set DAC\t",str(hs),"\t",str(lane),"\t",str(Iasic),"\t",str(Ich),"\t",str(thval))
      fset_scint_threshold(hs,lane,Iasic,Ich,thval)
      fset_scint_threshold(hs,lane,Iasic,Ich,thval)

