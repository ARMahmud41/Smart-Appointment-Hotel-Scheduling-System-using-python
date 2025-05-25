import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import mysql.connector

class RoomManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Room Management")
        self.root.geometry("900x500+300+200")

        # Variables
        self.var_room_no = tk.StringVar()
        self.var_room_type = tk.StringVar()
        self.var_floor = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_search_by = tk.StringVar()
        self.var_search_txt = tk.StringVar()

        self.create_widgets()
        self.show_all_rooms()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="ROOM MANAGEMENT SYSTEM",
            font=("times new roman", 20, "bold"),
            bg="black",
            fg="gold"
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # Room Details Frame
        details_frame = ttk.LabelFrame(self.root, text="Room Details", padding=(10, 10))
        details_frame.place(x=10, y=50, width=400, height=420)

        tk.Label(details_frame, text="Room No:", font=("times new roman", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Entry(details_frame, textvariable=self.var_room_no, font=("times new roman", 12), width=20).grid(row=0, column=1, pady=6)

        tk.Label(details_frame, text="Room Type:", font=("times new roman", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=6)
        room_type_cb = ttk.Combobox(details_frame, textvariable=self.var_room_type, font=("times new roman", 12), width=18, state="readonly")
        room_type_cb['values'] = ("Single", "Double", "Suite", "Deluxe")
        room_type_cb.current(0)
        room_type_cb.grid(row=1, column=1, pady=6)

        tk.Label(details_frame, text="Floor:", font=("times new roman", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=6)
        floor_cb = ttk.Combobox(details_frame, textvariable=self.var_floor, font=("times new roman", 12), width=18, state="readonly")
        floor_cb['values'] = tuple(str(i) for i in range(1, 11))
        floor_cb.current(0)
        floor_cb.grid(row=2, column=1, pady=6)

        tk.Label(details_frame, text="Status:", font=("times new roman", 12, "bold")).grid(row=3, column=0, sticky=tk.W, pady=6)
        status_cb = ttk.Combobox(details_frame, textvariable=self.var_status, font=("times new roman", 12), width=18, state="readonly")
        status_cb['values'] = ("Available", "Occupied", "Maintenance")
        status_cb.current(0)
        status_cb.grid(row=3, column=1, pady=6)

        tk.Label(details_frame, text="Price per Night:", font=("times new roman", 12, "bold")).grid(row=4, column=0, sticky=tk.W, pady=6)
        ttk.Entry(details_frame, textvariable=self.var_price, font=("times new roman", 12), width=20).grid(row=4, column=1, pady=6)

        # Buttons
        btn_frame = ttk.Frame(details_frame)
        btn_frame.place(x=10, y=250, width=370, height=40)

        ttk.Button(btn_frame, text="Add", command=self.add_room, width=10).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_room, width=10).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_room, width=10).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_fields, width=10).grid(row=0, column=3, padx=5)

        # Search Frame
        search_frame = ttk.LabelFrame(self.root, text="Search Room", padding=(10, 10))
        search_frame.place(x=420, y=50, width=460, height=80)

        tk.Label(search_frame, text="Search By:", font=("times new roman", 12, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5)
        search_by_cb = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 12), width=15, state="readonly")
        search_by_cb['values'] = ("room_no", "room_type")
        search_by_cb.current(0)
        search_by_cb.grid(row=0, column=1, padx=5)

        ttk.Entry(search_frame, textvariable=self.var_search_txt, font=("times new roman", 12), width=20).grid(row=0, column=2, padx=5)

        ttk.Button(search_frame, text="Search", command=self.search_room, width=10).grid(row=0, column=3, padx=5)
        ttk.Button(search_frame, text="Show All", command=self.show_all_rooms, width=10).grid(row=0, column=4, padx=5)

        # Table Frame
        table_frame = ttk.Frame(self.root)
        table_frame.place(x=420, y=140, width=460, height=380)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.room_table = ttk.Treeview(
            table_frame,
            columns=("room_no", "room_type", "floor", "status", "price"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show="headings"
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("room_no", text="Room No")
        self.room_table.heading("room_type", text="Room Type")
        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("status", text="Status")
        self.room_table.heading("price", text="Price/Night")

        self.room_table.column("room_no", width=80)
        self.room_table.column("room_type", width=100)
        self.room_table.column("floor", width=80)
        self.room_table.column("status", width=100)
        self.room_table.column("price", width=80)

        self.room_table.pack(fill=tk.BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            username="root",
            password="WJ28@krhps",
            database="hotel_management"
        )

    def add_room(self):
        if not self.var_room_no.get() or not self.var_price.get():
            messagebox.showerror("Error", "Room number and price are required", parent=self.root)
            return
        try:
            price = float(self.var_price.get())
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM room WHERE room_no=%s", (self.var_room_no.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Room number already exists!", parent=self.root)
                conn.close()
                return

            cursor.execute(
                "INSERT INTO room (room_no, room_type, floor, status, price) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.var_room_no.get(),
                    self.var_room_type.get(),
                    self.var_floor.get(),
                    self.var_status.get(),
                    price
                )
            )
            conn.commit()
            conn.close()

            self.show_all_rooms()
            self.reset_fields()
            messagebox.showinfo("Success", "Room added successfully!", parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}", parent=self.root)

    def show_all_rooms(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM room")
            rows = cursor.fetchall()
            self.room_table.delete(*self.room_table.get_children())
            for row in rows:
                self.room_table.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch rooms: {e}", parent=self.root)

    def get_cursor(self, event=None):
        selected = self.room_table.focus()
        data = self.room_table.item(selected)
        row = data.get("values")
        if row:
            self.var_room_no.set(row[0])
            self.var_room_type.set(row[1])
            self.var_floor.set(row[2])
            self.var_status.set(row[3])
            self.var_price.set(row[4])

    def update_room(self):
        if not self.var_room_no.get():
            messagebox.showerror("Error", "Please enter room number to update", parent=self.root)
            return
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE room SET room_type=%s, floor=%s, status=%s, price=%s WHERE room_no=%s",
                (
                    self.var_room_type.get(),
                    self.var_floor.get(),
                    self.var_status.get(),
                    float(self.var_price.get()),
                    self.var_room_no.get()
                )
            )
            conn.commit()
            conn.close()
            self.show_all_rooms()
            self.reset_fields()
            messagebox.showinfo("Success", "Room updated successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update room: {e}", parent=self.root)

    def delete_room(self):
        if not self.var_room_no.get():
            messagebox.showerror("Error", "Please select a room to delete", parent=self.root)
            return
        try:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this room?", parent=self.root)
            if confirm:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM room WHERE room_no=%s", (self.var_room_no.get(),))
                conn.commit()
                conn.close()
                self.show_all_rooms()
                self.reset_fields()
                messagebox.showinfo("Success", "Room deleted successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete room: {e}", parent=self.root)

    def reset_fields(self):
        self.var_room_no.set("")
        self.var_room_type.set("Single")
        self.var_floor.set("1")
        self.var_status.set("Available")
        self.var_price.set("")
        self.var_search_by.set("room_no")
        self.var_search_txt.set("")

    def search_room(self):
        search_by = self.var_search_by.get()
        search_txt = self.var_search_txt.get()
        if not search_txt:
            messagebox.showerror("Error", "Please enter search text", parent=self.root)
            return
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = f"SELECT * FROM room WHERE {search_by} LIKE %s"
            cursor.execute(query, ('%' + search_txt + '%',))
            rows = cursor.fetchall()
            self.room_table.delete(*self.room_table.get_children())
            for row in rows:
                self.room_table.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}", parent=self.root)


def open_room_management():
    new_win = Toplevel()
    RoomManagement(new_win)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hotel Management System")
    root.geometry("400x200+500+300")

    btn_open_room_mgmt = tk.Button(root, text="Open Room Management", font=("times new roman", 14), command=open_room_management)
    btn_open_room_mgmt.pack(expand=True)

    root.mainloop()
