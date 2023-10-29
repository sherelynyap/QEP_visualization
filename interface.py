import tkinter as tk
from tkinter import Scrollbar
def destroy_disk_accessed_canvas():
    global disk_accessed_canvas

    # Remove disk_accessed_canvas that holds list of accessed dick buttons
    if(disk_accessed_canvas is not None):
        disk_accessed_canvas.destroy()
        disk_accessed_canvas = None
def destroy_disk_accessed_scrollbar():
    global disk_accessed_scrollbar

    # Remove scrollbar at the disk accessed frame
    if(disk_accessed_scrollbar is not None):
        disk_accessed_scrollbar.destroy()
        disk_accessed_scrollbar = None
def destroy_qep_aspect_canvas():
    global qep_aspect_canvas

    # Remove qep_aspect_canvas that holds list of qep feature buttons
    if(qep_aspect_canvas is not None):
        qep_aspect_canvas.destroy()
        qep_aspect_canvas = None
def destroy_explain_scrollbar():
    global explain_scrollbar

    # Remove scrollbar at the explain_frame
    if(explain_scrollbar is not None):
        explain_scrollbar.destroy()
        explain_scrollbar = None
def destroy_back_button():
    global back_button

    # Remove back_button
    if(back_button is not None):
        back_button.destroy()
        back_button = None
def destroy_explain_detail_widget():
    global explain_detail_widget

    # Remove explain_detail_widget textbox widget that provide details of QEP aspect
    if(explain_detail_widget is not None):
        explain_detail_widget.destroy()
        explain_detail_widget = None
def on_hover(event):
    # Hover effect for button
    clr = event.widget.cget("background")
    if( clr != "#444444"):
        event.widget.config(bg="lightblue")  # Change background color on hover
def on_leave(event):
    # Hover effect for button
    clr = event.widget.cget("background")
    if( clr != "#444444"):
        event.widget.config(bg="grey50")  # Restore original background color on leave

def reset_window():
    # Reset window to original window
    destroy_disk_accessed_canvas()
    destroy_disk_accessed_scrollbar()
    destroy_qep_aspect_canvas()
    destroy_explain_scrollbar()
    destroy_back_button()
    
def on_submit():
    # Get the text from the Text widget
    reset_window()
    sql_input = sql_input_widget.get("1.0", "end-1c")  
    print("sql_input = " + sql_input)
    
    # Pass the text to explore.py

    # Get explain results
    # Display explain results
    display_qep_aspects_buttons()
    
    # Get accessed disk 
    # Display dyamic buttons of accessed disk
    display_disk_accessed_buttons()

    # Get schema
    # Display Schema on result_frame
    

def on_configure_qep_aspect_canvas(event):
    global qep_aspect_canvas

    # Update the canvas scroll region at qep_aspect_canvas to match the frame size
    if(qep_aspect_canvas is not None and qep_aspect_canvas.bbox("all") is not None):
        qep_aspect_canvas.configure(scrollregion=qep_aspect_canvas.bbox("all"))

def on_configure_disk_accessed_canvas(event):
    global disk_accessed_canvas

    # Update the canvas scroll region at disk_accessed_canvas to match the frame size
    if(disk_accessed_canvas is not None and disk_accessed_canvas.bbox("all") is not None):
        disk_accessed_canvas.configure(scrollregion=disk_accessed_canvas.bbox("all"))


def click_accessed_dick_button(k, button):
    # Get the k disk accessed schema
    # Display the content of k disk accessed in the result_frame

    # Create toggle effect by setting button to gray colour
    button.configure(bg='#444444')

def add_accessed_disk_button(k):
    # Add a button, k to disk_accessed_frame, where k is the disk ID
    global inner_frame
    global accessed_disk_buttons
    global disk_accessed_canvas

    # Create Button
    disk_button = tk.Button(inner_frame, text=f"Button {k}", padx=150, borderwidth=5, wraplength=150, bg = "grey50")
    disk_button.configure(command = lambda btn = disk_button:click_accessed_dick_button(k, btn))

    # Add hover effect on Button
    disk_button.bind("<Enter>", on_hover)
    disk_button.bind("<Leave>", on_leave)
    disk_button.pack(fill='x', expand = True)

    # Adjust scrollbar
    accessed_disk_buttons.append(disk_button)
    disk_accessed_canvas.bind('<Configure>', on_configure_disk_accessed_canvas)

def add_qep_aspect_button(qep_aspect):
    # Add a button, qep_aspect to qep_aspect_canvas_inner_frame
    global qep_aspect_canvas_inner_frame
    qep_aspect_button = tk.Button(qep_aspect_canvas_inner_frame, text=f"Button {qep_aspect}", padx=100, wraplength=150, bg = "grey50")
    qep_aspect_button.configure(command = lambda btn = qep_aspect_button:click_qep_aspect_button(qep_aspect, btn))

    # Add hover effect on button
    qep_aspect_button.bind("<Enter>", on_hover)
    qep_aspect_button.bind("<Leave>", on_leave)
    qep_aspect_button.pack(fill='x')

    # Adjust scrollbar
    qep_aspect_buttons.append(qep_aspect_button)
    qep_aspect_canvas.bind('<Configure>', on_configure_qep_aspect_canvas)
    

def initialize_window():
    # Instantiate global frames needed in the window
    global root 
    global upper_frame
    global schema_output_frame
    global frame1
    global frame2
    global sql_input_label_frame
    global sql_input_widget_frame
    global sql_input_button_frame
    global explain_frame
    global disk_accessed_frame
    global label_font 
    label_font= ("Helvetica", 14, "bold")
    global button_font
    button_font = ("Arial", 10)
    
    # Initialize root frame
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_width//=2
    screen_height//=2
    root.geometry(f"{screen_width}x{screen_height}")
    root.title('Database System Principle Project 2')

    # Split root frame into upper_frame for SQL inputs, QEP aspects displays and disk accessed display
    # And schema_output_frame to output schema
    upper_frame = tk.Frame(root, relief="groove")
    upper_frame.pack( side = tk.TOP, fill = tk.BOTH, expand = True)
    schema_output_frame = tk.Frame(root, borderwidth=2, relief="groove")
    schema_output_frame.pack( side = tk.TOP, fill = tk.BOTH, expand = True)

    # Split upper frame into frame1 for SQL inputs 
    # And frame2 for QEP aspects displays and dick accessed display
    frame1 = tk.Frame(upper_frame, borderwidth=2, relief="groove", bg='gray')
    frame1.pack( side = tk.LEFT, fill = tk.BOTH, expand = True, padx=0, pady=0)
    frame2 = tk.Frame(upper_frame, relief="groove")
    frame2.pack( side = tk.LEFT, fill = tk.BOTH, expand = True)

    # Split frame2 into explain_frame for QEP aspects display
    # And disk_accessed_frame for disk accessed display
    explain_frame = tk.Frame(frame2, borderwidth=2, relief="groove")
    explain_frame.pack( side = tk.LEFT, fill = tk.BOTH, expand = True, padx=0, pady=0)
    disk_accessed_frame = tk.Frame(frame2, borderwidth=2, relief="groove")
    disk_accessed_frame.pack( side = tk.LEFT, fill = tk.BOTH, expand = True)

def config_frame1():
    global sql_input_widget
    global submit_button

    # Split frame1 into sql_input_label_frame to display "Enter your SQL Query"
    sql_input_label_frame = tk.Frame(frame1, bg='white')
    sql_input_label_frame.grid(row=0, column=0, sticky='nsew')
    inputLabel = tk.Label(sql_input_label_frame, text='Enter your SQL Query:', font = label_font, bg = "white")
    inputLabel.pack(side = 'left')
    frame1.grid_rowconfigure(0, weight=1)

    # Split frame1 into sql_input_widget_frame to get sql inputs
    sql_input_widget_frame = tk.Frame(frame1, bg='blue')
    sql_input_widget_frame.grid(row=1, column=0, sticky='nsew')
    frame1.grid_rowconfigure(1, weight=5)

    # Set sql_input_widget to get sql inputs inside sql_input_widget_frame
    sql_input_widget = tk.Text(sql_input_widget_frame, wrap='word', borderwidth=2, relief="groove") 
    sql_input_widget.place(relwidth=1, relheight=1) 
    sql_input_widget.pack_propagate(False)

    # Split frame1 into sql_input_button_frame to include "Run Query" Button
    sql_input_button_frame = tk.Frame(frame1, bg='white')
    sql_input_button_frame.grid(row=2, column=0, sticky='nsew')
    frame1.grid_rowconfigure(2, weight=1)
    submit_button = tk.Button(frame1, text='Run Query', command=on_submit, bg = "grey50")
    submit_button.grid(row = 2, column = 0)

    # Add hover effect for submit_button
    submit_button.bind("<Enter>", on_hover)
    submit_button.bind("<Leave>", on_leave)
    frame1.grid_columnconfigure(0, weight=1)

def display_qep_aspects_buttons():
    qep_aspect_label.config(text = "QEP Aspects", font = label_font)
    global qep_aspect_canvas
    global explain_scrollbar 
    explain_scrollbar = None
    global qep_aspect_canvas_inner_frame
    global qep_aspect_buttons
    global explain_detail_widget

    # Clear space in explain_frame
    destroy_explain_detail_widget()
    destroy_back_button()
    
    # Create qep_aspect_canvas to hold qep_aspect_buttons
    qep_aspect_canvas = tk.Canvas(explain_frame, width=1, height=1, bg = 'white')
    qep_aspect_canvas.pack(side='left', fill='both', expand=True)

    # Create a canvas with a vertical scrollbar
    explain_scrollbar = tk.Scrollbar(explain_frame, orient='vertical', command=qep_aspect_canvas.yview)
    explain_scrollbar.pack(side='right', fill='y')
    qep_aspect_canvas.configure(yscrollcommand=explain_scrollbar.set)
    qep_aspect_canvas.bind('<Configure>', on_configure_qep_aspect_canvas)

    # Create an inner frame to hold the buttons within the canvas
    qep_aspect_canvas_inner_frame = tk.Frame(qep_aspect_canvas)
    qep_aspect_canvas.create_window((0, 0), window=qep_aspect_canvas_inner_frame, anchor='nw')

    qep_aspect_buttons = []

    # EDIT: Get the qep_aspects to be made into buttons
    qep_aspects =["Cost", "Time", "Number of Disk Accessed", "HAHAHAHAHHAHAHAHHAHAHAHHAHAHHAHAHHAHHAHAHHHAHAHAHHA"]
    for aspect in qep_aspects:
        add_qep_aspect_button(aspect)

def click_qep_aspect_button(qep_aspect, btn):
    global qep_aspect_canvas
    global qep_aspect_canvas_inner_frame
    global explain_scrollbar
    global back_button

    # Clear space at explain_frame
    destroy_qep_aspect_canvas()
    destroy_explain_scrollbar()

    # Display the details of qep_espects
    display_qep_aspects_details(qep_aspect)


def display_qep_aspects_details(qep_aspect):
    global qep_aspect_label
    global explain_detail_widget
    global explain_frame
    global back_button

    # Update the qep_aspect_label
    qep_aspect_label.config(text = "Details of : " + qep_aspect, height = 3, font = button_font)
    
    TESTING = ""
    # Add a explain_detail_widget textbox widget to output the explanations
    explain_detail_widget = tk.Text(explain_frame, width=1, height=1, wrap=tk.WORD)
    explain_detail_widget.pack(expand = True, fill = "both", side = 'top')

    # Edit: Set explain_result_text
    explain_detail_widget.insert("1.0", TESTING)

    # Initialize a back_button to backtrack
    back_button = tk.Button(explain_frame, text='Back', command=click_back_button, bg = "grey50")
    back_button.pack(side = "top")

    # Add hover effect on back_button
    back_button.bind("<Enter>", on_hover)
    back_button.bind("<Leave>", on_leave)

def click_back_button():
    # Back tracks
    display_qep_aspects_buttons()

def config_explore_result_frame():
    global qep_aspect_label
    global qep_aspect_canvas
    qep_aspect_canvas = None
    global explain_detail_widget
    explain_detail_widget = None
    global back_button
    back_button = None
    global explain_scrollbar 
    explain_scrollbar = None

    # Set "QEP Aspects" in qep_aspect_label
    qep_aspect_label = tk.Label(explain_frame, text='QEP Aspects', wraplength=90, font = label_font, height = 3, bg = "white", borderwidth=2, relief="groove")
    qep_aspect_label.pack(side = "top", fill = "x")


def display_disk_accessed_buttons():
    global disk_accessed_label
    disk_accessed_label.config(text = "Disk Accessed")
    global disk_accessed_canvas
    disk_accessed_canvas = None
    global disk_accessed_scrollbar 
    disk_accessed_scrollbar = None
    global inner_frame
    global accessed_disk_buttons

    # Create disk_accessed_canvas to store the disk_accessed_buttons
    disk_accessed_canvas = tk.Canvas(disk_accessed_frame, width=1, height=1, bg = 'white')
    disk_accessed_canvas.pack(side='left', fill='both', expand=True)

    # Create a canvas with a vertical scrollbar
    disk_accessed_scrollbar = tk.Scrollbar(disk_accessed_frame, orient='vertical', command=disk_accessed_canvas.yview)
    disk_accessed_scrollbar.pack(side='right', fill='y')
    disk_accessed_canvas.configure(yscrollcommand=disk_accessed_scrollbar.set)
    disk_accessed_canvas.bind('<Configure>', on_configure_disk_accessed_canvas)

    # Create an inner frame to hold the disk_accessed_buttons within the canvas
    inner_frame = tk.Frame(disk_accessed_canvas, width = 1, height = 1)
    inner_frame.pack(fill="both", expand=True)
    disk_accessed_canvas.create_window((0, 0), window=inner_frame, anchor='nw')
    
    
    accessed_disk_buttons = []

    # EDIT: Create and add buttons dynamically for diskID
    for i in range(1000):
        add_accessed_disk_button(i)

    

def config_disk_accessed_frame():
    global disk_accessed_canvas
    global disk_accessed_scrollbar
    global inner_frame
    global disk_accessed_label
    disk_accessed_canvas = None
    disk_accessed_scrollbar = None
    inner_frame = None
    disk_accessed_label = None
    disk_accessed_label = tk.Label(disk_accessed_frame, text='Disk Accessed', font = label_font, height = 3, bg = "white", borderwidth=2, relief="groove")
    disk_accessed_label.pack(fill = "x")


def main():
    initialize_window()
    config_explore_result_frame()
    config_frame1()
    config_disk_accessed_frame()
    root.mainloop()

main()