import customtkinter as ctk

class VendingMachineApp:
    def __init__(self, root):
        self.root = root
        self.center_window(600, 600)
        self.root.title("Custom Vending Machine")

        self.total_price = 0
        self.cart = {}
        self.selected_item = None
        self.selected_price = 0
        self.last_addition = None  # Store the last added item, price, and quantity

        self.items = {
            "Soda": (1.5, 10),
            "Chips": (2.0, 8),
            "Candy": (1.0, 15),
            "Water": (1.2, 20),
        }

        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f"{width}x{height}+{position_right}+{position_top}")

    def create_widgets(self):
        header_label = ctk.CTkLabel(self.root, text="Vending Machine", font=("Arial", 20, "bold"))
        header_label.pack(pady=10)

        self.cart_display = ctk.CTkLabel(self.root, text="Cart: Empty", font=("Arial", 14))
        self.cart_display.pack(pady=10)

        # Create a frame to hold item buttons horizontally
        items_frame = ctk.CTkFrame(self.root)
        items_frame.pack(pady=10)

        # Buttons for items arranged horizontally in grid with larger size
        col = 0  # Start from the first column
        for item, (price, _) in self.items.items():
            button = ctk.CTkButton(
                items_frame, text=f"{item}\n${price}",
                command=lambda item=item, price=price: self.select_item(item, price),
                width=150, height=75, font=("Arial", 14)  # Increased size
            )
            button.grid(row=0, column=col, padx=10)  # Position buttons in a row (horizontally)
            col += 1  # Move to the next column

        # Slider to choose quantity
        self.slider_label = ctk.CTkLabel(self.root, text="Select Quantity: 0", font=("Arial", 14))
        self.slider_label.pack(pady=10)

        self.quantity_slider = ctk.CTkSlider(self.root, from_=0, to=10, command=self.update_quantity)
        self.quantity_slider.pack(pady=10)

        # Add to Cart Button
        add_button = ctk.CTkButton(self.root, text="Add to Cart", command=self.add_to_cart, width=200, height=50, font=("Arial", 14))
        add_button.pack(pady=10)

        # Remove Last Addition Button
        remove_last_button = ctk.CTkButton(self.root, text="Remove Last Addition", command=self.remove_last_addition, width=200, height=50, font=("Arial", 14))
        remove_last_button.pack(pady=10)

        # Checkout Button
        checkout_button = ctk.CTkButton(self.root, text="Checkout", command=self.checkout, width=200, height=50, font=("Arial", 14))
        checkout_button.pack(pady=10)

        # Reset Button
        reset_button = ctk.CTkButton(self.root, text="Reset", command=self.reset, width=200, height=50, font=("Arial", 14))
        reset_button.pack(pady=10)

    def select_item(self, item, price):
        """Select an item and store its details."""
        self.selected_item = item
        self.selected_price = price
        self.slider_label.configure(text="Select Quantity: 0")
        self.quantity_slider.set(0)

    def update_quantity(self, value):
        """Update the quantity label when the slider is moved."""
        self.slider_label.configure(text=f"Select Quantity: {int(value)}")

    def add_to_cart(self):
        """Add selected item to the cart with the chosen quantity."""
        quantity = int(self.quantity_slider.get())
        if self.selected_item and quantity > 0:
            # Add to the cart
            self.cart[self.selected_item] = self.cart.get(self.selected_item, 0) + quantity
            self.total_price += self.selected_price * quantity

            # Save the last addition
            self.last_addition = (self.selected_item, self.selected_price, quantity)

            # Update cart display
            cart_items = "\n".join([f"{item}: {qty}" for item, qty in self.cart.items()])
            self.cart_display.configure(text=f"Cart:\n{cart_items}\nTotal Price: ${self.total_price:.2f}")
        else:
            self.cart_display.configure(text="Please select an item and a valid quantity.")

    def remove_last_addition(self):
        """Remove the last added item from the cart."""
        if self.last_addition:
            item, price, quantity = self.last_addition
            if item in self.cart:
                self.cart[item] -= quantity
                if self.cart[item] <= 0:
                    del self.cart[item]
                self.total_price -= price * quantity

            # Clear the last addition record
            self.last_addition = None

            # Update cart display
            if self.cart:
                cart_items = "\n".join([f"{item}: {qty}" for item, qty in self.cart.items()])
                self.cart_display.configure(text=f"Cart:\n{cart_items}\nTotal Price: ${self.total_price:.2f}")
            else:
                self.cart_display.configure(text="Cart: Empty")
        else:
            self.cart_display.configure(text="No item to remove.")

    def checkout(self):
        """Finalize the purchase."""
        if self.total_price == 0:
            self.cart_display.configure(text="Cart is empty. Add items to checkout.")
        else:
            self.cart_display.configure(text=f"Purchase Successful!\nTotal Paid: ${self.total_price:.2f}")
            self.cart.clear()
            self.total_price = 0

    def reset(self):
        """Reset the GUI."""
        self.cart.clear()
        self.total_price = 0
        self.selected_item = None
        self.selected_price = 0
        self.last_addition = None
        self.slider_label.configure(text="Select Quantity: 0")
        self.quantity_slider.set(0)
        self.cart_display.configure(text="Cart: Empty")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VendingMachineApp(root)
    root.mainloop()
