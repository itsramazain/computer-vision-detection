import numpy as np
import cv2 as cv
polygon = np.array([[(20, 20), (220, 20), (220, 70), (20, 70)]])
capture=cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FRAME_WIDTH,1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT,720)
net=cv.dnn.readNet('yolov4-tiny.weights','yolov4-tiny.cfg')
model=cv.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)
objects=[]
select_person=False
cv.namedWindow('object_detect_window')
def click_button(event,x,y,flags,params):
    global select_person
    if event==cv.EVENT_LBUTTONDOWN:
        if cv.pointPolygonTest(polygon,(x,y),False):
            if select_person:
                select_person=False
            else:
                select_person = True

cv.setMouseCallback('object_detect_window',click_button)
with open('classes.txt') as f:
    for line in f:
        line=line.rstrip()
        objects.append(line)
while True:
    _,frame=capture.read()
    class_ids,scores,bboxs=model.detect(frame)
    for class_id,score,bbox in zip(class_ids,scores,bboxs):
        polygon = np.array([[(20, 20), (220, 20), (220, 70), (20, 70)]])
        cv.fillPoly(frame,polygon,(0,0,200))
        cv.putText(frame, 'person', (25, 45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if select_person:
            x,y,w,h=bbox
            cv.putText(frame,objects[class_id],(x,y-10),cv.FONT_HERSHEY_SIMPLEX,1,(200,0,20),2)
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),1)
    cv.imshow('object_detect_window',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.waitKey(0)
cv.release()
cv.destroyAllWindows()
