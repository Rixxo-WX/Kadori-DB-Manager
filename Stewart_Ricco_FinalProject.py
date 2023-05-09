from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
from tkinter import ttk
import customtkinter
# This is a document based database not Relational!
import database


def onClose():
    msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                        icon="question", option_1="Cancsel", option_2="No", option_3="Yes")
    response = msg.get()

    if response == "Yes":

        app.destroy()
    else:
        print("Click 'Yes' to exit!")


class SideBarFrame(customtkinter.CTkFrame):
    def openAddEntry_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddEntryTopLevel(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def openUpdateEntry_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = UpdateEntryTopLevel(self)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def openSettings_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SettingsTopLevel(self)
        else:
            self.toplevel_window.focus()

    # Tkinter has an issue where it will not update the selected List properly, I have no idea how to fix this weird
    # bug :/
    def requestDbEntryDelete(self):
        selected_item = self.master.dbFrame.selected_values
        if selected_item:
            database.deleteEntry(selected_item[2])

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        buttonPadding = 20
        buttonFgColor = "grey"
        buttonHeight = 45
        buttonWidth = 180

        appLogo = customtkinter.CTkImage(light_image=Image.open("trans_logo.png"), size=(200, 100))

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Side Menu Logo | Disabled
        self.sideMenuLogo = customtkinter.CTkButton(self, image=appLogo, text="", fg_color="black", state="disabled")
        self.sideMenuLogo.grid(row=1, column=0, )

        # Side Menu Buttons
        self.testButton = customtkinter.CTkButton(master=self, text="Add Entry", height=buttonHeight, width=buttonWidth,
                                                  fg_color=buttonFgColor, command=self.openAddEntry_toplevel)
        self.testButton.grid(row=2, column=0, pady=(200, buttonPadding), padx=buttonPadding)

        self.testButton = customtkinter.CTkButton(master=self, text="Update Entry", height=buttonHeight,
                                                  width=buttonWidth, fg_color=buttonFgColor,
                                                  command=self.openUpdateEntry_toplevel)

        self.testButton.grid(row=3, column=0, pady=buttonPadding)

        self.testButton = customtkinter.CTkButton(master=self, text="Delete Entry", height=buttonHeight,
                                                  width=buttonWidth, fg_color=buttonFgColor,
                                                  command=self.requestDbEntryDelete)
        self.testButton.grid(row=4, column=0, pady=buttonPadding)

        self.toplevel_window = None


class dbFrame(customtkinter.CTkFrame):
    # A Useless argument must be given since self gives two arguments, this is a Python Tkinter issue, nothing I can
    # do C# is a better programming language |
    def selectDbItem(self, event):
        currentItem = self.dbTable.focus()
        self.selected_values = self.dbTable.item(currentItem)["values"]
        return self.selected_values

    def dbTableUpdate(self):
        dbTableList = database.getAllEntries()
        for entry in range(len(dbTableList)):
            self.dbTable.insert('', "end", values=dbTableList[entry])
            app.after(10000, self.dbTableConstantUpdate)

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.selected_values = None

        # DB Header
        self.dbName = customtkinter.CTkLabel(master=self, text="Kadori Simple DB", font=("Arial", 30))
        self.dbName.grid(row=0, column=0, padx=10)

        # DB Table
        columns = ('first_name', 'last_name', 'email', 'department', 'status')
        self.dbTable = ttk.Treeview(master=self, columns=columns, show='headings')

        self.after(1000, self.dbTableConstantUpdate)

        # Define Heading
        self.dbTable.heading("first_name", text="First Name")
        self.dbTable.heading("last_name", text="Last Name")
        self.dbTable.heading("email", text="Email")
        self.dbTable.heading("department", text="Department")
        self.dbTable.heading("status", text="Status")
        self.dbTable.bind("<ButtonRelease-1>", self.selectDbItem)

        # DB Table Grid
        self.dbTable.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)

        # Make TreeView load DB on app load
        dbTableList = database.getAllEntries()
        for entry in range(len(dbTableList)):
            self.dbTable.insert('', "end", values=dbTableList[entry])
        selected_item = self.dbTable.selection()

    def dbTableConstantUpdate(self):
        # Clear the existing items in the treeview
        self.dbTable.delete(*self.dbTable.get_children())

        # Add the new items from the database
        dbTableList = database.getAllEntries()
        for entry in range(len(dbTableList)):
            self.dbTable.insert('', "end", values=dbTableList[entry])

        # Call this function again after a second
        # Tkinter handles classes and objects poorly
        # TreeView also does not accept any-form of selection no matter
        # format I use, I can't fix this therefore this is the best option
        self.after(3000, self.dbTableConstantUpdate)


class AddDataEntryFrame(customtkinter.CTkFrame):
    def requestDbAddEntry(self):
        # This project
        firstName = self.fnameEntry.get().strip()
        lastName = self.lnameEntry.get().strip()
        email = self.emailEntry.get().strip()
        department = self.departmentEntry.get().strip()
        if firstName == "" or lastName == '':
            print("First and Last Name: ",firstName,lastName)
            msg = CTkMessagebox(title="Error", message="Please enter a First and Last Name",
                                icon="cancel", option_1="Okay")
            return
        # This can be cleaned up but Time over Optimization right now
        if "@" in email:
            database.addEntry(firstName, lastName, email, department)
            msg = CTkMessagebox(title="Success", message="Successfully Added Entry to Database", icon="check",
                                option_1="Okay")
            # Tkinter is horrible, No matter how I try to call a method from another class nothing works
            # This is an alternative solution to closing the top level window which simply blanks out the fields
            # To prevent the user from submitting the same information again.
            self.fnameEntry.delete(0, "end")
            self.lnameEntry.delete(0, "end")
            self.emailEntry.delete(0, "end")
            self.departmentEntry.delete(0, "end")
        elif email == " " or email == "" or "@" not in email:
            msg = CTkMessagebox(title="Error", message="Please enter a Valid Email",
                                icon="cancel", option_1="Okay")
        else:
            msg = CTkMessagebox(title="Error", message="Cannot connect to Database, Contact System Admin",
                                icon="cancel", option_1="Okay")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        x_padding = 10
        y_padding = 5

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Labels For Text Entry
        self.label = customtkinter.CTkLabel(master=self, text="Add Details")
        self.label.grid(row=0, column=1, padx=x_padding, pady=y_padding)

        self.fnameLabel = customtkinter.CTkLabel(master=self, text="First Name")
        self.fnameLabel.grid(row=1, column=0, padx=x_padding, pady=y_padding)

        self.lnameLabel = customtkinter.CTkLabel(master=self, text="Last Name")
        self.lnameLabel.grid(row=2, column=0, padx=x_padding, pady=y_padding)

        self.emaiLabel = customtkinter.CTkLabel(master=self, text="Email")
        self.emaiLabel.grid(row=3, column=0, padx=x_padding, pady=y_padding)

        self.departmentLabel = customtkinter.CTkLabel(master=self, text="Department")
        self.departmentLabel.grid(row=4, column=0, padx=x_padding, pady=y_padding)

        # Text Entry
        self.fnameEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.fnameEntry.grid(row=1, column=1)

        self.lnameEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.lnameEntry.grid(row=2, column=1)

        self.emailEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.emailEntry.grid(row=3, column=1)

        self.departmentEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.departmentEntry.grid(row=4, column=1)

        # Add Sumbit button
        self.sumbitButton = customtkinter.CTkButton(master=self, text="Submit", command=self.requestDbAddEntry)
        self.sumbitButton.grid(row=5, column=0, columnspan=2, pady=(30, 0))


class UpdateDataEntryFrame(customtkinter.CTkFrame):
    def requestDbpdateEntry(self):
        print("RequestDB Called")
        email = self.emailEntry.get().strip()
        department = self.departmentEntry.get().strip()
        status = self.statusUpdateCombo.get()
        if "@" in email:
            if department == "":
                database.updateEntry(email, 0, status)
                print("DB updateEntry Called - Status")
            else:
                database.updateEntry(email, department, status)
                print("DB updateEntry Called - Department")

        else:
            msg = CTkMessagebox(title="Error", message="Please enter a Valid Email",
                                icon="cancel", option_1="Okay")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        x_padding = 10
        y_padding = 5

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # Labels For Text Entry
        self.label = customtkinter.CTkLabel(master=self, text="Update Details")
        self.label.grid(row=0, column=1, padx=x_padding, pady=0)

        self.emaiLabel = customtkinter.CTkLabel(master=self, text="Entries Email")
        self.emaiLabel.grid(row=1, column=0, padx=x_padding, pady=(0, 50))

        self.departmentLabel = customtkinter.CTkLabel(master=self, text="Department")
        self.departmentLabel.grid(row=2, column=0, padx=x_padding, pady=y_padding)

        self.departmentLabel = customtkinter.CTkLabel(master=self, text="Status")
        self.departmentLabel.grid(row=3, column=0, padx=x_padding, pady=y_padding)

        # Text Entry
        self.emailEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.emailEntry.grid(row=1, column=1, pady=(0, 50))

        self.departmentEntry = customtkinter.CTkEntry(master=self, width=180, corner_radius=0)
        self.departmentEntry.grid(row=2, column=1)

        self.statusUpdateCombo = customtkinter.CTkComboBox(master=self, values=["Free", "Away", "Busy"],
                                                           corner_radius=0)
        self.statusUpdateCombo.grid(row=3, column=1)

        # Add Sumbit button
        self.sumbitButton = customtkinter.CTkButton(master=self, text="Update", command=self.requestDbpdateEntry)
        self.sumbitButton.grid(row=4, column=0, columnspan=2, pady=(10, 0))


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("1200x650")
        self.title("Kadori DB")
        self.minsize(1000, 650)
        customtkinter.set_appearance_mode("light")
        # Configure Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Side Menu
        self.sideBarFrame = SideBarFrame(master=self, fg_color="black")
        self.sideBarFrame.grid(row=0, column=0, sticky="nsew", rowspan=1)

        # DB Frame
        self.dbFrame = dbFrame(master=self)
        self.dbFrame.grid(row=0, column=1, sticky="nsew")

        self.toplevel_window = None


class AddEntryTopLevel(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Add Entry")
        self.geometry("400x300")
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.dataFrame = AddDataEntryFrame(master=self)
        self.dataFrame.grid(row=0, column=0, columnspan=1, sticky="nsew")


class UpdateEntryTopLevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Update Entry")
        self.geometry("400x240")
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.dataFrame = UpdateDataEntryFrame(master=self)
        self.dataFrame.grid(row=0, column=0, columnspan=1, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", onClose)
    timer = dbFrame(master=app)
    app.after(0, timer.update())
    app.mainloop()
