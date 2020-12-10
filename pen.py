import cv2
import numpy as np 

class Pen:
        def __init__(self,webcam):
                self.cap = webcam
                self.img = None
                self.dilate = None
                self.blurred = None
                self.hsv = None
                self.Mask = None
                self.edges = None
                self.cnts = None
                self.low_red = (136, 87, 111)
                self.high_red = (180, 255, 255)
                self.filtered = None
                self.xs  = self.ys = []
                self.mode = cv2.RETR_LIST
                self.method = cv2.CHAIN_APPROX_SIMPLE
                self.winname = "Frame"
                self.key = cv2.waitKey(1)
                self.kernel = np.ones((7,7),np.uint8)

        def get_frames(self):
                _,self.img = self.cap.read()
                self.img = self.flip(self.img)
                self.img = self.resize(self.img)

        def filters(self,image):
                self.dilate = cv2.dilate(image,self.kernel,iterations=1)
                self.blurred = cv2.GaussianBlur(self.dilate,self.kernel.shape,0)
                self.hsv = cv2.cvtColor(self.blurred,cv2.COLOR_BGR2HSV)
                return self.hsv

        def resize(self,image):
                return cv2.resize(image,(288*3,512))

        def flip(self,image):
                return cv2.flip(image,1)

        def mask(self):
                self.Mask = cv2.inRange(self.filters(self.img),self.low_red,self.high_red)
                self.edges = cv2.Canny(self.Mask,100,150)
                cv2.imshow("edges",cv2.resize(self.edges,(288,170)))
                return self.edges

        def current_point(self):
                return min(self.ys)
                
        def contours(self):
                self.cnts,_ = cv2.findContours(self.mask(),self.mode,self.method)

        def points(self,cnts):
                self.xs,self.ys = [],[]
                try:
                        for cnt in cnts[:]:
                                self.xs.append(cnt[0][0][0])
                                self.ys.append(cnt[0][0][1])
                        points = (min(self.xs),min(self.ys))
                        self.draw_points(points)
                except Exception:
                        pass

        def draw_points(self,coordinates):
                cv2.circle(self.img,coordinates,10,(255,0,0),-1)
                
        def show(self):
                cv2.imshow(self.winname,cv2.resize(self.img,(288,170)))

        def main(self):
                self.get_frames()
                self.contours()
                self.points(self.cnts)
                self.show()
                self.key = cv2.waitKey(1)
                Y = self.current_point()
                return Y



