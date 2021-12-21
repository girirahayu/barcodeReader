import cv2
import os
from pyzbar import pyzbar
from datetime import date


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

def generateDir(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir, 0o777)


def read_barcodes(frame,dir_format):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        key = cv2.waitKey(1)
        if key == ord('s'): 
            # with open("barcode_result.txt", mode ='w') as file:
            #     file.write("Recognized Barcode:" + barcode_info)
            cv2.imwrite(filename=ROOT_DIR+"/"+dir_format+"/"+barcode_info+".jpg", img=frame)
            img_new = cv2.putText(frame, "Saved!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 87, 51), 2, cv2.LINE_AA)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

    return frame


def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    today = date.today()
    dir_format = today.strftime("%d%b%Y")
    generateDir(dir_format)
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame,dir_format)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()