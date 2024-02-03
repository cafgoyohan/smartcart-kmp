import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from result_page import ResultPage

class CartPage:
    def __init__(self, master, main_master, added_products, update_callback):
        self.master = master
        self.master.title("My Cart")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        self.main_master = main_master
        self.cart_items = added_products
        self.update_callback = update_callback  # Callback function

        # Background image
        self.original_image = Image.open("background/cart.png")
        self.background_image = ImageTk.PhotoImage(self.original_image)
        self.background_label = ctk.CTkLabel(master, image=self.background_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1, anchor="nw")
        self.background_label.bind("<Configure>", self.resize_background_image)

        # Frame for cart items
        self.cart_frame = ctk.CTkFrame(self.master)
        self.cart_frame.pack(pady=(65, 10))

        # Cart Text widget
        self.cart_text = tk.Text(self.cart_frame, wrap="word", width=40, height=10, font=("TkDefaultFont.", 11))
        self.cart_text.pack(side=tk.LEFT)

        # Scrollbar for the cart_text widget
        self.scrollbar = ttk.Scrollbar(self.cart_frame, command=self.cart_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure cart_text to use the scrollbar
        self.cart_text['yscrollcommand'] = self.scrollbar.set

        # Compare Products Button
        self.compare_button = ctk.CTkButton(self.master, text="Compare Products", command=self.compare_products, bg_color="#DDE6D6", fg_color="#3D5919")
        self.compare_button.pack(pady=10)

        # Return Button
        self.return_button = ctk.CTkButton(self.master, text="Return to Search", command=self.return_to_search, bg_color="#DDE6D6", fg_color="#3D5919")
        self.return_button.pack(pady=10)

        # Display cart items
        self.display_cart_items()

    def resize_background_image(self, event):
        new_width = event.width
        new_height = event.height

        resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.configure(image=self.background_image)
    
    def display_cart_items(self):
        self.cart_text.delete(1.0, tk.END)  # Clear previous items
        for item in self.cart_items:
            product_name, category, *_ = item  # Extracting product name and category
            self.cart_text.insert(tk.END, f" {product_name} | {category}\n")

    def compare_products(self):
        self.master.withdraw()  # Hide the current window
        results_window = tk.Toplevel(self.master)
        ResultPage(results_window, self.main_master, self.cart_items)


    def return_to_search(self):
        self.master.destroy()  # Close the current window
        self.main_master.deiconify()  # Show the search window

if __name__ == "__main__":
    root = ctk.CTk()
    app = CartPage(root, None, [], lambda: None)
    root.mainloop()
