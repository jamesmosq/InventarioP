import tkinter as tk
from tkinter import ttk, messagebox
from database.db_handler import DatabaseHandler
from utils import validate_float, validate_int, format_currency


class ProductGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de productos")
        self.master.geometry("600x400")  # Set window size to 600x400
        self.master.resizable(False, False)  # Make window non-resizable

        try:
            self.db = DatabaseHandler()
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudo conectar a la base de datos: {e}")
            self.master.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        # Create a main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid
        for i in range(6):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            main_frame.grid_rowconfigure(i, weight=1)

        # Input fields
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Brand:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.brand_entry = ttk.Entry(main_frame, width=30)
        self.brand_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Reference:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.reference_entry = ttk.Entry(main_frame, width=30)
        self.reference_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Price:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_entry = ttk.Entry(main_frame, width=30)
        self.price_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(main_frame, width=30)
        self.quantity_entry.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Buttons
        ttk.Button(main_frame, text="Agregar producto", command=self.add_product).grid(row=5, column=0, columnspan=3,
                                                                                  pady=20)
        ttk.Button(main_frame, text="Mostrar productos", command=self.show_products).grid(row=6, column=0, columnspan=3,
                                                                                      pady=10)

    def add_product(self):
        name = self.name_entry.get()
        brand = self.brand_entry.get()
        reference = self.reference_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if name and brand and reference and price and quantity:
            price = validate_float(price)
            quantity = validate_int(quantity)

            if price is not None and quantity is not None:
                try:
                    self.db.insert_product(name, brand, reference, price, quantity)
                    messagebox.showinfo("Success", "Producto agregado exitosamente!")
                    self.clear_entries()
                except Exception as e:
                    messagebox.showerror("Database Error", f"No se pudo agregar producción: {e}")
            else:
                messagebox.showerror("Error", "Precio o cantidad no válidos!")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios!")

    def show_products(self):
        try:
            products = self.db.get_all_products()
            if products:
                product_window = tk.Toplevel(self.master)
                product_window.title("Lista de productos")
                product_window.geometry("800x400")  # Set size for product list window

                tree = ttk.Treeview(product_window, columns=("ID", "Name", "Brand", "Reference", "Price", "Quantity"),
                                    show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Name", text="Name")
                tree.heading("Brand", text="Brand")
                tree.heading("Reference", text="Reference")
                tree.heading("Price", text="Price")
                tree.heading("Quantity", text="Quantity")

                # Set column widths
                tree.column("ID", width=50)
                tree.column("Name", width=150)
                tree.column("Brand", width=150)
                tree.column("Reference", width=150)
                tree.column("Price", width=100)
                tree.column("Quantity", width=100)

                for product in products:
                    formatted_product = list(product)
                    formatted_product[4] = format_currency(product[4])  # Format price
                    tree.insert("", "end", values=formatted_product)

                tree.pack(expand=True, fill='both', padx=10, pady=10)

                # Add scrollbar
                scrollbar = ttk.Scrollbar(product_window, orient="vertical", command=tree.yview)
                scrollbar.pack(side='right', fill='y')
                tree.configure(yscrollcommand=scrollbar.set)
            else:
                messagebox.showinfo("Info", "No se encontraron productos!")
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudieron recuperar los productos: {e}")

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.brand_entry.delete(0, 'end')
        self.reference_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')

    def run(self):
        self.master.mainloop()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()