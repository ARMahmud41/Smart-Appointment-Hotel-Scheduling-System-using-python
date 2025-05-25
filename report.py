from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class ReportWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reports")
        self.root.geometry("1000x600+250+100")
        self.root.config(bg="white")

        # Dropdown to select report
        lbl_title = Label(self.root, text="Hotel Report Section", font=("Arial", 20, "bold"), bg="black", fg="gold", pady=10)
        lbl_title.pack(fill=X)

        self.report_options = [
            "Customer Report",
            "Room Booking Report",
            "Billing Report",
            "Check-in Report",
            "Check-out Report",
            "Payment Report",
            "Occupancy Summary Report",
            "Revenue Report"
        ]
        self.selected_report = StringVar()
        self.selected_report.set(self.report_options[0])

        frame_top = Frame(self.root, bg="white")
        frame_top.pack(pady=20)

        Label(frame_top, text="Select Report:", font=("Arial", 14), bg="white").pack(side=LEFT, padx=5)
        report_menu = OptionMenu(frame_top, self.selected_report, *self.report_options)
        report_menu.config(font=("Arial", 12), width=30)
        report_menu.pack(side=LEFT, padx=10)

        Button(frame_top, text="Generate", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.generate_report).pack(side=LEFT, padx=10)

        # Treeview for displaying data
        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(fill=BOTH, expand=1, padx=20, pady=10)

        self.scroll_x = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)
        self.report_table = ttk.Treeview(self.tree_frame, xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.config(command=self.report_table.xview)
        self.scroll_y.config(command=self.report_table.yview)
        self.report_table.pack(fill=BOTH, expand=1)

    def generate_report(self):
        report_name = self.selected_report.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Enter your password
                database="hotel"
            )
            cursor = conn.cursor()

            queries = {
                "Customer Report": "SELECT ref, name, room_no, room_type, checkin_date, checkout_date, mobile, email, nationality, id_number FROM customer;",
                "Room Booking Report": "SELECT room_no, room_type, status, checkin_date, checkout_date, name FROM bookings INNER JOIN customer ON bookings.customer_id = customer.id;",
                "Billing Report": "SELECT invoice_id, name, room_no, total_amount, payment_status, payment_method, bill_date FROM bills INNER JOIN customer ON bills.customer_id = customer.id;",
                "Check-in Report": "SELECT name, room_no, checkin_date FROM bookings INNER JOIN customer ON bookings.customer_id = customer.id WHERE checkin_date = CURDATE();",
                "Check-out Report": "SELECT name, room_no, checkout_date FROM bookings INNER JOIN customer ON bookings.customer_id = customer.id WHERE checkout_date = CURDATE();",
                "Payment Report": "SELECT bill_id, name, amount, payment_method, payment_date FROM payments INNER JOIN customer ON payments.customer_id = customer.id;",
                "Occupancy Summary Report": "SELECT COUNT(*) AS total_rooms, SUM(CASE WHEN status='Occupied' THEN 1 ELSE 0 END) AS occupied_rooms, SUM(CASE WHEN status='Available' THEN 1 ELSE 0 END) AS available_rooms FROM rooms;",
                "Revenue Report": "SELECT DATE(bill_date) as date, SUM(total_amount) as total_revenue FROM bills GROUP BY DATE(bill_date) ORDER BY date DESC;"
            }

            cursor.execute(queries[report_name])
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.report_table.delete(*self.report_table.get_children())
            self.report_table["columns"] = columns
            self.report_table["show"] = "headings"

            for col in columns:
                self.report_table.heading(col, text=col)
                self.report_table.column(col, width=120)

            for row in rows:
                self.report_table.insert("", END, values=row)

            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch report:\n{e}")

if __name__ == "__main__":
    root = Tk()
    app = ReportWindow(root)
    root.mainloop()
