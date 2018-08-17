echo "###########################################"
echo "Loading FEE on HSLB $1 RunControl"
echo "###########################################"
echo "Reading: HSLB $1 fee32 0x38 response :" 
echo "the value of FEE32 reg 0x38 is changed to 0xa then 0x960-check"
echo "###########################################"
reghs $1 fee32 0x38
reghs $1 fee32 0x38 10 #test value to see if reg 0x38 changes
reghs $1 fee32 0x38
reghs $1 fee32 0x38 2400 #this is the value which shows actual number of RCL
reghs $1 fee32 0x38
echo "###########################################"
echo "Sending RCL to FEE on HSLB $1"
echo "###########################################"
reghs $1 stream $2
echo "wait to make sure all pedestals are calculated and "
echo "if you look at HV current, you should see a momentary dip"
sleep 2
echo "Done sending RCL data to HSLB $1"
echo "###########################################"



