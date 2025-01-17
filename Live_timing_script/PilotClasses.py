import re
import time
import datetime
from random import randint

class Pilot:
    def __init__(self, **kwargs):
        self.update(0, **kwargs)

    def update(self, position, **kwargs):
        self.absoluttime =      kwargs.get('ABSOLUTTIME', None)
        self.besttime =         kwargs.get('BESTTIME', None)
        self.besttimen =        kwargs.get('BESTTIMEN', None)
        self.carid =            kwargs.get('CARID', None)
        self.club =             kwargs.get('CLUB', None)
        self.color =            kwargs.get('COLOR', None)
        self.country =          kwargs.get('COUNTRY', None)
        self.delaytimefirst =   kwargs.get('DELAYTIMEFIRST', None)
        self.delaytimeprevious = kwargs.get('DELAYTIMEPREVIOUS', None)
        self.forecast =         kwargs.get('FORECAST', None)
        self.index =            kwargs.get('INDEX', None)
        self.laps =             kwargs.get('LAPS', None)
        self.laptime =          kwargs.get('LAPTIME', None)
        self.mediumtime =       kwargs.get('MEDIUMTIME', None)
        self.pilot =            kwargs.get('PILOT', None)
        self.pilotnumber =      kwargs.get('PILOTNUMBER', None)
        self.progress =         kwargs.get('PROGRESS', None)
        self.speed =            kwargs.get('SPEED', None)
        self.standarddeviation = kwargs.get('STANDARDDEVIATION', None)
        self.temperature =      kwargs.get('TEMPERATUR', None)
        self.transponder =      kwargs.get('TRANSPONDER', None)
        self.trend =            kwargs.get('TREND', None)
        self.vehicle =          kwargs.get('VEHICLE', None)
        self.voltage =          kwargs.get('VOLTAGE', None)
        self.position = position
        self.updateTime()
    
    def updateTime(self):
        try:
            self.besttime_s = float(self.besttime)
            self.besttimen_s = float(self.besttimen)
            self.laptime_s = float(self.laptime)
            self.mediumtime_s = float(self.mediumtime)
            m, s = map(int, str(self.absoluttime).split(":"))
            self.absoluttime_s = datetime.timedelta(minutes=m, seconds=float(s))
        except ValueError:
            print("ParseError")

class Round:
    RoundDict = {
        "100" : "4x2 Standard",
        "101" : "4x2 Modifié",
        "102" : "4xd Modifié",
        "103" : "Truck",
        "104" : "Vintage",
        "105" : "Rookie",
        "Online" : "4x0 Test"
                 }
    
    def __init__(self, **kwargs):
        self.pilotList = [Pilot(**pilot) for pilot in kwargs['DATA']]
        self.update(**kwargs)
        
    def update(self, **kwargs):
        self.countdown =        kwargs['METADATA'].get('COUNTDOWN', None)
        self.currenttime =      kwargs['METADATA'].get('CURRENTTIME', None)
        self.divergence =       kwargs['METADATA'].get('DIVERGENCE', None)
        self.group =            kwargs['METADATA'].get('GROUP', None)
        self.name =             kwargs['METADATA'].get('NAME', None)
        self.racetime =         kwargs['METADATA'].get('RACETIME', None)
        self.remainingtime =    kwargs['METADATA'].get('REMAININGTIME', None)
        self.section =          kwargs['METADATA'].get('SECTION', None)
        self.updateRaceTime(randomize=True)
        self.updatePilotList(kwargs['DATA'])
        self.parseCategory()

    def updateRaceTime(self, randomize=False):
        h, m, s = map(int, str(self.racetime).split(":"))
        self.racetime_s = datetime.timedelta(hours=h, minutes=m, seconds=s)
        h, m, s = map(int, str(self.remainingtime).split(":"))
        self.remainingtime = datetime.timedelta(hours=h, minutes=m, seconds=s) + datetime.timedelta(seconds=randint(1,60))*randomize
        

    def getRaceTime_pretty(self):
        #returns a pretty string of the current race time
        if self.racetime_s.seconds>3600:
            return f"{self.remainingtime} / {self.racetime_s}"
        else:
            return f"{str(self.remainingtime)[-5:]} / {str(self.racetime_s)[-5:]}"
    
    def parseCategory(self):
        self.roundData = f"{self.section}{self.group}"
        try:
            categoryMatch = re.findall(pattern="\[(\d{3})\].*?::(.*)", string=self.roundData)
            catNumber = categoryMatch[0][0]
            serie = categoryMatch[0][1:][0].replace("::","-")
            self.round_pretty = self.RoundDict[catNumber]+serie
        except IndexError:
            print("Error parsing category")
        except KeyError:
            self.round_pretty = "Manche non reconnue"

        print(f"Manche en cours : {self.roundData} ==> {self.round_pretty}")
    
    def updatePilotList(self, data:list):
        self.numberOfPilots = len(data)
        for i, pilot in enumerate(data):
            self.pilotList[i].update(i, **pilot)
