# Py-Betty - ZdrytchX
#debugging cmd line python -m ipdb Py_Betty.py
#import tkinter
#import tkinter.messagebox
import time
import random
#import urllib.request
import requests #this?
#import http
#import io
import json
#import some kind of sound library
#import libao #pydub TODO

class settings: #more like a data struct
    def __init__(self):
        #states
        self.Redline        #max IAS
        self.MaxTemp        #max raw temperature
        self.MaxOilTemp     #max oil temperature
        self.MaxWaterTemp   #max water temperature
        self.MaxAoA         #max angle of attack
        self.GearUp         #GearUp threshold
        self.GearDn         #GearDown threshold
        self.MaxRPM         #Max RPM
        self.Mach           #Max Mach Speed
        self.Flaps1         #Max Speed Flaps Combat
        self.Flaps2         #Max Speed Flaps Take-off
        self.Flaps3         #Max Speed Flaps Landing
        self.GLoad          #Max G-Loading
        self.GLoad-Ve       #Minimum G-Loading
        self.MaxDescent     #Maximum Descent Rate
        self.MaxAoS         #Max Absolute Sideslip
        self.BingoFuel      #Bingo Fuel Threshold, fraction of Mfuel / Mfuel0
        self.BingoFuelRepeats #number of times to repeat warning
        self.Economy        #Efficiency of Prop for whatever reason
        #Indicators
        self.MaxBankAngle   #Max Banking Angle for Autopilot

class Navigation: #Mostly for autopilot integreation possibility
    def __init__(self):
        self.Compass        #Desired Compass Heading
        self.Distance       #Distance to travel
        self.Time           #Time to travel, interchangable with the above
        self.Altitude       #Cruising Altitude
        self.Bombdrops      #Number of times to smash the bomb drop button

class Program: #"blueprint"
    def __init__(ac, *args, **kwargs):
        ac.indicators = FetchIndicators()
        ac.state = FetchStatus()

        while True:
            if(ac.state["valid"] == True): #state valid likely means the same for indicators
                ACsettings = []
                LoadChanges(ac.indicators["type"], ACsettings)
                #main program checks here
                #print("Instance Indicator | type: " + ac.indicators["type"])
                #print("Instance Status | AoA:" + str(ac.state["AoA, deg"]))

            else:
                print("Aircraft Not Active")

            #At the end of main loop:
            time.sleep(0.125)

def PlayWarning(warningtype, indication):
    print(warningtype + " Warning: " str(indication))#Replace this with sound playback l8r

def CheckExceeded(warningtype, indication):
    print("CheckExceeded() | nothing here yet")

def FetchIndicators():
    indicators = []
    try:
        #with urllib.request.urlopen("http://localhost:8111/indicators") as url:
            #indicators = json.loads(url.read().decode())
        indicators = requests.get("http://localhost:8111/indicators", timeout=0.02).json()
        print("FetchIndicators() | Active: " + str(indicators["valid"]))#stored in dictionary type
        return indicators
    except:
        print("FetchIndicators() | nothing here yet")
        return indicators

def FetchStatus():
    state = []
    try:
        state = requests.get("http://localhost:8111/state", timeout=0.02).json()
        print("FetchStatus() | Active: " + str(state["valid"]))#stored in dictionary type
        return state
        #States are given in dict fomat "title, unit": value
    except:
        print("FetchStatus() | nothing here yet")
        return state

def SaveChanges(ACType, settings):
    continYN = inputSomething("Y to save\n> ")
    if continYN == "Y":
        file = open(ACType + ".json", "w")
        json.dump(settings, file)
        file.close()#let the user know that it was successful
        print("Changes Saved to " + ACType + ".json...\n")
        return
    else:#if they chose not to save their undesired changes etc.
        print("Changes have not been saved...")

def LoadChanges(ACType, settings):
    try:
        file = open(ACType + ".json","r")
        settings = json.load(file)
        file.close()
        print(ACType + ".json loaded successfully")
    except:#no file present, file gets created when we save later
        print("No " + ACType + ".json file was found or was corrupted.")
        settings = []

#Basic navigation functions til we get UI
# Accepts only integers
def InputInt(prompt): #finishmeTODO
    while True:
        entry = input(prompt)#custom input message
        try:
            intput = int(entry.strip())#remove whitespace
            return intput
        except:#if failed it is likely a string
            print("Please enter in an integer")
            continue

#Stringput
def InputSomething(prompt):
    while True:
        entry = input(prompt)#multiple entries not allowed for input function?
        if entry == "":
            print("Please enter an answer.")
            continue
        try:
            stringput = entry.strip().upper() #remove whitespace at the beginning and end, then sets to uppercase
            return stringput
        except:#obligatory backup exception for re-input
            print("Please try something else, you're not doing it right")
            continue

PyBetty = Program()



"""
a = Instance()

print(dir(a))


_list = [1, 3, 4]
print(dir(_list))

_list.append(5)

print(vars(_list))



class States:#TOFIX
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    def ACType(self):
        return self[type]

while True:

    try:
        with urllib.request.urlopen("http://localhost:8111/indicators") as url:
            indicators = json.loads(url.read().decode())
    except:
        print("nothing here yet")

    #basic read


    #need last aircraft type and current aircraft type, if different, load respective aircraf type
    #problem with this logic is that 8111 sometimes returns nothing and this will force an unwanted load
    #a possible solution could be to find the "average" aircraft type in the past 5 refreshes
    def LoadSettings():
        try:
            Aircraft = "mig-21_f13" #placeholder
            file = open(Aircraft + ".json","r")
            data = json.load(file)
            file.close()
            print(Aircraft + ".json loaded successfully")
            return data
        except:#no file present, file gets created when we save later
            print("No " + Aircraft + ".json file was found or was corrupted.")
            data = []
            return data

    def __init__(self):
    ACType = self.  indicators.type
    #mainshit

    #at the end of everything
    time.sleep(0.125)
    #aircraft sounds should not play over each other but should permit multiple-channels


    def saveChanges(settings):
        continYN = inputSomething("Y to save\n> ")
        if continYN == "Y":
            file = open(ACType + ".json", "w")
            json.dump(settings, file)
            file.close()#let the user know that it was successful
            print("Changes Saved to " + ACType + "json...\n")
            return
        else:#if they chose not to save their undesired changes etc.
            print("Changes have not been saved...")
"""
