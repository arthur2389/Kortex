from Kortex.KortexCoreInterface.KortexCoreInterface import KortexCoreInterface as KortexCoreInterface
import Kortex.KortexData.KortexEnums as KortexEnums

date = "31/12/2012"
time = "23:58"

rootDir = "C:\\Users\\USER\\Documents\\arthur\\Project"
files = [{"image": "C:\\Users\\USER\\Documents\\image1.jpg",
          "desc": "Woman with boat an castle",
          "importance" : KortexEnums.Importance.HIGH},
         {"image": "C:\\Users\\USER\\Documents\\image2.jpg",
          "desc": "Turtles an butterflies",
          "importance": KortexEnums.Importance.LOW},
         {"image": "C:\\Users\\USER\\Documents\\image3.jpg",
          "desc": "Woman looking at a distante castle",
          "importance": KortexEnums.Importance.LOW}]

kortexCore = KortexCoreInterface(rootDir)
pass
