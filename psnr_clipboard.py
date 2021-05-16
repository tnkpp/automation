import pyperclip
import re
from collections import namedtuple

ResultData = namedtuple("ResultData", "file bitrate result")

filenameRegex = re.compile(r'Input file#1.*\\(\w+)_(\d+(k|M))bps\.yuv')
resultRegex = re.compile(r'Parsed PSNR.*Y:(\d+\.\d+)')

lines = pyperclip.paste().split('\n')
bitrates = []
files = []
results = []

for l in lines:
    fileScan = filenameRegex.search(l)
    if fileScan != None:
        # group(1) : prefix
        # group(2) : bitrate
        currentFile = fileScan.group(1)
        currentBitrate = fileScan.group(2)
        continue
    resultScan = resultRegex.search(l)
    if resultScan != None:
        # group(1) : x.xxxx
        #print(currentFile)
        #print(currentBitrate)
        #print(resultScan.group(1))
        files.append(currentFile)
        bitrates.append(currentBitrate)
        m = ResultData(currentFile, currentBitrate, resultScan.group(1))
        results.append(m)

bitrates = list(set(bitrates))
bitrates.sort()
files = list(set(files))
files.sort()

#print(files)
#print(bitrates)
#print(results)
print(bitrates)
for f in files:
    #print(f)
    #print(bitrates)
    resultRow = []
    for b in bitrates:
        found = False
        for r in results:
            if (r.file==f and r.bitrate==b):
                if (found==True):
                    print("#### DUPLICATED data!")
                found = True
                #print('### ', f, b, r.result)
                resultRow.append(r.result)
        if (found==False):
            resultRow.append('NULL')
            #print('### ', f, b, 'NULL')
    resultRow.append(f)
    print(resultRow)

