#!/bin/sh

# DC registers

# every register is described by five values: name, number, base, column width, and value width, separated by colons
# first two are required, others are optional
# base is: b for binary, d for decimal, h for hexidecimal
# if no base, column width or value width are given,
# register value is printed as decimal, column is 12 simbols wide, with natural value width

regs=("HSL_CHAN_UP:0x614:b:13:8"  "FIFO_FLAGS1:0x630:b:18:16" "TRG_PKTSZ1:0x631"   "DAQ_PKTSZ1:0x632"   "STS_PKTSZ1:0x633"
      "FIFO_FLAGS2:0x634:b:18:16" "TRG_PKTSZ2:0x635"          "DAQ_PKTSZ2:0x636"   "STS_PKTSZ2:0x637"   "LKBK_STRT_C:0x30"
      "LKBK_STOP_C:0x31"          "LKBK_STRT_F:0x32"          "LKBK_STOP_F:0x33"   
# line 2
      "MISSED_TRG:0x06A0"         "RPC_FLAGS:0x06A1:b:18:16"
      "SCNT_FLAGS:0x06A2:b:18:16" "RPC_TRGTAG:0x06A3"         "SCNT_TRGTAG:0x06A4" "SCNT_TTERR:0x06A5"  "RPC_DELAY:0x06A6"
      "RPC_EVTAG:0x06A7"          "SCNT_EVTAG:0x06A8"         "EVNT_RDCNT1:0x06A9" "EVNT_RDCNT2:0x06AA" "EVNT_WRCNT1:0x06AB"
      "EVNT_WRCNT2:0x06AC"        "EVNT_WDCNT:0x06AD"
)

# where to split registers between two lines
nSplit=13


parse_registers() {
	local IFS=':'

	for ((i=0; i<${nRegs}; ++i))
	do
		local regTmp=( ${regs[i]} )

		regName[i]=${regTmp[0]}
		regNumber[i]=${regTmp[1]}
		regBase[i]=${regTmp[2]}
		regColumnWidth[i]=${regTmp[3]}
		regValueWidth[i]=${regTmp[4]}
	done
}

remote_readout() {
	# argument to reghs command
	reghsArg=""
	for i in ${regNumber[@]}
	do
		reghsArg=${reghsArg}" fee32 ${i} -"
	done

	for link in "-a" "-b" "-c" "-d"
	do
		output=`reghs ${link} ${reghsArg} 2>/dev/null | grep -E -o '0{4}[0-9a-f]{4}' | tr '[:lower:]' '[:upper:]'`

		# take care of missing HSLB
		if [ -n "${output}" ]
		then
			echo ${output}
		else
			for ((i=0; i<${nRegs}; ++i))
			do
				echo -n " -1"
			done
			echo
		fi
	done
}

print_headers() {
	if [ ! ${1} ]
	then
		echo "print_headers() needs an argument"
		return 1;
	fi

	local minCol=0
	local maxCol=0
	if [[ ${1} == 1 ]]
	then
		minCol=0
		maxCol=${nSplit}
	else
		minCol=${nSplit}
		maxCol=${nRegs}
	fi

	if [ ${maxCol} -gt ${nRegs} ]
	then
		maxCol=${nRegs}
	fi

	printf "%10s" "link"

	for ((i=${minCol}; i<${maxCol}; ++i))
	do
		local columnWidth=12
		if [[ "a${regColumnWidth[i]}" != "a" ]]
		then
			columnWidth=${regColumnWidth[i]}
		fi
		printf "%*s" ${columnWidth} ${regName[i]}
	done
	echo

	return 0;
}

print_values() {
	if [ ! ${1} ]
	then
		echo "print_values() needs an argument"
		return 1;
	fi

	if [[ ${1} == 1 ]]
	then
		minCol=0
		maxCol=${nSplit}
	else
		minCol=${nSplit}
		maxCol=${nRegs}
	fi

	if [ ${maxCol} -gt ${nRegs} ]
	then
		maxCol=${nRegs}
	fi

	# padding zeros
	local pad=$(printf '%0.1s' "0"{1..20})
	local padLength=${#pad}

	local i=0
	for copper in "cpr7001" "cpr7002" "cpr7003" "cpr7004"
	do
		local j=0
		for link in "-a" "-b" "-c" "-d"
		do
			printf "%10s" "${copper} ${link}"

		#	for ((k=0; k<${nRegs}; ++k))
			for ((k=${minCol}; k<${maxCol}; ++k))
			do
				value=${regValues[i*4*nRegs + j*nRegs + k + 1]}

				local base=10
				local columnWidth=12
				local valueWidth=0
				if [[ "a${regBase[k]}" == "ab" ]]
				then
					base=2
				elif [[ "a${regBase[k]}" == "ah" ]]
				then
					base=16
				else
					base=10
				fi
				if [[ "a${regColumnWidth[k]}" != "a" ]]
				then
					columnWidth=${regColumnWidth[k]}
				fi
				if [[ "a${regValueWidth[k]}" != "a" ]]
				then
					valueWidth=${regValueWidth[k]}
				fi
				if [ "${valueWidth}" -gt "${columnWidth}" ]
				then
					columnWidth=$((valueWidth+2))
				fi

				if [[ ${value} == "-1" ]]
				then
					printf "%*s" ${columnWidth} ${value}
				else
					local convValue=`echo "obase=${base}; ibase=16; ${value}" | bc`

					if [[ ${valueWidth} == 0 ]]
					then
						printf "%*s" ${columnWidth} ${convValue}
					else
						local len=${#convValue}
						local zeros=$((valueWidth-len))
						local blanks=$((columnWidth-valueWidth))
						printf "%*s" ${blanks} " "
						printf "%*.*s%s" 0 ${zeros} ${pad} ${convValue}
					fi
				fi
			done
			echo
			j=$((j+1))
		done
		echo
		i=$((i+1))
	done 
}

fill_logfile() {
	# log file
	if [ ${1} ]
	then
		logDir=`dirname ${1}`
		[[ ${logDir} == "." ]] && logDir=${PWD}
		logFile="${logDir}/"`basename ${1}`
		touch ${logFile}
	else
		return 0
	fi

	# column headers
	if [[ ! -s ${logFile} ]]
	then
		echo -n "#" >> ${logFile}
		for ((i=0; i<${nRegs}; ++i))
		do
			echo -n " ${regName[i]}"
		done
	fi

	# values
	echo "${output}" >> ${logFile}
}



# resisters
nRegs=${#regs[*]}

declare -a regName
declare -a regNumber
declare -a regBase
declare -a regColumnWidth
declare -a regValueWidth

parse_registers

if [[ ! ${HOSTNAME} =~ cpr700[1-4] ]]
then
	# this part executes on klm01

	# full script name
	script=`basename ${0}`
	scrDir=`dirname ${0}`
	[[ ${scrDir} == "." ]] && scrDir=${PWD}

	# start with date
	output=`date "+%s"`

	# read registers
	for i in 1 2 3 4
	do
		cprOut=`ssh cpr700${i} ${scrDir}/${script} 2>/dev/null`

		# take care of missing COPPERs
		if [ -z "${cprOut}" ]
		then
			for ((j=0; j<4; ++j))
			do
				for ((k=0; k<${nRegs}; ++k))
				do
					cprOut=${cprOut}" -1"
				done
			done
		fi
		output="${output} ${cprOut}"
	done

	regValues=( ${output} )

	# output to screen
	# start with date
	date

	# registers values are printed on the screen in two lines
	# line 1
	print_headers 1
	print_values 1

	# line 2
	print_headers 2
	print_values 2

	# output to log file
	fill_logfile ${1}
else
	# this part executes on a COPPER
	remote_readout
fi

