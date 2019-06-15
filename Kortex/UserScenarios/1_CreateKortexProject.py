from os import path
import sys

from Kortex.KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
from Kortex.KortexCoreInterface.KortexCoreInterface import PropertyArgs as PropertyArgs
import Kortex.KortexData.KortexEnums as KortexEnums


TEST_ROOT_DIR = path.dirname(sys.modules['__main__'].__file__)

image1 = path.join(TEST_ROOT_DIR, "TestFiles/image1.jpg")
image2 = path.join(TEST_ROOT_DIR, "TestFiles/image2.jpg")
image3 = path.join(TEST_ROOT_DIR, "TestFiles/image3.jpg")
audio1 = path.join(TEST_ROOT_DIR, "TestFiles/Mann feat 50 Cent - Buzzin (Remix).mp3")
audio2 = path.join(TEST_ROOT_DIR, "TestFiles/Tupac-04 Soon As I Get Home-get-tunes.su.mp3")
projectName = "Project"

rootDir = input("Set your kortex project root directory: ")
rootDir = path.join(rootDir, projectName)
kortexCore = KortexCoreInterface(rootDir)

# Create base events
f1 = kortexCore.CreateEvent("Feature1")
f2 = kortexCore.CreateEvent("Feature2")
f3 = kortexCore.CreateEvent("Feature3")
f4 = kortexCore.CreateEvent("Feature4")

f1[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(imgPath=image1)
f1[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
f1.ImportFile(path=audio1)

f2[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(imgPath=image2)
f2[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="13/10/2019", time="20:30")
f2[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="13/10/2019", time="23:30")
f2.ImportFile(path=audio2, newName="Audio2")

f3[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(imgPath=image3)
f3[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="20:00")
f3[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="18/10/2019", time="21:30")

f4[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="21:00")
f4[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="10:00")

f1duration = f1.GetDuration(timeUnit=KortexEnums.ETimeInterval.MINUTE)
f2duration = f2.GetDuration(timeUnit=KortexEnums.ETimeInterval.HOUR)
f3duration = f3.GetDuration(timeUnit=KortexEnums.ETimeInterval.DAY)
f4duration = f4.GetDuration(timeUnit=KortexEnums.ETimeInterval.MINUTE)

# Create sub events related to Feature1
n11 = kortexCore.CreateEvent("Nested11", holdingEvent=f1)
n12 = kortexCore.CreateEvent("Nested12", holdingEvent=f1)
n13 = kortexCore.CreateEvent("Nested13", holdingEvent=f1)
n14 = kortexCore.CreateEvent("Nested14", holdingEvent=f1)

# Assign money balance to events
n11[KortexEnums.EPropertyType.MONEY_BALANCE] = PropertyArgs(moneyBalance=650)
n12[KortexEnums.EPropertyType.MONEY_BALANCE] = PropertyArgs(moneyBalance=-2000)
n14[KortexEnums.EPropertyType.MONEY_BALANCE] = PropertyArgs(moneyBalance=8000)

# Get the events sorted by money balance
mbSortedList = f1.GetEventList(sortBy=KortexEnums.EPropertyType.MONEY_BALANCE)

# Create sub events related to Nested11
n111 = kortexCore.CreateEvent("Nested111", holdingEvent=n11)
n112 = kortexCore.CreateEvent("Nested112", holdingEvent=n11)
n113 = kortexCore.CreateEvent("Nested113", holdingEvent=n11)
n114 = kortexCore.CreateEvent("Nested114", holdingEvent=n11)

n111[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
n112[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
n113[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.MEDIUM)

importanceSorted = n11.GetEventList(sortBy=KortexEnums.EPropertyType.IMPORTANCE)

# Get all events in the project
root = kortexCore.GetEvent(name="Project")
allEvents = root.GetEventList()
allEventSortedDuration = root.GetEventList(sortBy=KortexEnums.EPropertyType.DURATION)
allEventSortedDate = root.GetEventList(sortBy=KortexEnums.EPropertyType.START_DATE_AND_TIME)
kortexCore.PrintProjectTree()
f2.OpenFile(f2.files["Audio2.mp3"])
f1.OpenEventLocation()
