from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import mysql.connector


class CustWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

        # Variables
        self.var_ref = StringVar(value=str(random.randint(1000, 9999)))
        self.var_cust_name = StringVar()
        self.var_mother = StringVar()
        self.var_gender = StringVar(value="Male")
        self.var_mobile = StringVar()
        self.var_email = StringVar()
        self.var_nationality = StringVar()
        self.var_address = StringVar()
        self.var_id_number = StringVar()

        self.search_var = StringVar()

        # Title
        lbl_title = Label(self.root, text="ADD CUSTOMER DETAILS", font=("times new roman", 18, "bold"), bg="black", fg="gold")
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # Logo Image
        try:
            img1 = Image.open("E:/Photo/image.jpg")
            img1 = img1.resize((120, 50), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            lblimg = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
            lblimg.place(x=5, y=2, width=120, height=50)
        except Exception as e:
            print("Image load error:", e)

        # Customer Details Frame
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Customer Details", font=("times new roman", 12, "bold"))
        labelframeleft.place(x=5, y=50, width=425, height=490)

        # Entry Fields
        labels = ["Customer Ref", "Customer Name", "Mother Name", "Gender", "Mobile", "Email", "Nationality", "ID Number", "Address"]
        variables = [self.var_ref, self.var_cust_name, self.var_mother, self.var_gender, self.var_mobile,
                     self.var_email, self.var_nationality, self.var_id_number, self.var_address]
        for row, label_text in enumerate(labels):
            lbl = Label(labelframeleft, text=label_text, font=("times new roman", 12, "bold"), padx=2, pady=6)
            lbl.grid(row=row, column=0, sticky=W)

            if label_text == "Gender":
                combo = ttk.Combobox(labelframeleft, textvariable=self.var_gender, font=("arial", 12, "bold"), width=24, state="readonly")
                combo["value"] = ("Male", "Female", "Other")
                combo.current(0)
                combo.grid(row=row, column=1)
            else:
                entry = ttk.Entry(labelframeleft, textvariable=variables[row], width=22, font=("times new roman", 14, "bold"))
                if label_text == "Customer Ref":
                    entry.config(state="readonly")
                entry.grid(row=row, column=1)

        # Buttons
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=400, width=412, height=40)

        Button(btn_frame, text="ADD", command=self.add_data, font=("times new roman", 12, "bold"), bg="black", fg="gold", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE", command=self.update, font=("times new roman", 12, "bold"), bg="black", fg="gold", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE", command=self.delete, font=("times new roman", 12, "bold"), bg="black", fg="gold", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET", command=self.reset, font=("times new roman", 12, "bold"), bg="black", fg="gold", width=10).grid(row=0, column=3, padx=1)

        # Search Frame
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details And Search System", font=("arial", 12, "bold"))
        Table_Frame.place(x=435, y=50, width=860, height=490)

        Label(Table_Frame, text="Search By:", font=("arial", 12, "bold"), bg="red", fg="white").grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.combo_search = ttk.Combobox(Table_Frame, textvariable=self.search_var, font=("arial", 12, "bold"), width=27, state="readonly")
        self.combo_search["value"] = ("mobile", "ref")  # lowercase to match DB columns
        self.combo_search.current(0)
        self.combo_search.grid(row=0, column=1, padx=10)

        self.txt_search = ttk.Entry(Table_Frame, font=("arial", 13, "bold"), width=24)
        self.txt_search.grid(row=0, column=2, padx=2)

        Button(Table_Frame, text="Search", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, command=self.search).grid(row=0, column=3, padx=1)
        Button(Table_Frame, text="Show All", font=("arial", 11, "bold"), bg="black", fg="gold", width=18, command=self.show_all).grid(row=0, column=4, padx=1)

        # Table
        details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=50, width=850, height=350)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Cust_Details_Table = ttk.Treeview(
            details_table,
            columns=("ref", "name", "mother", "gender", "mobile", "email", "nationality", "idnumber", "address"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Cust_Details_Table.xview)
        scroll_y.config(command=self.Cust_Details_Table.yview)
        self.Cust_Details_Table.pack(fill=BOTH, expand=1)

        self.Cust_Details_Table["show"] = "headings"
        for col in self.Cust_Details_Table["columns"]:
            self.Cust_Details_Table.heading(col, text=col.title())
            self.Cust_Details_Table.column(col, width=100)

        self.Cust_Details_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.show_all()

    def add_data(self):
        if self.var_mobile.get() == "" or self.var_mother.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="WJ28@krhps",
                database="hotel_management"
            )
            my_cursor = conn.cursor()
            my_cursor.execute(
                "INSERT INTO customer (ref, name, mother, gender, mobile, email, nationality, id_number, address) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.var_ref.get(),
                    self.var_cust_name.get(),
                    self.var_mother.get(),
                    self.var_gender.get(),
                    self.var_mobile.get(),
                    self.var_email.get(),
                    self.var_nationality.get(),
                    self.var_id_number.get(),
                    self.var_address.get()
                )
            )
            conn.commit()
            self.show_all()
            conn.close()
            messagebox.showinfo("Success", "Customer has been added successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}", parent=self.root)

    def show_all(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="WJ28@krhps",
                database="hotel_management"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM customer")
            rows = my_cursor.fetchall()
            if rows:
                self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
                for row in rows:
                    self.Cust_Details_Table.insert("", "end", values=row)
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Failed to load data: {str(es)}", parent=self.root)

    def search(self):
        if self.search_var.get() == "" or self.txt_search.get() == "":
            messagebox.showerror("Error", "Please select a search criteria and enter the value", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="WJ28@krhps", database="hotel_management")
            my_cursor = conn.cursor()
            query = "SELECT * FROM customer WHERE " + str(self.search_var.get()) + " LIKE %s"
            val = ("%" + str(self.txt_search.get()) + "%",)
            my_cursor.execute(query, val)
            rows = my_cursor.fetchall()
            if rows:
                self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
                for row in rows:
                    self.Cust_Details_Table.insert("", "end", values=row)
            else:
                messagebox.showinfo("Info", "No matching record found", parent=self.root)
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Something went wrong: {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.Cust_Details_Table.focus()
        content = self.Cust_Details_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_ref.set(row[0])
            self.var_cust_name.set(row[1])
            self.var_mother.set(row[2])
            self.var_gender.set(row[3])
            self.var_mobile.set(row[4])
            self.var_email.set(row[5])
            self.var_nationality.set(row[6])
            self.var_id_number.set(row[7])
            self.var_address.set(row[8])

    def update(self):
        if self.var_mobile.get() == "":
            messagebox.showerror("Error", "Please enter mobile number", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="WJ28@krhps",
                    database="hotel_management"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("""
                    UPDATE customer SET 
                        name=%s,
                        mother=%s,
                        gender=%s,
                        mobile=%s,
                        email=%s,
                        nationality=%s,
                        id_number=%s,
                        address=%s
                    WHERE ref=%s
                """, (
                    self.var_cust_name.get(),
                    self.var_mother.get(),
                    self.var_gender.get(),
                    self.var_mobile.get(),
                    self.var_email.get(),
                    self.var_nationality.get(),
                    self.var_id_number.get(),
                    self.var_address.get(),
                    self.var_ref.get()
                ))

                conn.commit()
                conn.close()
                messagebox.showinfo("Update", "Customer details have been updated successfully", parent=self.root)
                self.show_all()

            except Exception as es:
                messagebox.showerror("Error", f"Something went wrong: {str(es)}", parent=self.root)

    def delete(self):
        if self.var_ref.get() == "":
            messagebox.showerror("Error", "Customer reference number is required", parent=self.root)
        else:
            try:
                delete_confirmation = messagebox.askyesno("Hotel Management System", "Do you really want to delete this customer?", parent=self.root)
                if delete_confirmation > 0:
                    conn = mysql.connector.connect(host="localhost", username="root", password="WJ28@krhps", database="hotel_management")
                    my_cursor = conn.cursor()
                    my_cursor.execute("DELETE FROM customer WHERE ref=%s", (self.var_ref.get(),))
                    conn.commit()
                    conn.close()
                    self.show_all()
                    self.reset()
                    messagebox.showinfo("Delete", "Customer deleted successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Something went wrong: {str(es)}", parent=self.root)

    def reset(self):
        self.var_ref.set(str(random.randint(1000, 9999)))
        self.var_cust_name.set("")
        self.var_mother.set("")
        self.var_gender.set("Male")
        self.var_mobile.set("")
        self.var_email.set("")
        self.var_nationality.set("")
        self.var_id_number.set("")
        self.var_address.set("")


if __name__ == "__main__":
    root = Tk()
    obj = CustWin(root)
    root.mainloop()
