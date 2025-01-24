#Utility for log-reading
import os
from datetime import datetime
import re
import pandas as pd
import matplotlib.pyplot as plt

drive = r"C:\Users\student\Visualisering Scape"

logfile = "Data/run_scape.log"

os.chdir(drive)

#build dataframe for logdata

def convertlog():
    loglines =[]
    MyColumns=['Cycle','Task','Date','Start','Stop']
    logdata = pd.DataFrame(columns=MyColumns)
    with open (logfile, 'r', encoding='cp437') as log:
        loglines = log.readlines()
        #cycle = 0
        #for line in loglines:
        cycledelimiter = ['LogCounter','RESET_STATS', 'ScapeDetailedTimingInfo']
            #cycle through lines
        for i in range(0, len(loglines)):
            timeformat = "%H:%M:%S"
            timeformat_milli = "%H:%M:%S.%f"
            line = loglines[i]
            #Identify start and stop of cycles
            if any(delimiter in line for delimiter in cycledelimiter):
                #Identify cyclestartevent
                if line.find(cycledelimiter[0]) != -1:
                    #split the text into list by whitespaces
                    logstart = re.split('\s',line)
                    #filter away empty listelements to remove variance in listlength
                    logstart = list(filter(None, logstart))
                #identify individual subprocess
                if line.find(cycledelimiter[2]) != -1:
                    print(line)
                    process_text = re.search(r'for task "([^"]+)"', line)
                    #print(f"process_1: {process_1}")
                    process = process_text.group(1)
                    #print(f"process_2: {process}")
                    #split the text into list by whitespaces
                    #process = re.split('\s',line)
                    #print(process)
                    #filter away empty listelements to remove variance in listlength
                    #process = list(filter(None, process))
                    #process = process[-1]
                    print(f'Trimmed process is: {process}')

                    #trim process to only contain alphanumeric characters
                    process = re.sub(r'\W+', '', process)

                    #Get the processstart from next line and replace - with :
                    start = re.split('\s',loglines[i+1])
                    ls = len(start)
                    start = list(filter(None, start))
                    start = start[-1].replace('-', ':')
                    start = datetime.strptime(start,timeformat_milli)

                    #Get the processstop from secondnext line and replace - with :
                    stop = re.split('\s',loglines[i+2])
                    stop = list(filter(None, stop))
                    stop = stop[-1].replace('-', ':')
                    stop = datetime.strptime(stop,timeformat_milli)
                    #start = start.replace('-',':')
                    logdic = {0:[logstart[2],process,logstart[10],start,stop]}

                    processlog = pd.DataFrame().from_dict(logdic,
                                                    orient='index',
                                                    columns=MyColumns)
                    #Concatenate latest cycle into dataframe
                    logdata = pd.concat([logdata,processlog],
                                        axis=0,
                                        ignore_index=True)

                                 

                #Identify cyclestopevent
                if line.find(cycledelimiter[1]) != -1:
                    logend = re.split('\s',line)
                    logend = list(filter(None, logend))
                    #collect dictionary, and convert it to dataframe for later concatenation
                    start = datetime.strptime(logstart[7],timeformat)
                    stop = datetime.strptime(logend[8],timeformat)
                    logdic = {0:[logstart[2],'FullCycle',logstart[10],start,stop]}
                    #logseries = pd.Series(logdic)
                    #create dict of this cycle
                    cycle = pd.DataFrame().from_dict(logdic,
                                                    orient='index',
                                                    columns=MyColumns)
                    #Concatenate latest cycle into dataframe
                    logdata = pd.concat([logdata,cycle],
                                        axis=0,
                                        ignore_index=True)
            #print(i)
    
                #cycle += 1
                print(round(i/(len(loglines)),3))
        #print(cycle)
        return logdata
    
logdata = convertlog()

logdata.to_csv('Data/run_scape_logdata_df.csv')