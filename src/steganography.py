import numpy as np
from PIL import Image
from .encryption import AESCipher

class LSBSteganography:
    def __init__(self):
        self.delimiter = "$t3g0"
        
    def get_image_capacity(self, image_path):
        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            width, height = image.size
            max_bits = width * height * 3
            delimiter_bits = len(self.delimiter) * 8
            available_bits = max_bits - delimiter_bits - 32
            max_chars = available_bits // 8
            return max_chars
        except Exception as e:
            print(f"Error calculating capacity: {e}")
            return 0
    
    def text_to_binary(self, text):
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def embed_message(self, image_path, message, password, output_path):
        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            cipher = AESCipher(password)
            encrypted_message = cipher.encrypt(message)
            full_message = encrypted_message + self.delimiter
            binary_message = self.text_to_binary(full_message)
            
            if len(binary_message) > self.get_image_capacity(image_path) * 8:
                print("Error: Message too large for image capacity")
                return False
            
            img_array = np.array(image)
            flat_img = img_array.flatten()
            
            for i, bit in enumerate(binary_message):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            modified_img = flat_img.reshape(img_array.shape)
            result_image = Image.fromarray(modified_img.astype('uint8'))
            result_image.save(output_path, 'PNG')
            
            print(f"Message successfully hidden in {output_path}")
            return True
            
        except Exception as e:
            print(f"Error embedding message: {e}")
            return False
    
    def extract_message(self, image_path, password):
        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            flat_img = img_array.flatten()
            
            binary_message = ''
            for pixel in flat_img:
                binary_message += str(pixel & 1)
            
            extracted_text = self.binary_to_text(binary_message)
            
            if self.delimiter in extracted_text:
                encrypted_message = extracted_text.split(self.delimiter)[0]
                cipher = AESCipher(password)
                decrypted_message = cipher.decrypt(encrypted_message)
                return decrypted_message
            else:
                print("No hidden message found or wrong password")
                return None
                
        except Exception as e:
            print(f"Error extracting message: {e}")
            return None
