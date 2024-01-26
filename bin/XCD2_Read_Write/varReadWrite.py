# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:51:09 2024

@author: KMFin
"""

#!/usr/bin/python3
import os, os.path

filePath ='C:/Users/KMFin/OneDrive/Documents/Python/XCD2_Read_Write'
fileName = "VariableDictionary.txt"
logName = "log.txt"

########################
def writeVar(varName = None, varValue = None, new = '0'):
    
    if varName is None:                 # Checks if any arguments were given. If not, gives argument info
        print(" \
     No arguments given. writeVar will assign the given variable and values to the Test File. writeVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String in quotes. \n \
     2) varValue - Mandatory, specifies the variable value. \n \
     3) new - Optional. If given as 'new', the given variable name  \n \
     4) list - Optional. If 'list' is the only argument, outputs the current list of variables. \n \
     ")
        
    else:
        
        #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
        #Checks current working directory
        if os.path.exists(filePath):
            os.chdir(filePath)
        else:
            print("Can't change the Current Working Directory")    
            
        #Reads in the file as a dictionary
        varDict = {}
        with open(fileName) as fOld:
            for line in fOld:
                (k, v) = line.split()
                varDict[(k)] = v
    
        
        if varName in "list":             # Checks if list arg was given
            print("Variable List:")
            #print('%s %s\n' % (varDict, varDict[]))
            print(varDict)                          # Prints the list of variables with the list argument. Could be nicer.
        elif varName in varDict.keys():             # Checks if varName is a key
            if varValue is None:                    # Checks that a variable value was given
                print("No variable value given. To see a current list of variables, give 'list' as the only argument.")
            else:
                with open(logName, "a") as f:     # Logs the change to the log for a change
                    f.write('%s %s\n' % (varName, varValue))
                varDict[varName] = varValue         # Assigns the given varValue to the key varName
                print("Variable " +str(varName) + " changed to = " + str(varValue))
        else:                                       # If varName not in deictionary, checks for "new" command"
            if new in 'new':                        # If "new" command is there, appends varName and varValue to the dict
                with open("log.txt", "a") as f:     # Logs the change to the log for an addition
                    f.write('%s %s\n' % (varName, varValue))
                print("Added " + str(varName) + " : " + str(varValue) + " to dictionary")
                varDict[varName] = varValue 
            else:                                   # If "new" command is absent, returns error message
                print("Variable name not recongized. If you want to add a new variable to the list, add 'new' as a third argument. For a list of variables, add 'list' as the only argument.")
        
        #print(varDict)
        
        with open(fileName, 'w') as fileNew:            # Writes over the original with the new values

            for key, value in varDict.items():  
                fileNew.write('%s %s\n' % (key, value))
            

def readVar(varName = None):
    if varName is None:
        print(" \
     No arguments given. readVar will find the value for a given variable. readVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String. \n \
     ")
    else:
        #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
        #Checks current working directory
        if os.path.exists(filePath):
            os.chdir(filePath)
        else:
            print("Can't change the Current Working Directory")    
            
        #Reads in the file as a dictionary
        varDict = {}
        with open(fileName) as fOld:
            for line in fOld:
                (k, v) = line.split()
                varDict[(k)] = v
        #print(varDict)
        #Checks if varName is a key
        if varName in varDict.keys():
            print(varDict.get(varName))
            return float(varDict.get(varName))         # Returns varValue as an integer
        else:
            print("Variable name not found")
        
        
        
