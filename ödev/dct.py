import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.fftpack import dct, idct

def apply_block_dct(img_array):
    height, width = img_array.shape
    dct_output = np.zeros_like(img_array, dtype=float)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = img_array[i:i + 8, j:j + 8]
            block_dct = dct(dct(np.transpose(block), norm='ortho').T, norm='ortho')
            dct_output[i:i + 8, j:j + 8] = block_dct

    return dct_output

def compress_dct_blocks(dct_input, keep=4):
    height, width = dct_input.shape
    dct_compressed = np.zeros_like(dct_input)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_input[i:i + 8, j:j + 8]
            h, w = block.shape
            mask = np.zeros((h, w))
            mask[:min(keep, h), :min(keep, w)] = 1
            dct_compressed[i:i + h, j:j + w] = block * mask

    return dct_compressed


def apply_block_idct(dct_blocks):
    height, width = dct_blocks.shape
    idct_output = np.zeros_like(dct_blocks)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_blocks[i:i + 8, j:j + 8]
            block_idct = idct(idct(np.transpose(block), norm='ortho').T, norm='ortho')
            idct_output[i:i + 8, j:j + 8] = block_idct

    return np.clip(idct_output, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    image_path = "input_image.jpg"
    image_gray = Image.open(image_path).convert('L')
    image_array = np.array(image_gray)

    dct_full = apply_block_dct(image_array)
    dct_filtered = compress_dct_blocks(dct_full, keep=2)
    image_reconstructed = apply_block_idct(dct_filtered)


    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(image_array, cmap='gray')
    plt.title("Orijinal Görüntü")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(image_reconstructed, cmap='gray')
    plt.title("Sıkıştırılmış Görüntü (DCT 4x4)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()
