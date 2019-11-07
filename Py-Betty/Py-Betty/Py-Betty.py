# Py-Betty - ZdrytchX
# debugging cmd line python -m ipdb Py-Betty.py
# import tkinter
# import tkinter.messagebox
import time
import random
# import urllib.request
import requests  # this?
# import http
# import io
import json
# import some kind of sound library
# import libao #pydub TODO
import itertools, sys  # spinner thing
import math


class settings:  # more like a data struct
    def __init__(self):
        # states
        self.Redline  # max IAS
        self.MaxTemp  # max raw temperature
        self.MaxOilTemp  # max oil temperature
        self.MaxWaterTemp  # max water temperature
        self.AoAWarn  # AoA warning
        self.AoAMax  # max angle of attack
        self.GearUp  # GearUp threshold
        self.GearDn  # GearDown threshold
        self.MaxRPM  # Max RPM
        self.Mach  # Max Mach Speed
        self.Flaps1  # Max Speed Flaps Combat
        self.Flaps2  # Max Speed Flaps Take-off
        self.Flaps3  # Max Speed Flaps Landing
        self.GLoad  # Max G-Loading
        self.GLoad - Ve  # Minimum G-Loading
        self.MaxDescent  # Maximum Descent Rate
        self.MaxAoS  # Max Absolute Sideslip
        self.BingoFuel  # Bingo Fuel Threshold, fraction of Mfuel / Mfuel0
        self.BingoFuelRepeats  # number of times to repeat warning
        self.Economy  # Efficiency of Prop for whatever reason
        # Indicators
        self.MaxBankAngle  # Max Banking Angle for Autopilot


# List of uservalues
# {"Redline", "MaxTemp", "MaxOilTemp","MaxWaterTemp","MaxAoA","GearUp","GearDn","MaxRPM","Mach","Flaps1","Flaps2","Flaps3","GLoad","GLoad-Ve","MaxDescent","MaxAoS","BingoFuel","BingoFuelRepeats","Economy","MaxBankAngle"}

# TODO: Iterate through to get a more definitive long term solution
# Ideally, it should just grab only the necessary values off 8111
def SetSettings(data):
    data = ["Redline", "MaxTemp", "MaxOilTemp", "MaxWaterTemp", "MaxAoA", "GearUp", "GearDn", "MaxRPM", "Mach",
            "Flaps1", "Flaps2", "Flaps3", "GLoad", "GLoad-Ve", "MaxDescent", "MaxAoS", "BingoFuel", "BingoFuelRepeats",
            "Economy", "MaxBankAngle"]  # needs to be dict later but regular list for now


class Navigation:  # Mostly for autopilot integreation possibility
    def __init__(self):
        self.Compass  # Desired Compass Heading
        self.Distance  # Distance to travel
        self.Time  # Time to travel, interchangable with the above
        self.Altitude  # Cruising Altitude
        self.Bombdrops  # Number of times to smash the bomb drop button


class Program:  # "blueprint"
    def __init__(ac, *args, **kwargs):
        ACsettings = {}
        currentACType = "zzz_unavailable"
        ACActive = True  # if set to False initially, program will not tell you that aircraft isn't active
        ACTypeHistory = ["zzz_unavailable", "zzz_unavailable", "zzz_unavailable",
                         "zzz_unavailable"]  # random invalid buffer where json fails to output
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        barcapacitywidth = 64
        barlinesPrinted = 0

        # user settings
        TEMP_AoALIMIT = 12

        # global vars which should become global settings eventually
        AoA_Warning = "STALL WARNING   "  # 16 character long messages
        Drift_Warning = "OVER DRIFT      " # FIXME: get a better solution

        while True:
            ac.indicators = FetchIndicators()
            ac.state = FetchStatus()
            if ("valid" in ac.state and "valid" in ac.indicators and ac.state["valid"] == True and ac.indicators[
                "valid"] == True):  # DP: state can lie, but indicators tell the truth

                ShuffleThroughList(ACTypeHistory, ac.indicators["type"])

                # shows 8111 hiccups
                if ACActive == False:
                    ACActive = True
                    print("Main Active: " + ac.indicators["type"], end=" | ")
                    print("FetchIndicators() | Active: " + str(ac.indicators["valid"]),
                          end=" | ")  # stored in dictionary type
                    print("FetchStatus() | Active: " + str(ac.state["valid"]))  # stored in dictionary type

                # 8111 hiccup immunity
                if (ACTypeHistory[0] == ACTypeHistory[1] == ACTypeHistory[2] == ACTypeHistory[3] and ACTypeHistory[
                    3] != currentACType):
                    print("New Aircraft: " + ac.indicators["type"])
                    currentACType = ac.indicators["type"]
                    LoadChanges(ac.indicators["type"], ACsettings)

                # print display bar thingy as a test
                # in the actual thing there will be warning sounds in place here
                if "AoA, deg" in ac.state and "AoS, deg" in ac.state:
                    # Angle of Attack Warning
                    # DrawBars(ac.state["AoA, deg"], barcapacitywidth, -barcapacitywidth/2, barcapacitywidth/2, barcapacitywidth/2, TEMP_AoALIMIT, AoA_Warning, barlinesPrinted)

                    # Maximum Drift Meter
                    driftSpeed = round(ac.state["TAS, km/h"] * math.sin(math.radians(ac.state["AoS, deg"])), 1)
                    DrawBars(abs(driftSpeed), barcapacitywidth / 2, 0, 55,
                             0, 55, Drift_Warning, barlinesPrinted)


            else:
                if ACActive == True:
                    ACActive = False
                    print("Main Active: Aircraft Not Active", end=" | ")
                    print("FetchIndicators() | Active: " + str(ac.indicators["valid"]), end=" | ")
                    print("FetchStatus() | Active: " + str(ac.state["valid"]))  # stored in dictionary type


            # spinner thing to show it is active ripped from stackoverlow
            sys.stdout.write(next(spinner))  # write the next character
            sys.stdout.flush()  # flush stdout buffer (display characters now, do not wait)

            # End of main loop:
            time.sleep(0.03125) #32 FPS for testing purposes, I'll lower it later and give it as a global setting option

            #clear excess text
            sys.stdout.write('\b\b\b\b\b')
            sys.stdout.write('     ')#TODO: Find a better solution
            # sys.stdout.write('\r')            # erase the last written char \b moves curst back 1, \r moves cursor to start of line
            # while barlinesPrinted > 0:
            #    sys.stdout.write("\033[F")#moves cursor up one line and to the beginning / doesnt work on pycharm terminal
            sys.stdout.write('\r') #move cursor back to the beginning so we can write over it

#def FindMaxDriftAngle(speed):

    #if speed > 50:
    #    ratio = 50 / abs(speed)
    #    maxDriftAngle = math.asin(ratio)
    #    return math.degrees(maxDriftAngle)
    #else:
    #    return 90


def DrawBars(value, width, min, max, startpos, threshold, msg, printcount):
    # scale bars accoridingly to the bar width and numerical limits
    minmaxDifference = max - min
    multiplier = width/minmaxDifference
    bars = int(value) * multiplier + startpos

    # visual bar capacity [min    max]
    if bars > width:
        bars = width
    elif bars < 0:
        bars = 0

    barLength = int(bars) * "I"
    emptySpace = (int((width - bars))) * "-"

    # VarNumber = str(value) #FIXME: need better solution for erasing excessively long text
    # if len(VarNumber) < 5:
    #    VarNumber = AoANumber + " " * (5 - len(VarNumber))

    if int(value) > threshold:
        warningMessage = " " + str(value) + " " + msg
    else:
        warningMessage = " " + str(value) + "                 "

    print("[" + barLength + emptySpace + "]" + warningMessage, end="")
    printcount = printcount + 1  # FIXME does not modify value outside function
    return printcount


def PlayWarning(warningtype, indication):
    print(str(warningtype) + " Warning: " + str(indication))  # Replace this with sound playback l8r


def CheckExceeded(warningtype, indication):
    print("CheckExceeded() | nothing here yet")
    pass


def FetchIndicators():
    indicators = {}
    try:
        # with urllib.request.urlopen("http://localhost:8111/indicators") as url:
        # indicators = json.loads(url.read().decode())
        indicators = requests.get("http://localhost:8111/indicators", timeout=0.02).json()
        return indicators
    except:
        indicators["valid"] = False
        indicators["type"] = "zzz_unavailable"
        return indicators


def FetchStatus():
    state = {}
    try:
        state = requests.get("http://localhost:8111/state", timeout=0.02).json()
        return state
        # States are given in dict fomat "title, unit": value
    except:
        state["valid"] = False
        state["type"] = "zzz_unavailable"
        return state


def SaveChanges(ACType, settings):
    continYN = InputSomething("Y to save\n> ")
    if continYN == "Y":
        file = open(ACType + ".json", "w")
        json.dump(settings, file)
        file.close()  # let the user know that it was successful
        print("Changes Saved to " + ACType + ".json...\n")
        return
    else:  # if they chose not to save their undesired changes etc.
        print("Changes have not been saved...")


def LoadChanges(ACType, settings):
    try:
        file = open(ACType + ".json", "r")
        settings = json.load(file)
        file.close()
        print(ACType + ".json loaded successfully")
    except:  # no file present, file gets created when we save later
        print("No " + ACType + ".json file was found or was corrupted.")
        SetSettings(settings)
        SaveChanges(ACType, settings)


# Basic navigation functions til we get UI
# Accepts only integers
def InputInt(prompt):  # finishmeTODO
    while True:
        entry = input(prompt)  # custom input message
        try:
            intput = int(entry.strip())  # remove whitespace
            return intput
        except:  # if failed it is likely a string
            print("Please enter in an integer")
            continue


# Stringput
def InputSomething(prompt):
    while True:
        entry = input(prompt)  # multiple entries not allowed for input function?
        if entry == "":
            print("Please enter an answer.")
            continue
        try:
            stringput = entry.strip().upper()  # remove whitespace at the beginning and end, then sets to uppercase
            return stringput
        except:  # obligatory backup exception for re-input
            print("Please try something else, you're not doing it right")
            continue


def ShuffleThroughList(zalist, input):  # might be computationally inefficient
    del zalist[0]
    zalist.append(input)
    return


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
