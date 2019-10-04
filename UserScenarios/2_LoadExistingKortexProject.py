from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
from KortexCoreInterface.KortexCoreInterface import PropertyArgs as PropertyArgs
import EnumAndConsts.EnumsAndConsts as KortexEnums

rootDir = input("Set your kortex project root directory: ")

kortex_core = KortexCoreInterface(rootDir)

# Get some events
n111 = kortex_core.get_event("Nested111")
n112 = kortex_core.get_event("Nested112")
n113 = kortex_core.get_event("Nested113")
n114 = kortex_core.get_event("Nested114")

# Set date and time
n112[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="14/10/2020", time="15:00")
n113[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="15/10/2020", time="10:00")
n114[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="21/10/2020", time="09:00")

# Change importance
n112[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.LOW)

n11 = kortex_core.get_event("Nested11")
n12 = kortex_core.get_event("Nested12")
n13 = kortex_core.get_event("Nested13")
n14 = kortex_core.get_event("Nested14")

n11[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="10:00")
n12[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="11:30")
n13[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="11:50")
n14[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="1/1/2021", time="12:30")

kortex_core.remove_event(n112)
kortex_core.remove_event(n113)

try:
    kortex_core.move_event(n11, n111)
except NotImplementedError:
    pass
try:
    kortex_core.move_event(n11, n114)
except NotImplementedError:
    pass

f1 = kortex_core.get_event("Feature1")
f2 = kortex_core.get_event("Feature2")

try:
    kortex_core.move_event(f1, n111)
except NotImplementedError:
    pass
try:
    kortex_core.move_event(f1, n114)
except NotImplementedError:
    pass

kortex_core.move_event(f2, n114)

root = kortex_core.get_event(name="Project")
kortex_core.move_event(n11, root)
kortex_core.move_event(n14, root)


# Get all events in the project
all_events = root.get_event_list()
all_event_sorted_date = root.get_event_list(sort_by=KortexEnums.EPropertyType.START_DATE_AND_TIME)
kortex_core.print_project_tree()
