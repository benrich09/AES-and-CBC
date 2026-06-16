from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

# ========================= CONFIG =========================
INPUT_IMAGE = "input.png"
ECB_OUTPUT = "ecb_encrypted.png"
CBC_OUTPUT = "cbc_encrypted.png"

# Step 1: Load and prepare image
img = Image.open(INPUT_IMAGE).convert("RGB")
data = np.array(img)
plaintext = data.tobytes()

print(f"Original image shape: {data.shape}, bytes: {len(plaintext)}")

# Step 2: Key generation (128-bit AES)
key = get_random_bytes(16)  # AES-128
print(f"AES Key (hex): {key.hex()}")

# Step 3: ECB Mode (Insecure for patterned data)
cipher_ecb = AES.new(key, AES.MODE_ECB)
padded_plaintext = pad(plaintext, AES.block_size)
ciphertext_ecb = cipher_ecb.encrypt(padded_plaintext)

# Step 4: CBC Mode (Secure)
iv = get_random_bytes(16)
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
ciphertext_cbc = cipher_cbc.encrypt(padded_plaintext)

print(f"IV (CBC): {iv.hex()}")

# Step 5: Save encrypted results as images
def save_encrypted_image(ciphertext, filename, original_shape, original_len):
    # Take only original data length (ignore padding for visualization)
    cipher_data = ciphertext[:original_len]
    cipher_array = np.frombuffer(cipher_data, dtype=np.uint8)
    # Reshape - may have slight padding artifact at end
    try:
        cipher_array = cipher_array.reshape(original_shape)
    except ValueError:
        # Fallback: truncate to fit
        target_size = original_shape[0] * original_shape[1] * original_shape[2]
        cipher_array = cipher_array[:target_size].reshape(original_shape)
    Image.fromarray(cipher_array).save(filename)
    print(f"Saved: {filename}")

save_encrypted_image(ciphertext_ecb, ECB_OUTPUT, data.shape, len(plaintext))
save_encrypted_image(ciphertext_cbc, CBC_OUTPUT, data.shape, len(plaintext))

print("\n=== LAB COMPLETE ===")
print("Compare: input.png vs ecb_encrypted.png vs cbc_encrypted.png")