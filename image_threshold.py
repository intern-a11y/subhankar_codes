import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np




img = cv2.imread('44572929-e641-461a-bd0b-1a3964ea6db5-01.jpg',1)
ret,thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
# ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
# ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
# ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
# ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

titles = ['BINARY']
images = [thresh1]

# for i in range(1):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])

# plt.show()
# cv2.imshow('Image', images)
# cv2.waitKey(0)
cv2.imwrite("threshed_gray1.jpg", thresh1)
 
# def funcBrightContrast(bright=0):
#     bright = cv2.getTrackbarPos('bright', 'Life2Coding')
#     contrast = cv2.getTrackbarPos('contrast', 'Life2Coding')
 
#     effect = apply_brightness_contrast(img,bright,contrast)
#     cv2.imshow('Effect', effect)
 
# def apply_brightness_contrast(input_img, brightness = 255, contrast = 127):
#     brightness = map(brightness, 0, 510, -255, 255)
#     contrast = map(contrast, 0, 254, -127, 127)
 
#     if brightness != 0:
#         if brightness > 0:
#             shadow = brightness
#             highlight = 255
#         else:
#             shadow = 0
#             highlight = 255 + brightness
#         alpha_b = (highlight - shadow)/255
#         gamma_b = shadow
 
#         buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
#     else:
#         buf = input_img.copy()
 
#     if contrast != 0:
#         f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
#         alpha_c = f
#         gamma_c = 127*(1-f)
 
#         buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
 
#     cv2.putText(buf,'B:{},C:{}'.format(brightness,contrast),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#     return buf
 
# def map(x, in_min, in_max, out_min, out_max):
#     return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
 
# if __name__ == '__main__':
 
#     original = cv2.imread("./44572929-e641-461a-bd0b-1a3964ea6db5-01.jpg", 1)
#     img = original.copy()
 
#     cv2.namedWindow('Life2Coding',1)
 
#     bright = 255
#     contrast = 150
 
#     #Brightness value range -255 to 255
#     #Contrast value range -127 to 127
 
#     cv2.createTrackbar('bright', 'Life2Coding', bright, 2*255, funcBrightContrast)
#     cv2.createTrackbar('contrast', 'Life2Coding', contrast, 2*127, funcBrightContrast)
#     funcBrightContrast(0)
#     cv2.imshow('Life2Coding', original)
 
 
# cv2.waitKey(0)

