from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img_path = "rose.png"
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 1. Resize to 50%
h, w = img.shape[:2]
resized = cv2.resize(img, (w//2, h//2))

# 2. Rotate 30 degrees clockwise
center = (resized.shape[1]//2, resized.shape[0]//2)
M = cv2.getRotationMatrix2D(center, -30, 1.0)
rotated = cv2.warpAffine(resized, M, (resized.shape[1], resized.shape[0]))

# 3. Morphological transformation (Dilation example)
kernel = np.ones((5,5), np.uint8)
morph = cv2.dilate(rotated, kernel, iterations=1)

# Convert for plotting
resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
morph_rgb = cv2.cvtColor(morph, cv2.COLOR_BGR2RGB)

# Plot results
# plt.figure()
# plt.imshow(img_rgb)
# plt.title("Original")
# plt.axis('off')

# plt.figure()
# plt.imshow(resized_rgb)
# plt.title("Resized (50%)")
# plt.axis('off')

# plt.figure()
# plt.imshow(rotated_rgb)
# plt.title("Rotated (30 deg CW)")
# plt.axis('off')

plt.figure()
plt.imshow(morph_rgb)
plt.title("Morphological (Dilation)")
plt.axis('off')

plt.show()