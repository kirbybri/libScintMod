import struct
import sys 
import string
import os

class PROCESS_BINARY(object):

    #__INIT__#
    def __init__(self,inputFileName):
        self.inputFileName = inputFileName
        self.inputFile = None
        self.fileContent = None
        self.fileArray = []

        #constants

        print("GET DATA")
        self.getData()
        #self.dumpData()
        self.dumpRegs()

    def getData(self):
        #check if data exists
        isFile = os.path.isfile(self.inputFileName) 
        if isFile == False:
            print("Could not find input file, quitting")
            return
        #put binary data into memory
        self.input_file = open(self.inputFileName,'rb')
        self.fileContent = self.input_file.read()     
        print("Read input file of length (bytes): ", len(self.fileContent))

        #loop over input file X bytes at a time, load into array
        for pos in range(0, len(self.fileContent), 2):
            #line = struct.unpack('I', self.fileContent[pos:pos+4]) #normal ordering            
            #line = struct.unpack('!I', self.fileContent[pos:pos+4]) #network byte ordering
            #line = struct.unpack('Q', self.fileContent[pos:pos+8]) #normal ordering
            line = struct.unpack('H', self.fileContent[pos:pos+2]) #normal ordering                        
            if len(line) != 1:
                print("getData: error parsing input file, quitting")
                return
            data = line[0]
            self.fileArray.append(data)        

    def dumpData(self):
        if len(self.fileArray) == None:
            return

        #loop over input file 4 bytes at a time, look for packet header words
        for lineNum in range(0,len(self.fileArray),1):
            line = self.fileArray[lineNum]
            print(lineNum,"\t",hex(line))

            if lineNum > 100 :
                break

    def dumpRegs(self):
        if len(self.fileArray) == None:
            return

        #loop over input file 4 bytes at a time, look for packet header words
        for lineNum in range(0,len(self.fileArray),3):
            line0 = self.fileArray[lineNum]
            line1 = self.fileArray[lineNum+1]
            line2 = self.fileArray[lineNum+2]
            #print(lineNum,"\t",hex(line0),"\t",hex(line1),"\t",hex(line2))

            lane = (line0 & 0xF000 ) >> 12
            reg = (line1 & 0x000F << 4) + ( (line1 & 0xF000) >> 12 )
            data = ((line1 & 0x0F00) << 4 ) + ((line2 & 0x00F0) << 4 ) + ((line2 & 0x000F) << 4 ) + ((line2 & 0xF000) >> 12 )

            allLine = line2 + (line1 << 16) + (line0 << 32)

            print(hex(allLine),"\tLane ",hex(lane),"\tReg ",reg,"\tData ",hex(data))

            #if lineNum > 100 :
            #    break


def main():

    if len(sys.argv) != 2 :
        print("processBinary: need to provide input file name")
        return
    fileName = sys.argv[1]
    processBinary = PROCESS_BINARY(fileName)

if __name__ == '__main__':
    main()
