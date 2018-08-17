#Data Concentrator Registers 
#############################################
#echo "Write RPC window values 0x300 0x14C 0x90 0x010, and write to 0x300 to 0x34 ..."

reghs -b fee32 0x30 0x300
reghs -b fee32 0x31 0x14C
reghs -b fee32 0x32 0x90
reghs -b fee32 0x33 0x10
reghs -b fee32 0x34 0x300

echo "window coarse start"
reghs -b fee32 0x30
echo "window coarse stop"
reghs -b fee32 0x31
echo "window fine start"
reghs -b fee32 0x32
echo "window fine stop"
reghs -b fee32 0x33
