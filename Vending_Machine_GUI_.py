import customtkinter as ctk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk

class VendingMachineApp:
    def __init__(self, root):
        self.root = root
        self.center_window(600, 600)
        self.root.title("Vending Machine")

        self.total_price = 0
        self.cart = {}
        self.selected_item = None
        self.selected_price = 0

        self.items = {
           "Soda": (1.5, 10),
            "Chips": (2.0, 8),
            "Candy": (1.0, 15),
            "Water": (1.2, 20),
            "Juice": (2.5, 12),
            "Cookies": (3.0, 5),
            "Nuts": (2.8, 7),
            "Gum": (0.5, 50),
            "Coffee": (3.5, 10),
            "Tea": (3.0, 8),
            "Granola Bar": (1.8, 20),
            "Crackers": (1.7, 15),
            "Milk": (1.6, 10),
            "Energy Drink": (2.9, 10),
            "Popcorn": (2.3, 12),
            "Pretzels": (2.1, 15),
            "Protein Bar": (2.4, 8),
            "Biscuits": (1.9, 18),
            "Yogurt": (3.2, 6),
            "Chewing Gum": (0.8, 30),
            "Ice Cream": (3.6, 5),
            "Mints": (0.7, 40),
            "Chocolates": (1.2, 25),
            "Smoothie": (3.8, 7),
            "Seltzer": (2.2, 15),
            "Choco Bar": (2.1, 10),
            "Cereal Bar": (2.0, 12),
            "Fruit Snacks": (1.5, 20),
            "Brownie": (3.3, 10),
            "Cupcake": (3.4, 8),
            "Trail Mix": (2.7, 15),
            "Rice Cake": (1.3, 18),
        }

        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f"{width}x{height}+{position_right}+{position_top}")

    def create_widgets(self):
        header_label = ctk.CTkLabel(self.root, text="Welcome to The Vending Machine", font=("Arial", 40, "bold"))
        header_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a frame for the item buttons
        items_frame = ctk.CTkFrame(self.root, width=400, height=400)
        items_frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        # Configure grid layout for items_frame
        for col in range(4):  # 4 columns
            items_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        # Add image for "Soda" button
        
            img_path = r"C:\Users\HpZBOOK\Desktop\Python\can.png"  # Update with your Soda image path
            soda_image = Image.open(img_path).resize((100, 100))  # Resize the image as needed
            soda_photo = ImageTk.PhotoImage(soda_image)

            soda_button = ctk.CTkButton(
                items_frame,
                text="",  # No text
                image=soda_photo,
                command=lambda: self.select_item("Soda", self.items["Soda"][0]),
                width=100, height=100
            )
            soda_button.image = soda_photo  # Keep a reference to avoid garbage collection
            soda_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
       
        # Add remaining buttons
        row, col = 0, 1
        for item, (price, _) in self.items.items():
            if item == "Soda":
                continue  # Skip the Soda button since it already has an image

            button = ctk.CTkButton(
                items_frame,
                text=f"{item}\n${price}",
                command=lambda item=item, price=price: self.select_item(item, price),
                font=("Arial", 20), width=20, height=15
            )
            button.grid(row=row, column=col, padx=5, pady=10, sticky="ew")
            col += 1
            if col >= 4:  # Move to the next row after 4 columns
                col = 0
                row += 1

        # Create a frame for the cart, quantity selection, and checkout buttons below the items
        cart_frame = ctk.CTkFrame(self.root, width=150, height=300)
        cart_frame.grid(row=1, column=1, pady=120, padx=5, sticky="nsew")

    
        # Configure the grid in cart_frame to expand properly
        cart_frame.grid_columnconfigure(0, weight=1)  # Make the column expand to fill the space

        self.slider_label = ctk.CTkLabel(cart_frame, text="Select Quantity: 0", font=("Arial", 16))
        self.slider_label.grid(row=1, column=0, pady=10, sticky="nsew")

        self.quantity_slider = ctk.CTkSlider(cart_frame, from_=0, to=30, command=self.update_quantity)
        self.quantity_slider.grid(row=2, column=0, pady=5, sticky="nsew")

        # Center the buttons inside the cart frame
        add_button = ctk.CTkButton(cart_frame, text="Add to Cart", command=self.add_to_cart, width=200, height=70, font=("Arial", 18))  # Restored button size
        add_button.grid(row=3, column=0, pady=10, sticky="nsew")

        remove_last_button = ctk.CTkButton(cart_frame, text="Remove Last", command=self.remove_last_addition, width=200, height=70, font=("Arial", 18))  # Restored button size
        remove_last_button.grid(row=4, column=0, pady=10, sticky="nsew")

        checkout_button = ctk.CTkButton(cart_frame, text="Checkout", command=self.checkout, width=200, height=70, font=("Arial", 18))  # Restored button size
        checkout_button.grid(row=5, column=0, pady=10, sticky="nsew")

        reset_button = ctk.CTkButton(cart_frame, text="Reset", command=self.reset, width=200, height=70, font=("Arial", 18))  # Restored button size
        reset_button.grid(row=6, column=0, pady=10, sticky="nsew")

        self.selected_items_frame = ctk.CTkFrame(self.root, width=300, height=300)
        self.selected_items_frame.grid(row=1, column=2, pady=5, padx=5, sticky="nsew")

        self.selected_items_list = ctk.CTkLabel(self.selected_items_frame, text="", font=("Arial", 16))  # Restored font size
        self.selected_items_list.grid(row=0, column=0, pady=5, sticky="nsew")

        # Grid row/column configuration
        self.root.grid_rowconfigure(0, weight=0)  # Row 0 for header
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 for frames
        self.root.grid_columnconfigure(0, weight=1)  # Column 0 for items_frame
        self.root.grid_columnconfigure(1, weight=1)  # Column 1 for cart_frame
        self.root.grid_columnconfigure(2, weight=1)  # Column 2 for selected_items_frame
    def select_item(self, item, price):
        self.selected_item = item
        self.selected_price = price
        self.slider_label.configure(text="Select Quantity: 0")
        self.quantity_slider.set(0)

    def update_quantity(self, value):
        self.slider_label.configure(text=f"Select Quantity: {int(value)}")

    def add_to_cart(self):
        quantity = int(self.quantity_slider.get())
        if self.selected_item and quantity > 0:
            if self.selected_item in self.cart:
                current_qty = self.cart[self.selected_item][1]
                self.cart[self.selected_item] = (self.selected_price, current_qty + quantity)
            else:
                self.cart[self.selected_item] = (self.selected_price, quantity)

            self.total_price += self.selected_price * quantity
            selected_items = "\n".join([f"{item}: {qty} x ${price} = ${price * qty:.2f}" for item, (price, qty) in self.cart.items()])
            self.selected_items_list.configure(text=selected_items)
        else:
            self.selected_items_list.configure(text="Please select an item and a valid quantity.")

    def remove_last_addition(self):
        if self.cart:
            last_item = list(self.cart.keys())[-1]
            price, quantity = self.cart[last_item]
            self.total_price -= price * quantity
            del self.cart[last_item]
            selected_items = "\n".join([f"{item}: {qty} x ${price} = ${price * qty:.2f}" for item, (price, qty) in self.cart.items()])
            self.selected_items_list.configure(text=selected_items)
        else:
            self.selected_items_list.configure(text="Cart is empty.")

    def checkout(self):
        if self.total_price > 0:
            checkout_window = Toplevel(self.root)
            checkout_window.title("Checkout")
            checkout_window.geometry("400x700")

            total_label = ctk.CTkLabel(checkout_window, text=f"Total Price: ${self.total_price:.2f}", font=("Arial", 20))
            total_label.pack(pady=20)

            checkout_items_label = ctk.CTkLabel(checkout_window, text="Selected Items:\n", font=("Arial", 20))
            checkout_items_label.pack()

            checkout_items = "\n".join([f"{item}: {qty} x ${price} = ${price * qty:.2f}" for item, (price, qty) in self.cart.items()])
            items_label = ctk.CTkLabel(checkout_window, text=checkout_items, font=("Arial", 20))
            items_label.pack(pady=10)

            agree_button = ctk.CTkButton(checkout_window, text="Agree", command=self.complete_purchase, width=100, height=40, font=("Arial", 20))
            agree_button.pack(side="left", padx=20, pady=10)

            reject_button = ctk.CTkButton(checkout_window, text="Reject", command=self.reset, width=100, height=40, font=("Arial", 20))
            reject_button.pack(side="right", padx=20, pady=10)

    def complete_purchase(self):
        messagebox.showinfo("Purchase Completed", "Thank you for your purchase!")
        self.reset()

    def reset(self):
        self.cart = {}
        self.total_price = 0
        self.selected_item = None
        self.selected_price = 0
        self.selected_items_list.configure(text="")
        self.slider_label.configure(text="Select Quantity: 0")
        self.quantity_slider.set(0)


if __name__ == "__main__":
    root = ctk.CTk()
    app = VendingMachineApp(root)
    root.mainloop()
