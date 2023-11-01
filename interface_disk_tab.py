import tkinter as tk
from tkinter import ttk
from explore import *

class ProjectWindow(tk.Tk):
    
    def destroy_block_content_display(self):
        if(self.display_block_label is not None):
            self.display_block_label.destroy()
            self.display_block_label = None

        if(self.table is not None):
            self.table.destroy()
            self.table = None

        if(self.v_scroll is not None):
            self.v_scroll.destroy()
            self.v_scroll = None

        if(self.h_scroll is not None):
            self.h_scroll.destroy()
            self.h_scroll = None

    def destroy_block_frame(self):
        if(self.block_frame_label is not None):
            self.block_frame_label.destroy()
            self.block_frame_label = None

        if(self.block_canvas is not None):
            self.block_canvas.destroy()
            self.block_canvas = None

        if(self.block_scrollbar is not None):
            self.block_scrollbar.destroy()
            self.block_scrollbar = None


    def destroy_disk_tab(self):
        # Destroy disk_tab
        if(self.disk_tab is not None):
            self.disk_tab.destroy()
            self.disk_tab = None

    def click_block_button(self, relation, block, button):
        # Actions to do when block_button is clicked
        self.display_relation(relation, block)
        
        ## REMEMBER TO ADD INTO CODE IN GITHUB
        for b in self.block_buttons:
            b.configure(bg = "grey50")
        #print("click_block_button " + str(block))
        button.configure(bg='#444444')

    def on_configure_block_canvas(self, event):
        # Configure scroll bar for block_frame
        if self.block_canvas is not None:
            self.block_canvas.configure(scrollregion=self.block_canvas.bbox("all"))


    def add_block_button(self,relation, block):
        # Add block_button to create dynamic buttons into block_canvas
        block_button = tk.Button(self.block_canvas_inner_frame, text=block, bg = "grey50")
        block_button.configure(command = lambda btn = block_button:self.click_block_button(relation, block, btn))

        # Add hover effect on button
        # relation_button.bind("<Enter>", on_hover)
        # relation_button.bind("<Leave>", on_leave)
        block_button.pack(fill = "both")

        # Adjust scrollbar
        self.block_buttons.append(block_button)
        self.block_canvas.update_idletasks()
        self.block_canvas.bind('<Configure>', self.on_configure_block_canvas)

    def config_block_frame(self, relation, block_IDs):
        # Adjust layout of block_frame
        self.block_frame.grid_rowconfigure(0, weight=1)      
        self.block_frame.grid_rowconfigure(1, weight=9)     
        self.block_frame.grid_columnconfigure(0, weight=9)  
        self.block_frame.grid_columnconfigure(1, weight=1)  
        
        # Block_frame_label on block_frame
        self.block_frame_label = tk.Label(self.block_frame, text='Block Options', wraplength=90,  borderwidth=2, relief="groove")
        self.block_frame_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, columnspan=2)

        # Create block_canvas to hold scrollbar and dynamic buttons
        self.block_canvas = tk.Canvas(self.block_frame, bg="white", width = 0, height=200)
        self.block_canvas.grid(row=1, column=0, sticky = "nsew")
        
        # Create and place the scrollbar
        self.block_scrollbar = tk.Scrollbar(self.block_frame, orient="vertical", command=self.block_canvas.yview, width = 0)
        self.block_scrollbar.grid(row=1, column=1, columnspan = 1, sticky="nsew")
        self.block_canvas.config(yscrollcommand=self.block_scrollbar.set)
        self.block_canvas.bind('<Configure>', self.on_configure_block_canvas)

        # block_canvas_inner_frame to hold dynamic buttons 
        self.block_canvas_inner_frame = tk.Frame(self.block_canvas)
        self.block_canvas.create_window((0, 0), window=self.block_canvas_inner_frame, anchor='nw')

        # Add dynamic buttons based on the relation clicked
        self.block_buttons = []
        print("block_IDs")
        print(block_IDs)
        for block in block_IDs:
            self.add_block_button(relation, block)
        self.block_canvas.configure(scrollregion=self.block_canvas.bbox("all"))

    def click_relation_button(self, relation, block_IDs, button):
        # Action to do when relation_button is clicked
        
        # Clear the content at block_content_frame
        self.destroy_block_content_display()
        self.destroy_block_frame()
        ## REMEMBER TO ADD INTO CODE IN GITHUB
        for b in self.relation_buttons:
            b.configure(bg = "grey50")


        # Configure block_frame and add in new buttons
        # self.config_block_frame(relation, block_IDs)
        self.config_page_frame(relation, block_IDs)
        button.configure(bg='#444444')

    def on_configure_relation_canvas(self, event):
        # Adjust scrollbar for relation_canvas
        if self.relation_canvas is not None:
            self.relation_canvas.configure(scrollregion=self.relation_canvas.bbox("all"))


    def add_relation_button(self, relation, block_IDs):
        # Create relation_buttons
        relation_button = tk.Button(self.relation_canvas_inner_frame, text=relation, bg = "grey50")
        relation_button.configure(command = lambda btn = relation_button:self.click_relation_button(relation, block_IDs, btn))

        # Add hover effect on button
        # relation_button.bind("<Enter>", on_hover)
        # relation_button.bind("<Leave>", on_leave)
        relation_button.pack(fill = "both")

        # Adjust scrollbar
        self.relation_buttons.append(relation_button)
        self.relation_canvas.update_idletasks()
        self.relation_canvas.bind('<Configure>', self.on_configure_relation_canvas)

    def config_relation_frame(self, block_id_per_table):
        # Adjust layout of relation_frame
        self.relation_frame.grid_rowconfigure(0, weight=1)      
        self.relation_frame.grid_rowconfigure(1, weight=9)      
        self.relation_frame.grid_columnconfigure(0, weight=9)  
        self.relation_frame.grid_columnconfigure(1, weight=1)  
        

        # Place relation_frame_label
        relation_frame_label = tk.Label(self.relation_frame, text='Relation Options', wraplength=90, borderwidth=2, relief="groove")
        relation_frame_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, columnspan=2)

        # Create relation_canvas for relation_buttons
        self.relation_canvas = tk.Canvas(self.relation_frame, bg = "black", width = 0, height=200)
        self.relation_canvas.grid(row=1, column=0, sticky = "nsew")
        

        # # Create and place the scrollbar
        scrollbar = tk.Scrollbar(self.relation_frame, orient="vertical", command=self.relation_canvas.yview, width = 0)
        scrollbar.grid(row=1, column=1, columnspan = 1, sticky="nsew")
        self.relation_canvas.config(yscrollcommand=scrollbar.set)
        self.relation_canvas.bind('<Configure>', self.on_configure_relation_canvas)

        # Create relation_canvas_inner_frame to hold dynamic buttons
        self.relation_canvas_inner_frame = tk.Frame(self.relation_canvas)
        self.relation_canvas.create_window((0, 0), window=self.relation_canvas_inner_frame, anchor='nw')

        # Add relation_buttons in relation_frame
        self.relation_buttons = []
        for relation in block_id_per_table:
            self.add_relation_button(relation, block_id_per_table[relation])
        self.relation_canvas.configure(scrollregion=self.relation_canvas.bbox("all"))


    def display_relation(self, relation, ctid):
        self.destroy_block_content_display()
        # Rerieve the schema and result based on relation and ctid
        schema, result = execute_block_query(None, relation, ctid)

        # Adjust Layout
        self.block_content_frame.grid_rowconfigure(0, weight=1)      
        self.block_content_frame.grid_rowconfigure(1, weight=10)

        # Set the label for block_frame
        self.display_block_label = tk.Label(self.block_content_frame, text="Display Content of Block " + str(ctid) + " Accessed for Relation " + relation)
        self.display_block_label.grid(row=0, column=0, sticky="nsew", columnspan=2)

        # Create tree to display the table
        self.table = ttk.Treeview(self.block_content_frame, columns=schema, show="headings")
        self.table.grid(row=1, column=0, sticky="nsew")

        # Create vertical scrollbar
        self.v_scroll = ttk.Scrollbar(self.block_content_frame, orient="vertical", command=self.table.yview)
        self.v_scroll.grid(row=1, column=1, sticky="ns")
        self.table.configure(yscrollcommand=self.v_scroll.set)

        # Create horizontal scrollbar
        self.h_scroll = ttk.Scrollbar(self.block_content_frame, orient="horizontal", command=self.table.xview)
        self.h_scroll.grid(row=2, column=0, sticky="ew")
        self.table.configure(xscrollcommand=self.h_scroll.set)

        # Add in attributes name
        for attr in schema:
            self.table.heading(attr, text=attr)
            self.table.column(attr, width=100)

        # Add in records
        for row in result:
            self.table.insert('', 'end', values=row)

        # Do minor adjustment
        self.block_content_frame.grid_rowconfigure(0, weight=1)
        self.block_content_frame.grid_columnconfigure(0, weight=1)
        
    def click_page_button(self, relation, block_IDs, button):
                # Action to do when relation_button is clicked
                
                # Clear the content at block_content_frame
                self.destroy_block_frame()
                

                ## REMEMBER TO ADD INTO CODE IN GITHUB
                for b in self.page_buttons:
                    b.configure(bg = "grey50")


                # Configure block_frame and add in new buttons
                self.config_block_frame(relation, block_IDs)
                button.configure(bg='#444444')

    def add_page_button(self,relation, page, counter):
        # Add block_button to create dynamic buttons into block_canvas
        page_button = tk.Button(self.page_canvas_inner_frame, text="Page:" + str(counter), bg = "grey50")
        page_button.configure(command = lambda btn = page_button:self.click_page_button(relation, page, btn))

        # Add hover effect on button
        # relation_button.bind("<Enter>", on_hover)
        # relation_button.bind("<Leave>", on_leave)
        page_button.pack(fill = "both")

        # Adjust scrollbar
        self.page_buttons.append(page_button)
        self.page_canvas.update_idletasks()
        self.page_canvas.bind('<Configure>', self.on_configure_page_canvas)

    def on_configure_page_canvas(self, event):
        # Configure scroll bar for block_frame
        if self.page_canvas is not None:
            self.page_canvas.configure(scrollregion=self.page_canvas.bbox("all"))

    def paginate(self, block_IDs):
        # Define the size of each sublist
        sublist_size = 1000
        # Use a list comprehension to create sublists
        sublists = [block_IDs[i:i + sublist_size] for i in range(0, len(block_IDs), sublist_size)]
        return sublists

    def config_page_frame(self, relation, block_IDs):
        # Adjust layout of block_frame
        self.page_frame.grid_rowconfigure(0, weight=1)      
        self.page_frame.grid_rowconfigure(1, weight=9)     
        self.page_frame.grid_columnconfigure(0, weight=9)  
        self.page_frame.grid_columnconfigure(1, weight=1)  
        
        # Block_frame_label on block_frame
        page_frame_label = tk.Label(self.page_frame, text='Block Page', wraplength=90,  borderwidth=2, relief="groove")
        page_frame_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, columnspan=2)

        # Create block_canvas to hold scrollbar and dynamic buttons
        self.page_canvas = tk.Canvas(self.page_frame, bg="white", width = 0, height=200)
        self.page_canvas.grid(row=1, column=0, sticky = "nsew")
        
        # Create and place the scrollbar
        page_scrollbar = tk.Scrollbar(self.page_frame, orient="vertical", command=self.page_canvas.yview, width = 0)
        page_scrollbar.grid(row=1, column=1, columnspan = 1, sticky="nsew")
        self.page_canvas.config(yscrollcommand=page_scrollbar.set)
        self.page_canvas.bind('<Configure>', self.on_configure_page_canvas)

        # page_canvas_inner_frame to hold dynamic buttons 
        self.page_canvas_inner_frame = tk.Frame(self.page_canvas)
        self.page_canvas.create_window((0, 0), window=self.page_canvas_inner_frame, anchor='nw')

        # Add dynamic buttons based on the relation clicked
        pages = self.paginate(block_IDs)
        self.page_buttons = []
        counter = 0
        for page in pages:
            self.add_page_button(relation, page, counter)
            counter+=1
        self.page_canvas.configure(scrollregion=self.page_canvas.bbox("all"))


    def create_disk_tab(self, block_id_per_table):
        # Destroy disk_tab() if needed
        self.destroy_disk_tab()

        # Create disk_tab
        self.disk_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_tab, text="disk_tab")

        # Partition disk_tab into relation_frame
        self.relation_frame = tk.Frame(self.disk_tab, bg = "white", borderwidth=2, relief="groove")
        self.relation_frame.grid_propagate(0)

        # Partition disk_tab into block_frame
        self.block_frame = tk.Frame(self.disk_tab, borderwidth=2, relief="groove", bg = "white" )
        self.block_frame.grid_propagate(0)

        # Partition disk_tab into page_frame
        self.page_frame = tk.Frame(self.disk_tab, borderwidth=2, relief="groove", bg = "white" )
        self.page_frame.grid_propagate(0)

        # Partition disk_tab into block_content_frame
        self.block_content_frame = tk.Frame(self.disk_tab, bg = "white", borderwidth=2, relief="groove")
        self.block_content_frame.grid_propagate(0)

        # Adjust layout of disk_tab
        self.disk_tab.grid_columnconfigure(0, weight=2)  
        self.disk_tab.grid_columnconfigure(1, weight=2)  
        self.disk_tab.grid_columnconfigure(2, weight=6)  
        self.disk_tab.grid_rowconfigure(0, weight=1)      
        self.disk_tab.grid_rowconfigure(1, weight=1)      

        # Place relation_frame, block_frame, block_content_frame
        self.relation_frame.grid(row=0, column=0, sticky="nsew")
        self.block_frame.grid(row=0, column=1, rowspan = 2, sticky="nsew")
        self.page_frame.grid(row=1, column=0, sticky="nsew")
        self.block_content_frame.grid(row=0, column=2, rowspan=2, sticky="nsew")

        # Configure relation_frame to display buttons of relation
        self.config_relation_frame(block_id_per_table)

       

    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        screen_width//=2
        screen_height//=2
        self.geometry(f"{screen_width}x{screen_height}")
        self.title("CZ4031 Database Project 2")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.QEP_tab = ttk.Frame(self.notebook)

        # Add these to ProjectWindow() attributes
        self.disk_tab = None
        self.relation_frame = None
        self.relation_canvas = None
        self.relation_canvas_inner_frame = None
        self.display_block_label = None
        self.table = None
        self.v_scroll = None
        self.h_scroll = None
        self.blocks_frame = None
        self.block_frame_label = None
        self.block_content_frame = None
        self.block_scrollbar = None
        self.block_canvas = None
        self.block_scrollbar = None

        self.notebook.add(self.QEP_tab, text="QEP_tab")
        testingRelationTable = {"Table1": [1], 
                                "Table2": [2],
                                "Table3": [3], 
                                "Table4": [4],
                                "Table5": [5], 
                                "Table6": [6],
                                "Table7": [7], 
                                "Table8": [8],
                                "Table9": [9], 
                                "Table10": [10, 20, 30, 40, 50, 60, 70, 80, 80, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 57, 23, 31, 35, 235, 124],
                                "Table11": [11], 
                                "Table12": [12],
                                "Table13": [13], 
                                "Table14": [14],
                                "Table15": [15], 
                                "Table16": [16],
                                "Table17": [17], 
                                "Table18": [18],
                                "Table19": [19], 
                                "Table200000000000000000000000000": [20]
                                }
        temp = []
        for i in range(10000):
            temp.append(i)
        testingRelationTable["Table11"] = temp
        self.create_disk_tab(testingRelationTable)

# Create an instance of your custom window class and start the Tkinter mainloop
if __name__ == "__main__":
    app = ProjectWindow()
    app.mainloop()
