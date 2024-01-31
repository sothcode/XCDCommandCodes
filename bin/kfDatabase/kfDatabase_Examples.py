# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:00:55 2024

@author: kfinnelli
"""

#varReadWrite.py exmaples file

from kfDatabase import writeVar , readVar , listVar

#Before running, make sure filePath, fileName, and logName variables in varReadWrite are correct
# filePath : Path of Variable Dictionary and log file
# fileName : Name of dictionary, currently VariableDictionary.txt
# logName  : Name of log file, currently log.txt 

# VariableDictionay.txt is a text file that contains the variable names and their values, separated by a space.

# log.txt logs all the changes made to VariableDicitionary. Any time a variable is succesfully changed or added
# to VariableDicitionary, the variable name, NEW value, date & time, and user name are written to logt.txt
    #Ex: using writeVar("newHome", 6.3) to change the value of "newHome" from 5.8 to 6.3 will log
        # newHome 6.3 2024-01-31 11:21:37.718962 kfinnelli

# All variables should be given in quotes, and not separated by spaces
    #Ex: writeVar("variableName", 99) NOT writeVar( variable name, 99)

#-------------------

print("\n####To get a list of the current VariableDictionary: listVar(\"dbName\")")
listVar("VariableDictionary.txt")
#Prints a list of the values and returns True

#-------------------

print("\n####To read a value from VariableDictionary: readVar(\"dbName\",\"variableName\")")
readVar("VariableDictionary.txt","one")
#Prints the value of the variable given, and returns True and the value 

print("\n####If the variable name is not in the list, gives an error message and returns False")
readVar("VariableDictionary.txt","wrongName")

print("\n####If no arguments are given, argument info is printed and returns False")
readVar("VariableDictionary.txt")

#--------------------

print("\n####To write a value to a variable: writeVar(\"dbName\",\"variableName\", variable value)")
writeVar("VariableDictionary.txt","one", 12)
#Changes the value of variable "one" to 12. Reports the change, changes the value in VariableDictionary, logs the change in log.txt, and returns True

print("\n####If only a variable name is given and not a value, error message is printed and returns False")
writeVar("VariableDictionary.txt","one")

print("\n####If the variable given is not recognized, error message is printed and returns False")
writeVar("VariableDictionary.txt","wrongName", 99)

print("\n####If you give an array as the value name, that works fine too.")
writeVar("VariableDictionary.txt","array", [99,45])


print("\n####To add a new variable name and value to the dictionary, add \"new\" as a 3rd argument and returns True")
writeVar("VariableDictionary.txt","newVariable", 77, "new")
print("\n####If \"new\" is added but the variable name is already in the list, a new variable will NOT be added; the existing one will be updated")
writeVar("VariableDictionary.txt","existingVariable", 66, "new")

print("\n####If no arguments given, argument info is printed and returns False")
writeVar()
