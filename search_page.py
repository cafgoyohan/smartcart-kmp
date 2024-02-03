import customtkinter as ctk
from tkinter import Toplevel
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from cart_page import CartPage

class SearchPage:
    def __init__(self, master, main_master, product_data):
        self.master = master
        self.master.title("Search Products")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        # Background image
        self.original_image = Image.open("background/search.png")
        self.background_image = ImageTk.PhotoImage(self.original_image)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.bind("<Configure>", self.resize_background_image)

        # Label with background image
        self.label = ctk.CTkLabel(master, image=self.background_image, text="")
        self.label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        # Bind the <Configure> event of the master widget to the update_size function
        master.bind("<Configure>", self.update_size)

        self.main_master = main_master  # Reference to the main window
        self.product_data = product_data
        self.added_products = set()  # To keep track of added products

        # Frame for search entry and button
        self.search_frame = ctk.CTkFrame(self.master, bg_color="#DDE6D6", fg_color="#DDE6D6")
        self.search_frame.pack(pady=(70, 10))

        # Entry widget for user input
        self.search_entry = ctk.CTkEntry(self.search_frame, bg_color="#DDE6D6", fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
        self.search_entry.pack(side=ctk.LEFT, padx=10, fill=ctk.X, expand=True)

        # Button to trigger search
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.perform_search, bg_color="#DDE6D6", fg_color="#3D5919", width=10, text_color="#DDE6D6")
        self.search_button.pack(side=ctk.RIGHT, padx=10)

        # Results Frame
        self.results_frame = ctk.CTkFrame(self.master)
        self.results_frame.pack(pady=10)

        # Results Text widget
        self.results_text = tk.Text(self.results_frame, wrap="word", width=40, height=10, font=("TkDefaultFont.", 11))
        self.results_text.pack(side=ctk.LEFT, padx=10, pady=5)

        # Scrollbar for the results_text
        self.scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Configure results_text to use the scrollbar
        self.results_text['yscrollcommand'] = self.scrollbar.set

        # View Cart Button
        self.view_cart_button = ctk.CTkButton(self.master, text="View My Cart", command=self.open_cart_page, bg_color="#DDE6D6", fg_color="#3D5919")
        self.view_cart_button.pack(pady=10)

        # Return Button
        self.return_button = ctk.CTkButton(self.master, text="Return to Main", command=self.return_to_main, bg_color="#DDE6D6", fg_color="#3D5919")
        self.return_button.pack(pady=10)

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
        self.label.destroy()
        self.label = new_label
    
    def perform_search(self):
        search_term = self.search_entry.get().lower()

        # Check if the search term matches any products
        results = [product for product in self.product_data if search_term in product[0].lower() or search_term in product[1].lower()]

        self.results_text.delete(1.0, tk.END)  # Clear previous results

        if not results:
            # No results found, display a message
            self.results_text.insert(tk.END, "Sorry, the product you searched is not available\n")
        else:
            for i, product in enumerate(results):
                # Each product result includes an "Add" button
                add_button = self.create_add_button(product)
                self.results_text.window_create(tk.END, window=add_button)
                self.results_text.insert(tk.END, f" {product[0]} ({product[1]})\n")

    def create_add_button(self, product):
        def add_callback(p=product):
            selected_product_tuple = tuple(p)

            if selected_product_tuple not in self.added_products:
                # Product is not in the cart, add it and update the button state and text
                self.added_products.add(selected_product_tuple)
                add_button.config(state=tk.DISABLED, text="Added")
                self.update_cart_display()

        add_button = ttk.Button(self.results_text, text="Add", command=add_callback)
        return add_button

    def add_product_to_cart(self, product, button=None):
        selected_product_tuple = tuple(product)

        if selected_product_tuple not in self.added_products:
            # Product is not in the cart, add it and update the button state and text
            self.added_products.add(selected_product_tuple)
            
            # If button is provided, disable it
            if button:
                button.config(state=tk.DISABLED, text="Added")
                self.update_cart_display()  # Call the method to update cart display

    def update_cart_display(self):
        # This method will be called from CartPage to update the cart display
        pass

    def open_cart_page(self):
        # Hide the current window
        self.master.withdraw()

        # Create a new Toplevel window for the cart
        cart_window = tk.Toplevel(self.master)
        cart_window.geometry("400x600")
        cart_window.resizable(False, False)

        # Create an instance of CartPage and pass the necessary parameters
        cart_page = CartPage(cart_window, self.master, self.added_products, self.update_cart_display)

        # Wait for the cart window to be closed
        cart_window.wait_window(cart_page.master)

    def return_to_main(self):
        self.master.destroy()  # Close the current window
        self.main_master.deiconify()  # Show the main window

if __name__ == "__main__":
    root = ctk.CTk()
    app = SearchPage(root, None, [])
    root.mainloop()
