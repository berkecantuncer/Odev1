import numpy as np
from PIL import Image

def calculate_complexity(bit_plane_block):

    complexity = 0
    for i in range(8):
        for j in range(7):
            complexity += bit_plane_block[i][j] != bit_plane_block[i][j + 1]
            complexity += bit_plane_block[j][i] != bit_plane_block[j + 1][i]
    return complexity / 112

def message_to_bitstream(message):
    bits = ''.join(f'{ord(c):08b}' for c in message)
    return np.array([int(b) for b in bits], dtype=np.uint8)

def embed_bpcs(image_path, output_path, message, threshold=0.3):
    image = Image.open(image_path).convert('L')
    data = np.array(image)
    bit_planes = [(data >> i) & 1 for i in range(8)]

    msg_bits = message_to_bitstream(message + chr(0))
    bit_idx = 0

    for plane_index in reversed(range(1, 8)):
        plane = bit_planes[plane_index]
        for i in range(0, plane.shape[0] - 7, 8):
            for j in range(0, plane.shape[1] - 7, 8):
                block = plane[i:i+8, j:j+8]
                complexity = calculate_complexity(block)
                if complexity > threshold and bit_idx + 64 <= len(msg_bits):
                    new_block = msg_bits[bit_idx:bit_idx + 64].reshape((8, 8))
                    plane[i:i+8, j:j+8] = new_block
                    bit_idx += 64
                if bit_idx >= len(msg_bits):
                    break
            if bit_idx >= len(msg_bits):
                break
        if bit_idx >= len(msg_bits):
            break


    combined = sum((bit_planes[i] << i for i in range(8)))
    Image.fromarray(combined.astype(np.uint8)).save(output_path)
    print("Mesaj gömüldü.")

def extract_bpcs(image_path, threshold=0.3):
    image = Image.open(image_path).convert('L')
    data = np.array(image)
    bit_planes = [(data >> i) & 1 for i in range(8)]

    extracted_bits = []
    for plane_index in reversed(range(1, 8)):
        plane = bit_planes[plane_index]
        for i in range(0, plane.shape[0] - 7, 8):
            for j in range(0, plane.shape[1] - 7, 8):
                block = plane[i:i+8, j:j+8]
                complexity = calculate_complexity(block)
                if complexity > threshold:
                    extracted_bits.extend(block.flatten())


    chars = []
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(map(str, byte)), 2))
        if char == chr(0):
            break
        chars.append(char)
    return ''.join(chars)


if __name__ == "__main__":
    embed_bpcs("input_image.jpg", "bpcs_stego.png", "Gizli BPCS mesajı burada!")
    mesaj = extract_bpcs("bpcs_stego.png")
    print("Çıkarılan mesaj:", mesaj)
