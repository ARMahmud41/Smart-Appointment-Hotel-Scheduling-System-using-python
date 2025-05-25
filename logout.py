from tkinter import *
from tkinter import messagebox
import subprocess
import sys

class LogoutWindow:
    def __init__(self, root, main_root):
        self.root = root                # Logout confirmation window
        self.main_root = main_root      # Main app window reference
        self.root.title("Logout")
        self.root.geometry("400x200+500+300")
        self.root.config(bg="white")

        lbl_msg = Label(self.root, text="Are you sure you want to logout?", font=("Arial", 14, "bold"), bg="white")
        lbl_msg.pack(pady=30)

        frame_buttons = Frame(self.root, bg="white")
        frame_buttons.pack()

        btn_yes = Button(frame_buttons, text="Yes", font=("Arial", 12), bg="black", fg="white", width=10, command=self.logout)
        btn_yes.grid(row=0, column=0, padx=10)

        btn_no = Button(frame_buttons, text="No", font=("Arial", 12), bg="gray", fg="white", width=10, command=self.root.destroy)
        btn_no.grid(row=0, column=1, padx=10)

    def logout(self):
        # Close both logout window and main app window
        self.root.destroy()       # close logout confirmation window
        self.main_root.destroy()  # close main app window

        try:
            # Optionally open login.py again
            python = sys.executable
            subprocess.Popen([python, "login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open login window:\n{e}")

if __name__ == "__main__":
    main_root = Tk()             # Simulate main app window
    logout_win = Toplevel(main_root)
    app = LogoutWindow(logout_win, main_root)
    main_root.mainloop()
