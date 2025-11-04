from tkinter import *
from time import strftime

# Create the main window
window = Tk()
window.geometry("600x300")        # Set window size
window.title("Digital Clock")     # Set window title
window.config(bg="black")         # Background color

# Label to display time
lbl_time = Label(window, text="HH:MM:SS AM", font=("arial", 70, "bold"), bg="black", fg="white")
lbl_time.place(x=30, y=70)

# Label to display the day
lbl_day = Label(window, text="Day", font=("arial", 20, "bold"), bg="black", fg="white")
lbl_day.place(x=200, y=170)

# Function to update time continuously
def clock():
    h = strftime("%I")      # Hour in 12-hour format
    m = strftime("%M")      # Minute
    s = strftime("%S")      # Second
    ampm = strftime("%p")   # AM or PM
    day = strftime("%A")    # Day of the week

    lbl_time.config(text=h + ":" + m + ":" + s + " " + ampm)
    lbl_day.config(text=day)

    lbl_time.after(1000, clock)  # Update every 1 second

# Start the clock
clock()

# Run the main window loop
window.mainloop()