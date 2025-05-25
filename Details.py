from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class DetailsWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Booking Details")
        self.root.geometry("1000x600+200+100")

        # Variables
        self.var_booking_id = StringVar()
        self.var_cust_ref = StringVar()
        self.var_room_no = StringVar()
        self.var_check_in = StringVar()
        self.var_check_out = StringVar()
        self.var_duration = StringVar()
        self.var_services = StringVar()
        self.var_payment = StringVar()

        # Title Label
        title = Label(self.root, text="Booking Details", font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        title.pack(side=TOP, fill=X)

        # Form Frame
        form_frame = Frame(self.root, bd=4, relief=RIDGE, padx=10, pady=10)
        form_frame.place(x=10, y=60, width=450, height=500)

        # Form Labels and Entry Widgets
        Label(form_frame, text="Booking ID", font=("arial", 12)).grid(row=0, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_booking_id, font=("arial", 12)).grid(row=0, column=1, pady=5)

        Label(form_frame, text="Customer Ref", font=("arial", 12)).grid(row=1, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_cust_ref, font=("arial", 12)).grid(row=1, column=1, pady=5)

        Label(form_frame, text="Room No", font=("arial", 12)).grid(row=2, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_room_no, font=("arial", 12)).grid(row=2, column=1, pady=5)

        Label(form_frame, text="Check-In", font=("arial", 12)).grid(row=3, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_check_in, font=("arial", 12)).grid(row=3, column=1, pady=5)

        Label(form_frame, text="Check-Out", font=("arial", 12)).grid(row=4, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_check_out, font=("arial", 12)).grid(row=4, column=1, pady=5)

        Label(form_frame, text="Duration", font=("arial", 12)).grid(row=5, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_duration, font=("arial", 12)).grid(row=5, column=1, pady=5)

        Label(form_frame, text="Services", font=("arial", 12)).grid(row=6, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_services, font=("arial", 12)).grid(row=6, column=1, pady=5)

        Label(form_frame, text="Payment", font=("arial", 12)).grid(row=7, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_payment, font=("arial", 12)).grid(row=7, column=1, pady=5)

        Label(form_frame, text="Special Requests", font=("arial", 12)).grid(row=8, column=0, sticky=W, pady=5)
        self.txt_requests = Text(form_frame, width=22, height=4, font=("arial", 12))
        self.txt_requests.grid(row=8, column=1, pady=5)

        # Buttons Frame
        btn_frame = Frame(form_frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=15)

        Button(btn_frame, text="Add", command=self.add_booking, width=10, bg="black", fg="gold").grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Update", command=self.update_booking, width=10, bg="black", fg="gold").grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Delete", command=self.delete_booking, width=10, bg="black", fg="gold").grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Reset", command=self.reset_fields, width=10, bg="black", fg="gold").grid(row=0, column=3, padx=5)

        # Table Frame
        table_frame = Frame(self.root, bd=4, relief=RIDGE)
        table_frame.place(x=470, y=60, width=510, height=500)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.booking_table = ttk.Treeview(
            table_frame,
            columns=("booking_id", "cust_ref", "room_no", "check_in", "check_out", "duration", "services", "payment", "requests"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.booking_table.xview)
        scroll_y.config(command=self.booking_table.yview)

        for col in self.booking_table["columns"]:
            self.booking_table.heading(col, text=col.replace("_", " ").title())
            self.booking_table.column(col, width=100)

        self.booking_table["show"] = "headings"
        self.booking_table.pack(fill=BOTH, expand=1)
        self.booking_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def connect_db(self):
        return mysql.connector.connect(host="localhost", user="root", password="", database="hotel")

    def add_booking(self):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO booking VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_booking_id.get(),
                    self.var_cust_ref.get(),
                    self.var_room_no.get(),
                    self.var_check_in.get(),
                    self.var_check_out.get(),
                    self.var_duration.get(),
                    self.var_services.get(),
                    self.var_payment.get(),
                    self.txt_requests.get("1.0", END).strip()
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Booking added successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add booking\n{e}", parent=self.root)

    def fetch_data(self):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM booking")
            rows = cur.fetchall()
            if rows:
                self.booking_table.delete(*self.booking_table.get_children())
                for row in rows:
                    self.booking_table.insert("", END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data\n{e}", parent=self.root)

    def get_cursor(self, event=""):
        selected = self.booking_table.focus()
        content = self.booking_table.item(selected)
        row = content.get("values", [])
        if row:
            self.var_booking_id.set(row[0])
            self.var_cust_ref.set(row[1])
            self.var_room_no.set(row[2])
            self.var_check_in.set(row[3])
            self.var_check_out.set(row[4])
            self.var_duration.set(row[5])
            self.var_services.set(row[6])
            self.var_payment.set(row[7])
            self.txt_requests.delete("1.0", END)
            self.txt_requests.insert(END, row[8])

    def update_booking(self):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE booking SET 
                    cust_ref=%s, room_no=%s, check_in=%s, check_out=%s, duration=%s, 
                    services=%s, payment=%s, requests=%s 
                WHERE booking_id=%s
            """, (
                self.var_cust_ref.get(),
                self.var_room_no.get(),
                self.var_check_in.get(),
                self.var_check_out.get(),
                self.var_duration.get(),
                self.var_services.get(),
                self.var_payment.get(),
                self.txt_requests.get("1.0", END).strip(),
                self.var_booking_id.get()
            ))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Booking updated successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update booking\n{e}", parent=self.root)

    def delete_booking(self):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM booking WHERE booking_id=%s", (self.var_booking_id.get(),))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.reset_fields()
            messagebox.showinfo("Success", "Booking deleted successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete booking\n{e}", parent=self.root)

    def reset_fields(self):
        self.var_booking_id.set("")
        self.var_cust_ref.set("")
        self.var_room_no.set("")
        self.var_check_in.set("")
        self.var_check_out.set("")
        self.var_duration.set("")
        self.var_services.set("")
        self.var_payment.set("")
        self.txt_requests.delete("1.0", END)


if __name__ == "__main__":
    root = Tk()
    app = DetailsWin(root)
    root.mainloop()
