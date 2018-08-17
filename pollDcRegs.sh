#!/bin/bash

echo "HSL_CHANNEL_UP : Aurora channel up, bit per link"
reghs -a fee32 1556

echo "FIFO_FLAGS1 : Trigger/DAQ FIFO flags and errors"
reghs -a fee32 1584

echo "DAQ_PKTSZ1 : DAQ packet size"
reghs -a fee32 1586

echo "FIFO_FLAGS2 : Trigger/DAQ FIFO flags and errors"
reghs -a fee32 1588

echo "DAQ_PKTSZ2 : DAQ packet size"
reghs -a fee32 1590

echo "MISSED_TRG : Missed trigger and event flags"
reghs -a fee32 1696

echo "SCINT_FLAGS : Scint. event builder FIFO flags"
reghs -a fee32 1698

echo "SCINT_TRGTAG : Current scint. trigger tag"
reghs -a fee32 1700

echo "SCINT_EVTAG : Buffered scint trigger tag"
reghs -a fee32 1704

echo "EVNT_RDCNT1	Event buffer 1 read count."
reghs -a fee32 1705

echo "EVNT_RDCNT2	Event buffer 2 read count."
reghs -a fee32 1706

echo "EVNT_WRCNT1	Event buffer 1 write count."
reghs -a fee32 1707

echo "EVNT_WRCNT2	Event buffer 2 write count."
reghs -a fee32 1708

echo "EVNT_WDCNT	Number of words in event."
reghs -a fee32 1709
