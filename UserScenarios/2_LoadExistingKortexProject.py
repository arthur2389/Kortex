from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
from KortexCoreInterface.KortexCoreInterface import PropertyArgs as PropertyArgs
import EnumAndConsts.EnumsAndConsts as KortexEnums
from KortexCoreInterface.KortexCoreInterface import DateTimeArgs

rootDir = input("Set your kortex project root directory: ")

kortex_core = KortexCoreInterface(rootDir)

# Get some events
n111 = kortex_core.get_event("Nested111")
n112 = kortex_core.get_event("Nested112")
n113 = kortex_core.get_event("Nested113")
n114 = kortex_core.get_event("Nested114")


# Change importance
n112[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.LOW)

n11 = kortex_core.get_event("Nested11")
n12 = kortex_core.get_event("Nested12")
n13 = kortex_core.get_event("Nested13")
n14 = kortex_core.get_event("Nested14")

n11.set_date_time(start_date_time_args=DateTimeArgs(day=15, month=10, year=2019, hour=0, minute=30),
                  end_date_time_args=DateTimeArgs(day=23, month=10, year=2019, hour=0, minute=50))


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
