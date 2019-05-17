from Kortex.KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
from Kortex.KortexCoreInterface.KortexCoreInterface import PropertyArgs as PropertyArgs
import Kortex.KortexData.KortexEnums as KortexEnums

rootDir = input("Set your kortex project root directory: ")

kortexCore = KortexCoreInterface(rootDir)

# Get some events
n111 = kortexCore.GetEvent("Nested111")
n112 = kortexCore.GetEvent("Nested112")
n113 = kortexCore.GetEvent("Nested113")
n114 = kortexCore.GetEvent("Nested114")

# Set date and time
n112[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="14/10/2020", time="15:00")
n113[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="15/10/2020", time="10:00")
n114[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="21/10/2020", time="09:00")

# Change importance
n112[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.LOW)

n11 = kortexCore.GetEvent("Nested11")
n12 = kortexCore.GetEvent("Nested12")
n13 = kortexCore.GetEvent("Nested13")
n14 = kortexCore.GetEvent("Nested14")

n11[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="10:00")
n12[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="11:30")
n13[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="11:50")
n14[KortexEnums.EPropertyType.DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="12:30")

kortexCore.RemoveEvent(n112)
kortexCore.RemoveEvent(n113)

try:
    kortexCore.MoveEvent(n11, n111)
except NotImplementedError:
    pass
try:
    kortexCore.MoveEvent(n11, n114)
except NotImplementedError:
    pass

f1 = kortexCore.GetEvent("Feature1")
f2 = kortexCore.GetEvent("Feature2")

try:
    kortexCore.MoveEvent(f1, n111)
except NotImplementedError:
    pass
try:
    kortexCore.MoveEvent(f1, n114)
except NotImplementedError:
    pass

kortexCore.MoveEvent(f2, n114)

root = kortexCore.GetEvent(name="Project")
kortexCore.MoveEvent(n11, root)
kortexCore.MoveEvent(n14, root)


# Get all events in the project
allEvents = root.GetEventList()
allEventSortedDate = root.GetEventList(sortBy=KortexEnums.EPropertyType.DATE_AND_TIME)
