import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def int_to_bits(num, bit_length):
    return [int(b) for b in format(num, f'0{bit_length}b')]

def str_to_bits(s):
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def embed_data(image, data_bits):
    height, width, channels = image.shape
    total_pixels = height * width * channels

    if len(data_bits) > total_pixels:
        raise ValueError("Data too large to embed in this image!")

    bit_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                if bit_index < len(data_bits):
                    image[row][col][channel] = (image[row][col][channel] & 254) | data_bits[bit_index]
                    bit_index += 1
                else:
                    return image
    return image

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, file_path)

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    entry_output.delete(0, tk.END)
    entry_output.insert(0, file_path)

def encrypt():
    img_path = entry_image.get().strip()
    output_path = entry_output.get().strip()
    secret_message = entry_message.get().strip()
    passcode = entry_passcode.get().strip()

    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Image file not found. Check and try again.")
        return

    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Could not load image. Check the file format.")
        return

    if not secret_message or not passcode:
        messagebox.showerror("Error", "Secret message and passcode are required!")
        return

    header_bits = []
    header_bits.extend(int_to_bits(len(passcode), 16))
    header_bits.extend(str_to_bits(passcode))
    header_bits.extend(int_to_bits(len(secret_message), 32))
    header_bits.extend(str_to_bits(secret_message))

    try:
        encoded_image = embed_data(image, header_bits)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    cv2.imwrite(output_path, encoded_image)
    messagebox.showinfo("Success", f"Message hidden in '{output_path}'")

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("550x350")
root.configure(bg="#2c3e50")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TEntry", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12, "bold"), background="#2c3e50", foreground="white")

frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

for i in range(5):
    frame.grid_rowconfigure(i, weight=1)
frame.grid_columnconfigure(1, weight=1)

ttk.Label(frame, text="Select Image:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
entry_image = ttk.Entry(frame, width=40)
entry_image.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
ttk.Button(frame, text="Browse", command=select_image).grid(row=0, column=2, padx=5)

ttk.Label(frame, text="Save As:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
entry_output = ttk.Entry(frame, width=40)
entry_output.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
ttk.Button(frame, text="Browse", command=save_image).grid(row=1, column=2, padx=5)

ttk.Label(frame, text="Secret Message:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
entry_message = ttk.Entry(frame, width=40)
entry_message.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

ttk.Label(frame, text="Passcode:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
entry_passcode = ttk.Entry(frame, width=40, show="*")
entry_passcode.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

ttk.Button(frame, text="Encrypt", command=encrypt).grid(row=4, column=1, pady=20)

root.mainloop()
