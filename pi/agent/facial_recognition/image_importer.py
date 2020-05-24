import glob
import os
import recogniser
import cv2

importing_class = recogniser.Facialrecog()
username = input("Username to add images too:")
os.chdir("/import")
for file in glob.glob("*.jpg"):
    img = cv2.imread(file)
    importing_class.add_image(username,img)
importing_class.add_image()
