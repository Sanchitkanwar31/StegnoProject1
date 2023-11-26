from PIL import Image

# Function to encode text into an image
def encode_image(image_path, text, output_path):
    img = Image.open(image_path)
    width, height = img.size
    encoded_img = img.copy()
    #data = text.encode()
    data =''.join(format(ord(char), '08b') for char in text) #this will convert the acii secret messagevto 08b(format specifier) bit binary value 

    index = 0
    for row in range(height):
        for col in range(width):
            if index < len(data):
                pixel = list(img.getpixel((col, row)))
                for color_channel in range(3):  # R, G, B channels
                    if index < len(data):
                        pixel[color_channel] = pixel[color_channel] & 254 | int(data[index])
                        index += 1
                encoded_img.putpixel((col, row), tuple(pixel))
            else:
                break

    encoded_img.save(output_path)

# Function to decode text from an image
def decode_image(encoded_image_path):
    encoded_img = Image.open(encoded_image_path)
    width, height = encoded_img.size
    data = []

    for row in range(height):
        for col in range(width):
            pixel = list(encoded_img.getpixel((col, row)))
            for color_channel in range(3):  # R, G, B
                data.append(pixel[color_channel] & 1) #this will help in taking out lsb value

    decoded_text = []
    for i in range(0, len(data), 8):
        byte = data[i:i+8]
        decoded_text.append(chr(int(''.join(map(str, byte)), 2)))

    return ''.join(decoded_text)
    #return decoded_text

# Example usage
if __name__ == "__main__":
    # Encode text into an image
    encode_image("Screenshot 2023-11-05 004803.png", " Hello! is a secret message", "encoded_image.png")

    # Decode text from the encoded image
    decoded_text = decode_image("encoded_image.png")
    print("Decoded Text: ", decoded_text)
