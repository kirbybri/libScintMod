echo "Programming the FEEs"
#dcbit=~/lastfw/4020047_prog_concentrator_top_4dff56f3.bit
#dcbit=~/lastfw/4020047_concentrator_top_revo_frame_f30fb80b.bit
dcbit=~/lastfw/concentrator_top_revo_frame9_ec6295315a4.bit

#scrodbit=~/lastfw/klmscint_top_558d94c7f83.bit
#scrodbit=~/lastfw/20180515_klm_scrod_37bb_trigMode2.bit
#scrodbit=~/lastfw/klmscint_top_f6002c75c2b.bit
#scrodbit=~/lastfw/20180601_klmscint_top_558d_fakeData.bit
#scrodbit=~/lastfw/klm_scrod_dummy_frame9_20180308_37bbd637bfa.bit
#scrodbit=~/lastfw/20180604_klm-scint_592a_fakeHits.bit
#scrodbit=~/lastfw/20180604_klm-scint_592a_singleHit.bit
#scrodbit=~/lastfw/20180607_klm-scint_592a_singleHit.bit
#scrodbit=~/lastfw/20180613_klmscint_top_592a_singleHit.bit
scrodbit=~/lastfw/180625_klmscint_simple_top_csp.bit
echo using: $dcbit and $scrodbit
ls -la $dcbit
ls -la $scrodbit

ttaddr -191 -c
ttaddr -191 -a

#s154 and s153 are connected to local jtag for debugging
#ttaddr -191 -j s117,s118,s156,s157,s158,s159,s051,s075,s092,s104,s150,s152,s160,s161
ttaddr -191 -j s117,s118
jtagft -191 -p0 chain
jtagft -191 -p0 program $scrodbit

sleep 1

#DC 10 is programmed via local jtag for debugging
#ttaddr -191 -j dc16,dc17,dc18,dc12,dc13,dc20,dc19
ttaddr -191 -j dc16
jtagft -191 -p0 chain
jtagft -191 -p0 program $dcbit

sleep 2

resetft -191

echo ALL KLM FEE PROG DONE!
