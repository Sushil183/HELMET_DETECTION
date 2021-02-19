
'''
TEAM DIJON
THIS PORTION SHOWS READING AND TRAINING THE DATASET WHICH WE OBTAINED FROM KAGGLE , SINCE THE DATASET IS IN .XML FILE FIRST
WE WILL READ THE DATASET AND FROM THERE WE WILL STORE THE DATASET
'''

#IMPORTING NECCESSARY LIBRARY
import xml.etree.ElementTree as ET #FOR READING XML FILES
import os  #FOR PATH BASED OPERATION
import cv2 # FOR IMAGE BASED OPERATION
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow


#Defining some functions
def showBox(frame,xmin,ymin,xmax,ymax,Switch):
    if Switch == 'With Helmet':
        color = (0,255,0)
    else:
        color = (0,0,255)
    cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),color,2)

###############################################
#READING THE DATASET WHICH IS IN .XML FORMAT
# WE WILl CREATE TWO LIST THAT WILL STORE OUR DATASET
HELMET = []
NO_HELMET = []

DIRECTORY = r"annotations"
DIRECTORY2 = r"images"
for xml_file in os.listdir(DIRECTORY):
    path = os.path.join(DIRECTORY,xml_file)

    tree = ET.parse(path)
    root = tree.getroot()

    img_path = os.path.join(DIRECTORY2,str(root.find('filename').text))
    frame = cv2.imread(img_path)
    for member in root.findall('object'):

        Switch  = member.find('name').text
        for i in member.findall('bndbox'):
            xmin = int(i.find('xmin').text) - 20
            ymin = int(i.find('ymin').text) - 20
            xmax = int(i.find('xmax').text) + 20
            ymax = int(i.find('ymax').text) + 20

            if xmin < 0 :
                xmin = int(i.find('xmin').text)
            if ymin < 0 :
                ymin = int(i.find('ymin').text)

            if Switch == 'With Helmet':
                temp = frame[ymin:ymax,xmin:xmax]
                if temp.shape[0] != 0 and temp.shape[1] != 0 :
                    temp = cv2.resize(temp,(224,224))
                    HELMET.append(temp)
                # print('Added 1 image to HELMET LIST')
            else:
                temp = frame[ymin:ymax,xmin:xmax]
                if temp.shape[0] != 0 and temp.shape[1] != 0 :
                    temp = cv2.resize(temp,(224,224))
                    NO_HELMET.append(temp)
                # print('Added 1 image to NO_HELMET LIST')
    #     showBox(frame,xmin,ymin,xmax,ymax,Switch)
    # cv2.imshow('hi',frame)
    # cv2.waitKey(200)

labels = [] #We will set '1' as label for image with helmet and '0' as label for image with no helmet
img_data = []

for i in HELMET:
    j = cv2.cvtColor(i,cv2.COLOR_BGR2RGB)
    j = tensorflow.keras.applications.mobilenet_v2.preprocess_input(j)
    img_data.append(j)
    labels.append('HELMET')

for i in NO_HELMET:
    j = cv2.cvtColor(i,cv2.COLOR_BGR2RGB)
    j = tensorflow.keras.applications.mobilenet_v2.preprocess_input(j)
    img_data.append(j)
    labels.append('NO_HELMET')

# print(labels.shape)

from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

img_data=np.array(img_data,dtype="float32") # converting to numpy FORMAT
labels = np.array(labels)


from sklearn.model_selection import train_test_split
(trainX, testX, trainY, testY) = train_test_split(img_data, labels,
	test_size=0.20, stratify=labels, random_state=42)

# for i in HELMET:
#     # print(i.shape)
#     cv2.imshow('hi',i)
#     cv2.waitKey(500)




cv2.destroyAllWindows()
