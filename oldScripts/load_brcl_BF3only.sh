rcl_file=$1
echo "CPR7001"
ssh -n -n -XY -l${USER} cpr7001 tesths -b
ssh -n -n -XY -l${USER} cpr7001 /home/group/b2klm/run/scripts/load_bklm_rcl_BFRb.sh $rcl_file

