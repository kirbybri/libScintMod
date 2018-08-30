link = "-a"
echo "###########################################"
echo "Loading FEE on HSLB $link RunControl"
echo "###########################################"
echo "Reading: HSLB $link fee32 0x38 response :" 
echo "the value of FEE32 reg 0x38 is changed to 0xa then 0x960-check"
echo "###########################################"
reghs $link fee32 0x38
reghs $link fee32 0x38 10 #test value to see if reg 0x38 changes
reghs $link fee32 0x38
reghs $link fee32 0x38 2400 #this is the value which shows actual number of RCL
reghs $link fee32 0x38
echo "###########################################"
echo "Sending RCL to FEE on HSLB $1"
echo "###########################################"
reghs $link stream rcBF3.dat
echo "wait to make sure all pedestals are calculated and "
echo "if you look at HV current, you should see a momentary dip"
sleep 2
echo "Done sending RCL data to HSLB $link"
echo "###########################################"

#Data Concentrator Registers 
#############################################
#echo "Write RPC window values 0x300 0x14C 0x90 0x010, and write to 0x300 to 0x34 ..."

#reghs -b fee32 0x30 0x300
#reghs -b fee32 0x31 0x14C
#reghs -b fee32 0x32 0x90
#reghs -b fee32 0x33 0x10
#reghs -b fee32 0x34 0x300

#echo "window coarse start"
#reghs -b fee32 0x30
#echo "window coarse stop"
#reghs -b fee32 0x31
#echo "window fine start"
#reghs -b fee32 0x32
#echo "window fine stop"
#reghs -b fee32 0x33
