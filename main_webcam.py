import os
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode
import datetime

#read qr code from the camera and check if its ok

most_recent_access = {}

time_between_logs_th = 5 # after 5 seconds it will be possible for the already logged user to log in again

# Read authorized users from the whitelist file
with open('./whitelist.txt', 'r') as f:
    authorized_users = [l[:-1] for l in f.readlines() if len(l) > 2]
    #authorized_users = [l.strip() for l in f.readlines() if len(l.strip()) > 0]
    f.close()

# write the time users logs in (with correct qr code)
log_path = './log.txt'

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    qr_info = decode(frame)
    if(len(qr_info) > 0):
        qr = qr_info[0]

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon
        print('My data '+ data.decode())

        if data.decode() in authorized_users:
            cv2.putText(frame, 'ACCESS GRANTED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            if data.decode() not in most_recent_access.keys() \
                    or time.time() - most_recent_access[data.decode()] > time_between_logs_th:
                most_recent_access[data.decode()] = time.time()
                with open(log_path, 'a') as f: #a meaning append - so we dont overwrite our log.txt file
                    f.write('{},{}\n'.format(data.decode(), datetime.datetime.now()))
                    f.close()

        else:
            cv2.putText(frame, 'ACCESS DENIED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        3)
        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                            (0, 255, 0), 5)
        frame = cv2.polylines(frame, [np.array(polygon)], True, (255, 0, 0), 5)

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): # when q clicked, leave system
        break

cap.release()
cv2.destroyAllWindows()