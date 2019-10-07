from os import path
import sys

from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
from KortexCoreInterface.KortexCoreInterface import PropertyArgs as PropertyArgs
import EnumAndConsts.EnumsAndConsts as KortexEnums


TEST_ROOT_DIR = path.dirname(sys.modules['__main__'].__file__)

image1 = path.join(TEST_ROOT_DIR, "TestFiles/image1.jpg")
image2 = path.join(TEST_ROOT_DIR, "TestFiles/image2.jpg")
image3 = path.join(TEST_ROOT_DIR, "TestFiles/image3.jpg")
audio1 = path.join(TEST_ROOT_DIR, "TestFiles/Mann feat 50 Cent - Buzzin (Remix).mp3")
audio2 = path.join(TEST_ROOT_DIR, "TestFiles/Tupac-04 Soon As I Get Home-get-tunes.su.mp3")
project_name = "Project"

rootDir = input("Set your kortex project root directory: ")
rootDir = path.join(rootDir, project_name)
kortex_core = KortexCoreInterface(rootDir)

# Create base events
f1 = kortex_core.create_event("Feature1")
f2 = kortex_core.create_event("Feature2")
f3 = kortex_core.create_event("Feature3")
f4 = kortex_core.create_event("Feature4")

f1[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(img_path=image1)
f1[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
f1.import_file(path=audio1)

f2[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(img_path=image2)
f2.
f2[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="13/10/2019", time="20:30")
f2[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="13/10/2019", time="23:30")
f2.import_file(path=audio2, new_name="Audio2")

f3[KortexEnums.EPropertyType.IMAGE] = PropertyArgs(img_path=image3)
f3[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="20:00")
f3[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="18/10/2019", time="21:30")

f4[KortexEnums.EPropertyType.END_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="21:00")
f4[KortexEnums.EPropertyType.START_DATE_AND_TIME] = PropertyArgs(date="20/10/2019", time="10:00")

f1duration = f1.get_duration(time_unit=KortexEnums.ETimeInterval.MINUTE)
f2duration = f2.get_duration(time_unit=KortexEnums.ETimeInterval.HOUR)
f3duration = f3.get_duration(time_unit=KortexEnums.ETimeInterval.DAY)
f4duration = f4.get_duration(time_unit=KortexEnums.ETimeInterval.MINUTE)

# Create sub events related to Feature1
n11 = kortex_core.create_event("Nested11", holding_event=f1)
n12 = kortex_core.create_event("Nested12", holding_event=f1)
n13 = kortex_core.create_event("Nested13", holding_event=f1)
n14 = kortex_core.create_event("Nested14", holding_event=f1)

# Assign money balance to events
n11[KortexEnums.EPropertyType.CASH_FLOW] = PropertyArgs(cash_flow=650)
n12[KortexEnums.EPropertyType.CASH_FLOW] = PropertyArgs(cash_flow=-2000)
n14[KortexEnums.EPropertyType.CASH_FLOW] = PropertyArgs(cash_flow=8000)

# Get the events sorted by money balance
mb_sorted_list = f1.get_event_list(sort_by=KortexEnums.EPropertyType.CASH_FLOW)

# Create sub events related to Nested11
n111 = kortex_core.create_event("Nested111", holding_event=n11)
n112 = kortex_core.create_event("Nested112", holding_event=n11)
n113 = kortex_core.create_event("Nested113", holding_event=n11)
n114 = kortex_core.create_event("Nested114", holding_event=n11)

n111[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
n112[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.HIGH)
n113[KortexEnums.EPropertyType.IMPORTANCE] = PropertyArgs(importance=KortexEnums.Importance.MEDIUM)

importance_sorted = n11.get_event_list(sort_by=KortexEnums.EPropertyType.IMPORTANCE)

# Get all events in the project
root = kortex_core.get_event(name="Project")
all_events = root.get_event_list()
all_event_sorted_duration = root.get_event_list(sort_by=KortexEnums.EPropertyType.DURATION)
all_event_sorted_date = root.get_event_list(sort_by=KortexEnums.EPropertyType.START_DATE_AND_TIME)
kortex_core.print_project_tree()
f2.open_file(f2.files["Audio2.mp3"])
f1.open_event_location()
