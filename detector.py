import numpy as np
import dlib
import cv2

class Detector():
    
    def __init__(self):
        
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = \
        dlib.shape_predictor('/home/rjn/facial landmark/models/shape_predictor_68_face_landmarks.dat')
 
    def plot_landmark(self, gray,lands):
        
        for n,land in enumerate(lands):
            
            if n < 17 :
                color = (0, 255, 0)
                
            elif n >= 17 and n < 27 :
                color= (255, 0, 0)
                
            elif n >= 27 and n < 36 :
               color= (0, 0, 255)
                
            elif n >= 36 and n < 48 :
                color= (255, 255, 0)
            
            elif n >= 48 and n < 68 :
                color= (255, 0, 255)
                
            else:
                color = (255,255,255)
                  
            cv2.circle(gray, (land[0],land[1]), 2, (color), -1)
    
        mask = np.zeros(gray.shape)    
        
        points = np.array(lands, np.int32)
        convexhull = cv2.convexHull(points)
        cv2.fillConvexPoly(mask, convexhull, 255)
    
        gray = cv2.addWeighted(gray, 0.8, mask.astype('uint8'),0.3, 0)
        
        return gray     
    
    def shape_to_np(self, shape, dtype="int"):
    	# initialize the list of (x, y)-coordinates
    	coords = np.zeros((68, 2), dtype=dtype)
        
    	# loop over the 68 facial landmarks and convert them
    	# to a 2-tuple of (x, y)-coordinates
    	for i in range(0, 68):
    		coords[i] = (shape.part(i).x, shape.part(i).y)
            
    	# return the list of (x, y)-coordinates
    	return coords
    
    def detect_landmark(self, frame,filter_code=0):
        
        try: 
                                     
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # detect faces in the grayscale image
            rects = self.detector(gray,1)
            
            if filter_code == 0:
                for i,rect in enumerate(rects):
                    x = rect.left() - 15
                    y = rect.top() - 15
                    w = rect.right() + 10
                    h = rect.bottom() + 10
                    
                    lands = self.shape_to_np(self.predictor(gray, rect))
                    # Draw a box around the face
                    cv2.rectangle(frame, (x, y), (w, h), (100, 50, 255), 2)
                    cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
      		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                      
                    gray1 = frame[y:h,x:w]
                      
                    gray1 = self.plot_landmark(gray1,np.abs(lands - [x,y]))      
                    frame[y:h,x:w,] = gray1
                  
                return frame
            
            else:
                for i,rect in enumerate(rects):
                  lands = self.shape_to_np(self.predictor(gray, rect))  
                return lands
    
        except:
            return frame
    
    

