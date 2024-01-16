import tkinter as tk 
import calendar 


def display_calendar(): #function for giving us a calendar 
    #let us crate a separate gui for the calendar object 
    fetch_year  = 2024 
    cal_content = calendar.calendar(fetch_year)  
    return cal_content

#adding the buttons and the color coding functionality 
#well what we can do is before displaying the calendar , we can color code our calendar , we can add the required functionality to our project 
def select_date():
    #this function will select a particular date of particular month , and will highlight that date in the calendar 
    




if __name__ == "__main__":
    gui_window = tk.Tk()
    gui_window.title("Event Calendar")

    #adding resizability to our grid on the left hand side and the right hand side
    # gui_window.columnconfigure(0,weight = 1)
    gui_window.columnconfigure(1,weight = 1)
    
    #creating two frames to hold the havbar and the calendar 
    navbar_frm = tk.Frame(master = gui_window , width=350,height=1000,relief=tk.RAISED,background="red",borderwidth=5)
    calendar_frm = tk.Frame(master = gui_window , width= 1000 , height= 1000 , relief=tk.SUNKEN,background="white",borderwidth=5)

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

    #putting the two frames in the grid , navbar on left hand side , calendar on right hand side 
    navbar_frm.grid(row=0,column=0,padx=5)
    calendar_frm.grid(row=0,column=1,sticky="nsew")

    gui_window.mainloop()