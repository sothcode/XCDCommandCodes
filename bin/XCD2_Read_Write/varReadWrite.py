# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:51:09 2024

@author: KMFin
"""

#!/usr/bin/python3
import os, os.path
import datetime
import getpass

filePath ='C:/Users/kfinnelli/Documents/GitHub/XCDCommandCodes/bin/XCD2_Read_Write'

fileName = "VariableDictionary.txt"
logName = "log.txt"


########################
def writeVar(varName = None, varValue = None, new = '0'):
    
    if varName is None:                 # Checks if any arguments were given. If not, gives argument info
        print(" \
     No arguments given. writeVar will assign the given variable and values to the VariableDictionary. writeVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String in quotes. \n \
     2) varValue - Mandatory, specifies the variable value. \n \
     3) new - Optional. If given as 'new', the given variable name and value will be added to VariableDictionary \n \
     ")
        return False
        
    else:
        
        #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
        #Checks current working directory
        if os.path.exists(filePath):
            os.chdir(filePath)
        else:
            print("Can't change the Current Working Directory")   
            return False
            
        #Reads in the file as a dictionary
        varDict = {}
        with open(fileName) as fOld:
            for line in fOld:
                (k, v) = line.split()
                varDict[(k)] = v
    
        datetimeNow = str(datetime.datetime.now())
        userName = str(getpass.getuser())
        
        # if varName in "list":             # Checks if list arg was given
        #     print("Variable List:")
        #     #print('%s %s\n' % (varDict, varDict[]))
        #     print(varDict)                          # Prints the list of variables with the list argument. Could be nicer.
        if varName in varDict.keys():             # Checks if varName is a key
            if varValue is None:                    # Checks that a variable value was given
                print("No variable value given. To see a current list of variables and their values, use listVar()")
                return False
            else:
                with open(logName, "a") as f:     # Logs the change to the log for a change
                    f.write('%s %s %s %s \n' % (varName, varValue, datetimeNow, userName ))
                varDict[varName] = varValue         # Assigns the given varValue to the key varName
                if new in "new":
                    print("Variable name already exists. Existing variable will be changed.")
                print("Variable " +str(varName) + " changed to = " + str(varValue) + " at " + datetimeNow + " by " + userName)
                
        else:                                       # If varName not in deictionary, checks for "new" command"
            if new in 'new':                        # If "new" command is there, appends varName and varValue to the dict
                with open(logName, "a") as f:     # Logs the change to the log for an addition
                    f.write('%s %s %s %s \n' % (varName, varValue, datetimeNow, userName  ))
                print("Added " + str(varName) + " = " + str(varValue) + " to dictionary at " + datetimeNow + " by " + userName)
                varDict[varName] = varValue 
            else:                                   # If "new" command is absent, returns error message
                print("Variable name " + str(varName) +" not recongized. If you want to add a new variable to the list, add 'new' as a third argument. For a list of variables, use listVar()")
                return False
        #print(varDict)
        
        with open(fileName, 'w') as fileNew:            # Writes over the original with the new values
            for key, value in varDict.items():  
                fileNew.write('%s %s\n' % (key, value))
                
        return True
            

def readVar(varName = None):
    if varName is None:
        print(" \
     No arguments given. readVar will find the value for a given variable. readVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String. \n \
     ")
        return False
    else:
        #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
        #Checks current working directory
        if os.path.exists(filePath):
            os.chdir(filePath)
        else:
            print("Can't change the Current Working Directory") 
            return False
            
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
            return True, float(varDict.get(varName))         # Returns varValue as a float
            
        else:
            print("Variable name not found")
            return(False)
        
        
def listVar():
        
        #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
        #Checks current working directory
        if os.path.exists(filePath):
            os.chdir(filePath)
        else:
            print("Can't change the Current Working Directory")   
            return False
            
        #Reads in the file as a dictionary
        varDict = {}
        with open(fileName) as fOld:
            for line in fOld:
                (k, v) = line.split()
                varDict[(k)] = v

        print("Variable List:")
        print(varDict)  
        return True
