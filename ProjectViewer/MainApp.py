from ProjectViewer.KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
import ProjectViewer.KortexData.KortexEnums as PVEnums

date = "31/12/2012"
time = "23:58"

rootDir = "C:\\Users\\USER\\Documents\\arthur\\Project"
files = [{"image": "C:\\Users\\USER\\Documents\\image1.jpg",
          "desc": "Woman with boat an castle",
          "theme": "C:\\Users\\USER\\Documents\\arthur\\Project\\Feature1",
          "importance" : PVEnums.Importance.HIGH},
         {"image": "C:\\Users\\USER\\Documents\\image2.jpg",
          "desc": "Turtles an butterflies",
          "theme": "C:\\Users\\USER\\Documents\\arthur\\Project\\Feature2",
          "importance": PVEnums.Importance.LOW},
         {"image": "C:\\Users\\USER\\Documents\\image3.jpg",
          "desc": "Woman looking at a distante castle",
          "theme": "C:\\Users\\USER\\Documents\\arthur\\Project\\Feature3",
          "importance": PVEnums.Importance.LOW}]

pvManager = KortexCoreInterface(rootDir)

for i in range(3):
    pvManager.AddPropertyToEvent(eventPath=files[i]["theme"],
                                 property=PVEnums.EPropertyType.IMAGE,
                                 picPath=files[i]["image"])
    pvManager.AddPropertyToEvent(eventPath=files[i]["theme"],
                                 property=PVEnums.EPropertyType.DESCRIPTION,
                                 desc=files[i]["desc"])
    pvManager.AddPropertyToEvent(eventPath=files[i]["theme"],
                                 property=PVEnums.EPropertyType.IMPORTANCE,
                                 importance=files[i]["importance"])
    pvManager.AddPropertyToEvent(eventPath=files[i]["theme"],
                                 property=PVEnums.EPropertyType.DATE_AND_TIME,
                                 date=date,
                                 time=time)

feature4 = pvManager.CreateEvent("Feature4")
pvManager.CreateEvent("NestedFeature4", feature4)

pvManager.PrintProjectTree()
feature1 = pvManager.GetEvent("Feature1")
nested21 = pvManager.GetEvent("Nested21")
pass
