import customtkinter as ctk
from tkinter import Toplevel
from PIL import Image, ImageTk
from search_page import SearchPage
from view_page import ViewPage
from result_page import ResultPage
from pandas import read_excel

class SmartCart:
    def __init__(self, master):
        self.master = master
        self.master.title("SmartCart")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        # Read product dataset from excel file
        self.product_data = self.read_excel_data("Grocery_DataSet.xlsx")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Background image
        self.background_image = Image.open("background/SmartCart.png")
        self.width, self.height = self.master.winfo_width(), self.master.winfo_height()
        self.background_image = self.background_image.resize((self.width, self.height))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Label with background image
        self.label = ctk.CTkLabel(master, image=self.background_image, text="")
        self.label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        # Bind the <Configure> event of the master widget to the update_size function
        master.bind("<Configure>", self.update_size)

        # Buttons
        self.exit_button = ctk.CTkButton(master, text="Exit", command=master.destroy, fg_color="#3D5919", bg_color="#ABD788")
        self.exit_button.pack(side=ctk.BOTTOM, pady=30)

        self.search_button = ctk.CTkButton(master, text="Search Products", command=self.open_search_page, fg_color="#3D5919", bg_color="#A7C676")
        self.search_button.pack(side=ctk.BOTTOM, pady=10)

        self.view_button = ctk.CTkButton(master, text="Available Products", command=self.open_view_page, fg_color="#3D5919", bg_color="#A7C676")
        self.view_button.pack(side=ctk.BOTTOM, pady=10)

        
    def update_size(self, event):
        # Get the new size of the window
        self.width, self.height = event.width, event.height

        # Resize the image
        self.background_image = self.background_image.resize((self.width, self.height))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a new CTkLabel widget with the updated size
        new_label = ctk.CTkLabel(self.master, image=self.background_image)
        new_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        #Replace the old widget with the new one
        self.label.destroy()
        self.label = new_label


    def read_excel_data(self, file_path):
        # Read data from Excel file
        df = read_excel(file_path)
        # Convert DataFrame to a list of lists
        return df.values.tolist()

    def open_search_page(self):
        self.master.withdraw()  # Hide the current window
        search_window = Toplevel(self.master)
        search_window.geometry("400x600")
        search_window.resizable(False, False)
        SearchPage(search_window, self.master, self.product_data)

    def open_view_page(self):
        self.master.withdraw()
        view_window = Toplevel(self.master)
        view_window.geometry("400x600")  
        view_window.resizable(False, False)
        ViewPage(view_window, self.master, self.product_data)


    def open_result_page(self, search_page_instance):
        self.master.withdraw()
        result_window = Toplevel(self.master)
        ResultPage(result_window, self.master, search_page_instance, self.product_data)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SmartCart(root)
    root.mainloop()