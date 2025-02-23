import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk

def bits_to_int(bits):
    return int("".join(map(str, bits)), 2)

def bits_to_str(bits):
    return "".join(chr(bits_to_int(bits[i:i+8])) for i in range(0, len(bits), 8))

def extract_bits(image, num_bits):
    bits = []
    h, w, c = image.shape
    total_pixels = h * w * c
    if num_bits > total_pixels:
        raise ValueError("Not enough pixels in the image to extract the requested number of bits.")
    flat_image = image.flatten()
    for i in range(num_bits):
        bits.append(flat_image[i] & 1)
    return bits

def decrypt():
    img_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not img_path:
        return
    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Encrypted image not found!")
        return
    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load the image. Please check the file format.")
        return
    try:
        passcode_length_bits = extract_bits(image, 16)
        passcode_length = bits_to_int(passcode_length_bits)
        passcode_bits = extract_bits(image, 16 + passcode_length * 8)[16:]
        passcode = bits_to_str(passcode_bits)
        user_passcode = passcode_entry.get().strip()
        if user_passcode != passcode:
            messagebox.showerror("Error", "Incorrect passcode!")
            return
        message_length_bits = extract_bits(image, 16 + passcode_length * 8 + 32)[-32:]
        message_length = bits_to_int(message_length_bits)
        message_bits = extract_bits(image, 16 + passcode_length * 8 + 32 + message_length * 8)[-message_length * 8:]
        secret_message = bits_to_str(message_bits)
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, secret_message)
        output_text.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Image Decryption Tool")
root.geometry("500x400")
root.configure(bg="#2c3e50")

title_label = tk.Label(root, text="Decrypt Hidden Message", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
title_label.pack(pady=10)

passcode_label = tk.Label(root, text="Enter Passcode:", font=("Arial", 12), fg="white", bg="#2c3e50")
passcode_label.pack()

passcode_entry = ttk.Entry(root, show="*", font=("Arial", 12), width=30)
passcode_entry.pack(pady=5)

decrypt_button = ttk.Button(root, text="Select Image & Decrypt", command=decrypt)
decrypt_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, height=5, font=("Arial", 12), state=tk.DISABLED)
output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
