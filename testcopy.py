import cv2
import numpy as np

# 이미지 읽기
img = cv2.imread('apples.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -------------------
# 1. Sobel Edge
# -------------------
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

sobel = cv2.magnitude(sobelx, sobely)
sobel = np.uint8(sobel)

# -------------------
# 2. Canny Edge
# -------------------
canny = cv2.Canny(gray, 100, 200)

# -------------------
# 3. Contour Detection
# -------------------
# threshold 먼저 수행
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (0,255,0), 2)

# -------------------
# 결과 저장
# -------------------
cv2.imwrite('sobel.jpg', sobel)
cv2.imwrite('canny.jpg', canny)
cv2.imwrite('contour.jpg', contour_img)

# 화면 출력
cv2.imshow('Original', img)
cv2.imshow('Sobel', sobel)
cv2.imshow('Canny', canny)
cv2.imshow('Contour', contour_img)

cv2.waitKey(0)
cv2.destroyAllWindows()