import cv2
import numpy as np
import matplotlib.pyplot as plt


def plot_histogram(image):

    colors = ('b', 'g', 'r')
    plt.figure(figsize=(12, 6))
    for i, color in enumerate(colors):
        histogram = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histogram, color=color)
    plt.title('Histogram')
    plt.xlabel('Pixel Değeri')
    plt.ylabel('Frekans')
    plt.show()


def analyze_lsb(image):

    lsb_image = np.zeros_like(image[:, :, 0])

    for i in range(3):
        lsb_image += (image[:, :, i] & 1)

    lsb_count = np.sum(lsb_image)

    print(f"LSB bitlerinden sıfır olmayan değerlerin sayısı: {lsb_count}")

    return lsb_image


def steganalysis(image_path):

    image = cv2.imread(image_path)


    if image is None:
        print("Görüntü dosyası bulunamadı veya hatalı")
        return


    plot_histogram(image)


    lsb_image = analyze_lsb(image)


    plt.imshow(lsb_image, cmap='gray')
    plt.title('Görüntü LSB Analizi')
    plt.axis('off')
    plt.show()



if __name__ == "__main__":
    image_path = 'input_image.jpg'
    steganalysis(image_path)
