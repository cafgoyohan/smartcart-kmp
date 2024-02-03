import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk

class ViewPage:
    def __init__(self, master, main_master, product_data):
        self.master = master
        self.master.title("View Products")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        self.main_master = main_master

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Background image
        self.original_image = Image.open("background/list.png")
        self.background_image = ImageTk.PhotoImage(self.original_image)
        self.background_label = ctk.CTkLabel(master, image=self.background_image, text="")
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")
        self.background_label.bind("<Configure>", self.resize_background_image)

        # Bind the <Configure> event of the master widget to the update_size function
        master.bind("<Configure>", self.update_size)

        # Frame for product items
        self.product_frame = ctk.CTkFrame(self.master)
        self.product_frame.pack(pady=30, padx=30, expand=True, fill="both")

        # Product Text widget
        self.product_text = tk.Text(self.product_frame, wrap="word", width=40, height=10, font=("TkDefaultFont.", 11))
        self.product_text.pack(side=ctk.TOP, fill="both", expand=True)

        # Scrollbar for the product_text widget
        #self.scrollbar = ctk.CTkScrollbar(self.product_frame, command=self.product_text.yview)
        #self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Configure product_text to use the scrollbar
        #self.product_text['yscrollcommand'] = self.scrollbar.set

        # Return to Home Button
        self.return_home_button = ctk.CTkButton(self.master, text="Return to Home", command=self.return_to_home, fg_color="#3D5919", bg_color="#A7C676")
        self.return_home_button.pack(pady=(10, 40))

        # Display all products initially
        self.display_products(product_data)

    def resize_background_image(self, event):
        new_width = event.width
        new_height = event.height

        resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.configure(image=self.background_image)

    def update_size(self, event):
        # Get the new size of the window
        self.width, self.height = event.width, event.height

        # Resize the image
        self.background_image = self.background_image.resize((self.width, self.height))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a new CTkLabel widget with the updated size
        new_label = ctk.CTkLabel(self.master, image=self.background_image)
        new_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        # Replace the old widget with the new one
        self.background_label.destroy()
        self.background_label = new_label

    def display_products(self, product_list):
        self.product_text.delete(1.0, tk.END)  # Clear previous items
        for product in product_list:
            product_name, *_ = product  # Extracting product name
            self.product_text.insert(tk.END, f"{product_name}\n")

    def return_to_home(self):
        self.master.withdraw()  # Hide the current window
        self.main_master.deiconify()  # Show the SmartCart window

if __name__ == "__main__":
    root = ctk.CTk()
    app = ViewPage(root, None, [("Product A", "Category 1"), ("Product B", "Category 2"), ("Product C", "Category 1")])
    root.mainloop()
