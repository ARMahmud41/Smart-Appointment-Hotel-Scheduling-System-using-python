from tkinter import *
from PIL import Image, ImageTk
from customer import CustWin
from logout import LogoutWindow
from report import ReportWindow
from Room import RoomManagement
from Details import DetailsWin

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Appointment Hotel Scheduling System")
        self.root.geometry("1550x800+0+0")

        # Top Banner Image
        img1 = Image.open(r"E:\Photo\cover.jpg")
        img1 = img1.resize((1550, 140), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        lblimg = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        lblimg.place(x=0, y=0, width=1550, height=140)

        # Title Label
        lbl_title = Label(
            self.root,
            text="SMART APPOINTMENT HOTEL SCHEDULING SYSTEM",
            font=("times new roman", 30, "bold"),
            bg="black",
            fg="gold"
        )
        lbl_title.place(x=0, y=140, width=1550, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=610)

        # Menu Label
        lbl_menu = Label(
            main_frame,
            text="MENU",
            font=("times new roman", 20, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE
        )
        lbl_menu.place(x=0, y=0, width=230)

        # Button Frame
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE)
        btn_frame.place(x=0, y=35, width=228, height=300)

        # Menu Buttons
        Button(btn_frame, text="Customer", width=20, font=("times new roman", 14, "bold"),
               bg="black", fg="gold", bd=0, cursor="hand2", command=self.cust_details).grid(row=0, column=0, pady=5)
        Button(btn_frame, text="Room", width=20, font=("times new roman", 14, "bold"),
               bg="black", fg="gold", bd=0, cursor="hand2", command=self.room_details).grid(row=1, column=0, pady=5)
        Button(btn_frame, text="Details", width=20, font=("times new roman", 14, "bold"),
               bg="black", fg="gold", bd=0, cursor="hand2", command=self.details_window).grid(row=2, column=0, pady=5)
        Button(btn_frame, text="Report", width=20, font=("times new roman", 14, "bold"),
               bg="black", fg="gold", bd=0, cursor="hand2", command=self.report_window).grid(row=3, column=0, pady=5)
        Button(btn_frame, text="Logout", width=20, font=("times new roman", 14, "bold"),
               bg="black", fg="gold", bd=0, cursor="hand2", command=self.logout_window).grid(row=4, column=0, pady=5)

        # Right Side Image
        img3 = Image.open(r"E:\Photo\ph3.jpeg")
        img3 = img3.resize((1210, 490), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        lblimg1 = Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE)
        lblimg1.place(x=200, y=0, width=1210, height=490)

    def cust_details(self):
        new_window = Toplevel(self.root)
        CustWin(new_window)

    def room_details(self):
        new_window = Toplevel(self.root)
        RoomManagement(new_window)

    def details_window(self):
        new_window = Toplevel(self.root)
        DetailsWin(new_window)

    def report_window(self):
        new_window = Toplevel(self.root)
        ReportWindow(new_window)

    def logout_window(self):
        new_window = Toplevel(self.root)
        LogoutWindow(new_window, self.root)


if __name__ == "__main__":
    root = Tk()
    app = HotelManagementSystem(root)
    root.mainloop()
