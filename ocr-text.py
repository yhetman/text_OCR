import cv2
import sys
import pytesseract
import numpy as np
from PIL import Image, ImageChops


def isGrayScale(path):
	im = Image.open(path).convert('RGB')
	w,h = im.size
	for i in range(w):
		for j in range(h):
			r,g,b = im.getpixel((i,j))
			if r != g != b: return True
	return False


image_path = sys.argv[1]
image = cv2.imread(image_path)

isGray = isGrayScale(image_path)

ker = np.ones((2,1), np.uint8)

if isGray == False:
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	gray, image_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	gray = cv2.bitwise_not(image_bin)
	image = cv2.erode(gray, ker, iterations=1)
else:
	image = cv2.erode(image, ker, iterations=1)

image = cv2.dilate(image, ker, iterations=1)

out_result = pytesseract.image_to_string(image)

print("RESULT:\n", out_result)                        
