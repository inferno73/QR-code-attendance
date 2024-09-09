import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode

#used for reading QR code images saved locally

input_dir = r'C:\Users\Korisnik\Documents\Coding\CourseCVEmaterial\qr-code'

for j in sorted(os.listdir(input_dir)):
    img = cv2.imread(os.path.join(input_dir,j))
    qr_info = decode(img)

    #print(qr_info)
    #print(j, len(qr_info)) # len gives how many qr codes in  an image

    for qr in qr_info:
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                            (0,255,0), 5)
        img = cv2.polylines(img, [np.array(polygon)], True, (255,0,0), 5)
        print(data)
        print(rect)
        print(polygon)

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()