#!/bin/sh
#
# For KLM, CDC, ECL COPPERs slot A,B
#
#    print 'Usage : RecvSendCOPPER.py <COPPER hostname> <COPPER node ID> <bit flag of FINNESEs> <Use NSM(Network Shared Memory)? yes=1/no=0> <NSM nodename>'
# bit flag of FINESSE
# slot a : 1, slot b : 2, slot c : 4, slot d : 8
# e.g. slot abcd -> bitflag=15, slot bd -> bit flag=10
/usr/bin/xterm -fn 7x14 -geometry 40x7+200+150  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/start_copper_mono.sh cpr7001 117440513 2 0 1; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x7+500+150  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/start_copper_mono.sh cpr7002 117440514 0 0 1; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x7+800+150  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/start_copper_mono.sh cpr7003 117440515 0 0 1; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x7+1100+150 -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/start_copper_mono.sh cpr7004 117440516 0 0 1; sleep 3000000;" &


#
# basf2 program BEFORE eb0(event builder 0) on a readout PC
#
#    print 'Usage : RecvStream0.py <COPPER hostname> <Use NSM(Network Shared Memory)? yes=1/no=0> <port # of eb0> <NSM nodename>
/usr/bin/xterm -fn 7x14 -geometry 40x10+200+350  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/RecvStream2_mono.sh cpr7001 0 34001 hogehoge1000; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x10+500+350  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/RecvStream2_mono.sh cpr7002 0 34002 hogehoge1000; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x10+800+350  -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/RecvStream2_mono.sh cpr7003 0 34003 hogehoge1000; sleep 3000000;" &
#/usr/bin/xterm -fn 7x14 -geometry 40x10+1100+350 -e "${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/RecvStream2_mono.sh cpr7004 0 34004 hogehoge1000; sleep 3000000;" &

#
# event builder on ROPC (usually automatically invoked by inetd)
#
#/usr/bin/xterm -fn 7x14 -geometry 102x10+0+342 -e ${BELLE2_LOCAL_DIR}/daq/eventbuilder/evb0/eb0 -n 1 cpr006 -D -b &
#/usr/bin/xterm -fn 7x14 -geometry 102x10+0+342 -e ${BELLE2_LOCAL_DIR}/daq/eventbuilder/evb0/eb0 -n 2 cpr006 cpr015 -D -b &


#
# basf2 program AFTER eb0(event builder 0) on a readout PC
#
#    print 'Usage : RecvStream1.py <Use NSM(Network Shared Memory)? yes=1/no=0> <port # of eb0> <NSM nodename>
${BELLE2_LOCAL_DIR}/daq/copper/daq_scripts/RecvStream1.sh 0 34007 hogehoge1000 1
