import tkinter as tk 
import calendar 
from tkcalendar import Calendar
import tkinter as tk
from tkinter import simpledialog , messagebox
import json 
from tkinter import Menu
from tkinter.colorchooser import askcolor
import os 
import sys 


def display_calendar(): #function for giving us a calendar 
    #let us crate a separate gui for the calendar object 
    fetch_year  = 2024 
    cal_content = calendar.calendar(fetch_year)  
    return cal_content

def load_data():
     # Read existing data from the JSON file
        try:
            with open("data.json", "r") as file:
                data = json.load(file) 
                return data 
        except (FileNotFoundError, json.JSONDecodeError):
            dates = []  # If file doesn't exist or is empty, start with an empty list
     

def create_event_btn():
    def on_ok():
        selected_date = cal.selection_get().strftime("%Y-%m-%d")  # Format date as string

        #loading the data here 
        data = load_data()

        # Append the new date
        if selected_date not in data["dates"]:
            data["dates"].append(selected_date)

        # Write the updated data back to the JSON file
        with open("data.json", "w") as file:
            json.dump(data , file, indent=4)

        print("Selected Date is:", selected_date)
        top.destroy()

    top = tk.Toplevel(gui_window)
    cal = Calendar(top, selectmode='day')
    cal.pack(fill="both", expand=True)

    ok_button = tk.Button(top, text="OK", command=on_ok)
    ok_button.pack()


def restart_script():
    """Restart the current script."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def Delete_event(event_date):
    #here we can ask for cofirmation are you sure you want to delete the page 

    # try:
    #     with open("data.json","r") as file:
    #         data = json.load(file)
    # except (FileNotFoundError, json.JSONDecodeError):
    #         print("File not found or empty.")
    #         return
    #loading the data here 
    data = load_data()
    date_lst = data["dates"]  #it is a list containing a list of all the dates  on which there is a  event 
    #deleting the date from the json file 
     # Check if the date exists and remove it
    if event_date in date_lst and len(date_lst) > 0:
        idx = date_lst.index(event_date)
        del date_lst[idx]
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    #well we have  to restart the page that seems to be only option 
    #So let us start here now 
    restart_script()

def add_notes(event_date):
    '''function for creating a textbox and a save button to store notes'''
    # Create a frame to hold the text box and the save button
    notes_frame = tk.Frame(master=gui_window)
    notes_frame.grid(row=0, column=1 , sticky= "nw")  # Adjust grid placement as needed

    # Create the text box within the notes frame
    box = tk.Text(master=notes_frame, width=20, height=20, background="yellow")
    box.grid(row=0, column=0, sticky="nsew")  # Grid it at the top of the frame
    box.insert(tk.END, "Event notes\n")

    # Function to save notes
    def save_notes():
        input_text = box.get(1.0, "end-1c")
        store_text_from_box(event_date , input_text)

    def close_view():
        notes_frame.destroy()

    # Creating a save button directly below the text box in the notes frame
    save_button = tk.Button(master = notes_frame , text="Save Notes" , command=save_notes)
    save_button.grid(row=1 , column=0 , sticky="ew")  # Grid it below the text box
    save_button = tk.Button(master = notes_frame , text="Close Window" , command=close_view)
    save_button.grid(row=2 , column=0 , sticky="ew")  # Grid it below the text box
    
    

    # Configure the frame to make the text box expand to fill the space
    notes_frame.grid_rowconfigure(0, weight=1)  # Allow the text box to expand vertically
    notes_frame.grid_columnconfigure(0, weight=1)  # Allow the text box to expand horizontally


def store_text_from_box(event_date , input_text):
    '''Function to retrieve and print text from the given Text widget'''
    # with open("data.json","r") as file:
    #         data = json.load(file)
    #loading the data here 
    data = load_data()
     
    data["notes"][event_date] = input_text
    with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

def view_event_notes(event_date):
    # with open("data.json" , "r") as file:
    #     data = json.load(file)
    data = load_data()
    notes_text  = data["notes"][event_date]
    notes_frame = tk.Frame(master=gui_window)
    notes_frame.grid(row=0, column=1 , sticky= "nw")  # Adjust grid placement as needed

    #Create the text box within the notes frame
    box = tk.Text(master=notes_frame, width=20 , height=20 , background="green")
    box.insert(tk.END, notes_text)
    box.grid(row = 0 , column = 1)

    def close_view():
        #function for closing the window 
        notes_frame.destroy()

    close_button = tk.Button(master=notes_frame , text="Close Window" , command=close_view)
    close_button.grid(row=1,column=1, sticky="ew")




def edit_events(event, event_date):
    # Create a popup menu
    popup_menu = tk.Menu(gui_window, tearoff=0)

    # Add menu items
    popup_menu.add_command(label="Delete Event",  command = lambda: Delete_event(event_date))
    popup_menu.add_command(label = "Add Notes" , command = lambda:add_notes(event_date))
    popup_menu.add_command(label="View Event Notes" , command=lambda  : view_event_notes(event_date))

    #Display the menu at the cursor's positions
    popup_menu.tk_popup(event.x_root, event.y_root)


def Manage_events_btn():
    '''it should be able to show us all the saved events and also be able to edit all of the saved events'''
    with open("data.json","r") as file:
        data = json.load(file)
        dates = data["dates"]
        # Create and place labels for each event
        for i, dt in enumerate(dates):  #again and again it is also created 
            year , month , day = map(int ,  dt.split("-"))
            date_Btn = tk.Button(master=navbar_frm, text=f"DATE     :     {day} {calendar.month_name[month]} {year} \n",border=True,relief=tk.RAISED,background="red")

            date_Btn.bind("<Button-1>", lambda event, dt=dt: edit_events(event, dt))
            date_Btn.grid(row=i, column= 0 , sticky = "ew")
    # Configure the column within navbar_frm to expand
        navbar_frm.columnconfigure(0, weight=1)


if __name__ == "__main__":
    gui_window = tk.Tk()
    gui_window.title("Event Calendar")

    gui_window.rowconfigure(0, weight=1)  # Make the row in gui_window expandable
    gui_window.columnconfigure(0, weight=1)  # First column where navbar_frm is placed
    gui_window.columnconfigure(1, weight=3)  # Second column where calendar_frm is placed, given more weight

    gui_window.grid_rowconfigure(0, minsize=1000)  # Set a minimum height for the row
    gui_window.grid_columnconfigure(0, minsize=350)  # Set a minimum width for the navbar column
    gui_window.grid_columnconfigure(1, minsize=1000)  # Set a minimum width for the calendar column
    #creating two frames to hold the havbar and the calendar 
    navbar_frm = tk.Frame(master = gui_window ,height=1000,relief=tk.RAISED,borderwidth=20)
    calendar_frm = tk.Frame(master = gui_window , height= 1000 , relief=tk.SUNKEN,background="white",borderwidth=5)

    #creating the calendar label to display the calendar on the screen in the calendar_frm widget 
    #the label will take the text input returned by the display_calendar() function 
    calendar_text = display_calendar()
    calendar_txt_box = tk.Text(master=calendar_frm)

       # Create a tag with center alignment
    calendar_txt_box.tag_configure("center", justify="center")
    
    # Insert content with the "center" tag
    calendar_txt_box.insert("1.0", calendar_text, "center")
    
    # Add the tag to the entire content
    calendar_txt_box.tag_add("center", "1.0", "end")


    calendar_txt_box.config(state=tk.DISABLED)  # Set state to DISABLED after inserting content
    calendar_txt_box.pack(fill=tk.BOTH , expand=True)
    
    button_width = 20 

    #adding a menubar in the navbar widget to contain all the buttons for performing  various functions 
    menubar = Menu(gui_window)
    Event = Menu(menubar, tearoff=0)
    Event.add_command(label="CreateEvent", command = create_event_btn)
    menubar.add_cascade(label="EVENT", menu=Event)

    
    ManageEvents = Menu(menubar, tearoff=0)
    ManageEvents.add_command(label = "ManageEvents",command=Manage_events_btn)
    menubar.add_cascade(label="VIEWEVENTS",menu=ManageEvents)
    gui_window.config(menu=menubar)
    # ManageEvents.invoke()
    
    # Manage_events_btn()
    # Set minimum size for navbar_frm and calendar_frm
    navbar_frm.grid(row=0, column=0, padx=5, sticky="nsew")
    calendar_frm.grid(row=0, column=1, sticky="nsew")

    gui_window.mainloop()





