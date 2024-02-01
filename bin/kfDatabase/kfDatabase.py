# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:51:09 2024

@author: KMFin
"""

#!/usr/bin/python3
import os, os.path
import datetime
import getpass

########################

def is_number(s):
    if is_iterable(s):
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False    

def convert_to_numbers(arr):
    #converts an array of strings to an array of mixed strings and floats
    result = []

    for s in arr:
        # Try to convert the string to a number
        try:
            number = float(s)
            result.append(number)
        except ValueError:
            # If conversion fails, keep the original string
            result.append(s)

    return result

def loadDict(fileName='junk_db.kfdb'):
    #loads and returns the dictionary
    varDict = {}
    with open(fileName) as f:
        for line in f:
            lineContents=line.split()
            (k, v) = lineContents[0],lineContents[1:]
            varDict[(k)] = convert_to_numbers(v) #element by element, convert the values in v to numbers if possible.  leave them as strings otherwise
    return varDict
    
def writeVar(fileName='junk_db.kfdb', varName = None, varValue = None, writeNew = '0'):

    #stop if the varName of varValue are not filled in.
    if (varName is None) or (varValue is None):                 # Checks if any arguments were given. If not, gives argument info
        print("No arguments given. writeVar will assign the given variable and values to the VariableDictionary. writeVar parameters are: \n \
                1) varName - Mandatory, specifies the variable name. String in quotes. \n \
                2) varValue - Mandatory, specifies the variable value. \n \
                3) new - Optional. If given as 'new', the given variable name and value will be added to VariableDictionary")
        return False

    #check that file exists before opening
    if not os.path.exists(fileName):
        print("Can't load kfdb '",fileName,"'.  File does not exist.")
        return False;

    #the log of changes to this file is that + .log
    logName=f"{fileName}.log"
        
    #Reads in the file as a dictionary
    varDict = {}
    varDict=loadDict(fileName)
 

    datetimeNow = str(datetime.datetime.now())
    userName = str(getpass.getuser())

    #massage the input variable (internally, our key value pairs are key,array_of_vals):
    #make it an array if it isn't:
    if not is_iterable(varValue):
        varValue=[varValue]
    #make the values in the array numbers if we can:
    convert_to_numbers(varValue)

    #search for the variable in the db.  Try to create it if 'new', try to update it if not 'new'.  Fail otherwise.

    if varName in varDict.keys():             # Checks if varName is a key
        print("testcomparison:",varValue, varDict[varName])
        if writeNew=='new':
            print("Variable %s was declared as 'new', but it already exists.  Aborting. Existing value will not be changed." % varName)
            return False
        if (varValue==varDict[varName]):
            print("Variable " +str(varName) + " requested to be changed to = " + str(varValue) + " but is already that value.  Nothing changes.  No log entry will be added.")
            return True
        with open(logName, "a") as f:     # Logs the change to the log for a change
            f.write('%s %s %s %s \n' % (varName, varValue, datetimeNow, userName ))
        varDict[varName] = varValue         # Assigns the given varValue to the key varName
        print("Variable " +str(varName) + " changed to = " + str(varValue) + " at " + datetimeNow + " by " + userName)            
    else:                                       # If varName not in dictionary, checks for "new" command"
        if writeNew=='new':                        # If "new" command is there, appends varName and varValue to the dict
            with open(logName, "a") as f:     # Logs the change to the log for an addition
                f.write('%s %s %s %s \n' % (varName, varValue, datetimeNow, userName  ))
            print("Added " + str(varName) + " = " + str(varValue) + " to dictionary at " + datetimeNow + " by " + userName)
            varDict[varName] = varValue
        else:                                   # If "new" command is absent, returns error message
            print("Variable name " + str(varName) +" not recongized. If you want to add a new variable to the list, add 'new' as a third argument. For a list of variables, use listVar()")
            return False

        
    #overwrite the original db with the new list
    with open(fileName, 'w') as fileNew:            # Writes over the original with the new values
        for key, value in varDict.items():  
            fileNew.write("%s" % (key))
            if is_iterable(value):
                for item in value:
                    fileNew.write(" %s" % (item))
            else:
                fileNew.write(" %s" % (value))
            fileNew.write("\n")
                
    return True
            

def readVar(fileName='junk_db.kfdb', varName = None):
    #return the contents of that element if it exists.
    #return pattern is (bool Success),(if successful, value.  this is an array if the value has multiple entries, a single variable otherwise)
    if varName is None:
        print(" \
     No arguments given. readVar will find the value for a given variable. readVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String. \n \
     ")
        return False

    #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
    
   #check that file exists before opening
    if not os.path.exists(fileName):
        print("Can't load kfdb '",fileName,"'.  File does not exist.")
        return False;

    #the log of changes to this file is that + .log
    logName=f"{fileName}.log"

    
    #Reads in the file as a dictionary
    varDict = {}
    varDict=loadDict(fileName)

    #print(varDict)
    #Checks if varName is a key
    if varName in varDict.keys():
        #print(varDict.get(varName))
        value=varDict.get(varName)
        if len(value)==1:
            return True, value[0] #Returns the first element of the array directly, if there is only one element
        return True,value        # Returns varValue, which is an array
        
    else:
        print("Variable name not found")
        return False 
        
        
def listVar(fileName='junk_db.kfdb'):
        
    #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
    #check that file exists before opening
    if not os.path.exists(fileName):
        print("Can't load kfdb '",fileName,"'.  File does not exist.")
        return False;

    #the log of changes to this file is that + .log
    logName=f"{fileName}.log"
            
    #Reads in the file as a dictionary
    varDict = {}
    varDict=loadDict(fileName)

    print("Variable List:")
    print(varDict)  
    return True
