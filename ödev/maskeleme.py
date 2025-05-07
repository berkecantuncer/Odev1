import cv2
import numpy as np
import matplotlib.pyplot as plt


image = cv2.imread('input_image.jpg')


if image is None:
    print("Görüntü dosyası bulunamadı veya hatalı")
    exit()


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
edges = cv2.magnitude(sobelx, sobely)


gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)


median_blur = cv2.medianBlur(gray, 5)


plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap='gray')
plt.title('Orijinal Gri Görüntü')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title('Sobel Kenar Maskeleme')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(gaussian_blur, cmap='gray')
plt.title('Gaussian Filtreleme')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(median_blur, cmap='gray')
plt.title('Median Filtreleme')
plt.axis('off')

plt.tight_layout()
plt.show()
