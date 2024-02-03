#!/usr/bin/python3


# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:51:09 2024

@author: KMFin
"""

#!/usr/bin/python3
import os, os.path
import datetime
import getpass
import time

########################
sleeptime=0.05
debug=True

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

def is_string(obj):
    return isinstance(obj, str)

def is_locked_for_write(filename):
    #returns true if there is a read or a write lock.
    #ie, if someone is reading or writing right now, we cannot write.
    if os.path.exists("%s.readlock%s"%(filename,0)):
        return True
    if os.path.exists("%s.writelock"%(filename)):
        return True
    
    return False
    
def is_locked_for_read(filename):
    #returns true if there is a write lock.
    #ie, we can read if others are reading, but we cannot read if others are writing
    if os.path.exists("%s.writelock"%(filename)):
        return True
    return False

def wait_and_writelock(filename):
    waittime=0
    while is_locked_for_write(filename):
        time.sleep(sleeptime)
        waittime+=1
        if (waittime % 100 == 0):
            print("kfdb waiting to write to %s.  (sleeps=%s*%s)"%(filename,waittime,sleeptime))
    add_writelock(filename)
    return True

def wait_and_readlock(filename):
    waittime=0
    while is_locked_for_read(filename):
        time.sleep(sleeptime)
        waittime+=1
        if (waittime % 100 == 0):
            print("kfdb waiting to read from %s.  (sleeps=%s*%s)"%(filename,waittime,sleeptime))
    add_readlock(filename)
    return True

def add_writelock(filename):
    with open("%s.writelock"%(filename), 'w'): #create the (only) write lock 
        pass
    if debug:
        print("added writelock to %s"%(filename))
    return

def add_readlock(filename):
    locknum=0
    while os.path.exists("%s.readlock%s"%(filename,locknum)):
        locknum+=1
    with open("%s.readlock%s"%(filename,locknum), 'w'): #create the first read lock that doesn't exist
        pass
    if debug:
        print("added readlock %s to %s"%(locknum, filename))
    return

def remove_writelock(filename):
    lockfilename="%s.writelock"%filename
    if filename=='/':
        print("remove('%s')?! This would have reformatted the disk!  Thankfully we caught it."%filename)
        sys.exit()
    if not (".kfdb" in filename and "writelock" in lockfilename):
        print("trying to remove('%s') by deleting %s .  This does not look like a valid db to unlock.  aborting.  You will have to deal with lockfiles manually before retrying."%(filename,lockfilename))
        sys.exit()
    if debug:
        print("removing writelock from %s"%(filename))        
    os.remove(lockfilename)
    return
    
def remove_readlock(filename):
    if filename=='/':
        print("remove('%s')?! This would have reformatted the disk!  Thankfully we caught it."%filename)
        sys.exit()
    locknum=0
    while os.path.exists("%s.readlock%s"%(filename,locknum)):
        locknum+=1
    lockfilename="%s.readlock%s"%(filename,locknum-1)
    if not (".kfdb" in filename and "readlock" in lockfilename):
        print("trying to remove('%s') by deleting %s .  This does not look like a valid db to unlock.  aborting.  You will have to deal with lockfiles manually before retrying."%(filename,lockfilename))
        sys.exit()
    if debug:
        print("removing readlock %s from %s"%(locknum-1, filename))
    os.remove(lockfilename)
    return

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
    wait_and_readlock(fileName)
    with open(fileName) as f:
        for line in f:
            lineContents=line.split()
            (k, v) = lineContents[0],lineContents[1:]
            varDict[(k)] = convert_to_numbers(v) #element by element, convert the values in v to numbers if possible.  leave them as strings otherwise
    remove_readlock(fileName)
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
        return False

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

    #go through cases where nothing needs to be done:
    if varName in varDict.keys():             # Checks if varName is a key
        if writeNew=='new':
            print("Variable %s was declared as 'new', but it already exists.  Aborting. Existing value will not be changed." % varName)
            return False
        if (varValue==varDict[varName]):
            print("Variable " +str(varName) + " requested to be changed to = " + str(varValue) + " but is already that value.  Nothing changes.  No log entry will be added.")
            return True
    else: #varName is not in the dict yet
        if writeNew!='new':# If "new" command is absent, returns error message
            print("Variable name " + str(varName) +" not recognized. If you want to add a new variable to the list, add 'new' as a third argument. For a list of variables, use listVar()")
            return False           
        
 
    wait_and_writelock(fileName)
    wait_and_writelock(logName)
    #go through cases where we must write something:
    if varName in varDict.keys():             # Checks if varName is a key
        #so we have a change we intend to apply, now:
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

        
    #overwrite the original db with the new list
    with open(fileName, 'w') as fileNew:            # Writes over the original with the new values
        for key, value in varDict.items():  
            fileNew.write("%s" % (key))
            if  is_iterable(value) and (not is_string(value)): #if iterable, but not a string, write out each element (strings are also iterable)
                for item in value:
                    fileNew.write(" %s" % (item))
            else: #if a string, or otherwise not iterable, write it out as a single block
                fileNew.write(" %s" % (value))
            fileNew.write("\n")
    remove_writelock(logName)
    remove_writelock(fileName)
    return True
            

def readVar(fileName='junk_db.kfdb', varName = None):
    #return the contents of that element if it exists.
    #return pattern is (bool Success),(if successful, value.  this is an array if the value has multiple entries, a single variable otherwise)
    if varName is None:
        print(" \
     No arguments given. readVar will find the value for a given variable. readVar parameters are: \n \
     1) varName - Mandatory, specifies the variable name. String. \n \
     ")
        return False,0

    #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
    
   #check that file exists before opening
    if not os.path.exists(fileName):
        print("Can't load kfdb '",fileName,"'.  File does not exist.")
        return False,0

    #the log of changes to this file is that + .log
    logName=f"{fileName}.log"

    
    #Reads in the file as a dictionary
    varDict = {}
    varDict=loadDict(fileName) #this is locking on its own.

    #print(varDict)
    #Checks if varName is a key
    if varName in varDict.keys():
        #print(varDict.get(varName))
        value=varDict.get(varName)
        if len(value)==1:
            return True, value[0] #Returns the first element of the array directly, if there is only one element
        return True,value        # Returns varValue, which is an array
        
    else:
        print("kfdb: variable name '%s' not found in '%s'"%(varName,fileName))
        return False,0
        
        
def listVar(fileName='junk_db.kfdb'):
        
    #print("Current Working Directory " , os.getcwd())               # Checks current working directory and moves to the correct one
        
    #check that file exists before opening
    if not os.path.exists(fileName):
        print("Can't load kfdb '",fileName,"'.  File does not exist.")
        return False

    #the log of changes to this file is that + .log
    logName=f"{fileName}.log"
            
    #Reads in the file as a dictionary
    varDict = {}
    varDict=loadDict(fileName) #this is locking on its own.

    print("Variable List:")
    print(varDict)  
    return True



#to talk to it from the command line
if __name__ == "__main__":
    #check args
    if len(sys.argv)==2:
        #assume first arg is a filename, and try to open it to list:
        print("listVar returned",listVar(sys.argv[1]))
    elif len(sys.argv)==3:
        #assume first arg is a filename, second is a key name.  report back that key value
        readVar(sys.argv[1], sys.argv[2])
        print("readVar returned",readVar(sys.argv[1], sys.argv[2]))
    elif len(sys.argv)==4:
        #assume it's filename,key,value.  try to set that value.
        print("writeVar returned",readVar(sys.argv[1], sys.argv[2],sys.argv[3]))
    elif len(sys.argv)==5:
        #assume it's filename,key,value, newFlag.  try to set that value.
        print("writeVar with extra flag returned",readVar(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4]))
    else:
        print("kfdb NOT EXECUTED. Wrong number of arguments.  Requires 1,2,3, or 4 args")
        sys.exit()
