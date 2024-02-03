import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

class ResultPage:
    def __init__(self, master, main_master, cart_items):
        self.master = master
        self.master.title("Comparison Results")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        self.main_master = main_master
        self.cart_items = cart_items

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Background image
        self.original_image = Image.open("background/comparison.png")
        self.background_image = ImageTk.PhotoImage(self.original_image)
        self.background_label = ctk.CTkLabel(master, image=self.background_image, text="")
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")
        self.background_label.bind("<Configure>", self.resize_background_image)

        # Bind the <Configure> event of the master widget to the update_size function
        master.bind("<Configure>", self.update_size)

        # Frame for result items
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.pack(pady=(10, 10), padx=20, expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10))

        # Create a table
        self.tree = ttk.Treeview(self.result_frame, columns=("Product Name", "Category", "Store 1", "Store 2"), show="headings", height=10, style="Treeview")
        self.tree.pack(side="left", fill="both", expand=True)

        # Add horizontal scrollbar
        xscrollbar = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)

        # Set fixed width for columns
        self.tree.column("Product Name", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Store 1", width=75)
        self.tree.column("Store 2", width=75)

        # Set column headings
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Store 1", text="Store 1")
        self.tree.heading("Store 2", text="Store 2")

        # Display comparison results
        self.display_comparison_results()

        # Determine which store is cheaper
        #cheaper_store = "Store 1" if self.cart_items[0][2] < self.cart_items[0][3] else "Store 2"

        # Add a message label
        #message_text = f"You can shop at {cheaper_store} for a cheaper price."
        #self.message_label = ctk.CTkLabel(self.master, text=message_text, font=("Arial", 13, "bold"), fg_color="#DDE6D6", text_color="#FF6666")
        #self.message_label.pack(pady=(10, 50))

        # Return Button
        self.return_button = ctk.CTkButton(self.master, text="Return to Cart", command=self.return_to_cart, bg_color="#3D5919", fg_color="#3D5919")
        self.return_button.pack(pady=(10,40))

    def display_comparison_results(self):
        for item in self.cart_items:
            product_name, category, store1, store2 = item  # Extracting product details
            # Insert each product as a new row in the Treeview
            self.tree.insert("", "end", values=(product_name, category, store1, store2))

        # Calculate total prices
        total_price_store1 = sum(item[2] for item in self.cart_items)
        total_price_store2 = sum(item[3] for item in self.cart_items)

        # Insert total prices into the Treeview
        self.tree.insert("", "end", values=("Total", "", total_price_store1, total_price_store2), tags=("better_store",))

        # Determine the better store and highlight it
        better_store = "Store 1" if total_price_store1 < total_price_store2 else "Store 2"
        self.tree.tag_configure("better_store", background="pale green" if better_store == "Store 1" else "lightcoral")

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

    def return_to_cart(self):
        self.master.withdraw()  # Hide the current window
        self.main_master.deiconify()  # Show the cart window

if __name__ == "__main__":
    root = ctk.CTk()
    app = ResultPage(root, None, [("Gardenia White Bread", "Bread", 56.0, 59.5), ("Johnson's Baby Powder", "Baby Care", 33.75, 35.2)])
    root.mainloop()
