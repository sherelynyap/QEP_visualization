from math import floor
from tkinter import messagebox, font
from typing import Tuple, Union
import tkinter as tk
from tkinter import ttk
from explore import *

NoneType = type(None)

def countLeafNodes(node: Node):
    leafNodesNum = 0
    queue = [node]
    while (len(queue) > 0):
        curNode = queue.pop()
        if (len(curNode.children) > 0):
            for node in curNode.children:
                queue.append(node)
        else:
            leafNodesNum += 1
    return leafNodesNum

def traverseTree(root):
    if not root:
        return
    
    for k, v in root.attributes.items():
        root.annotations+= f"{k}: {v}\n"
    if root.children:
        for child in root.children:
            traverseTree(child)
class DisplayNode():
    def __init__(self) -> None:
        self.children: list[DisplayNode] = []
        self.text = ""
        self.annotations = ""
        self.depth: int = 0
        self.left_bound: int = 0
        self.right_bound: int = 0


def createDisplayNode(root: Node):
    maxBound = countLeafNodes(root)
    rootDisplay = DisplayNode()
    rootDisplay.left_bound = 0
    rootDisplay.right_bound = maxBound
    rootDisplay.text = root.attributes['Node Type']
    rootDisplay.annotations = root.annotations
    nodeQueue: list[Tuple[DisplayNode, Node, Tuple[int, int]]] = []  # tuple of (displayNode parent, node child)
    if (len(root.children) == 1):
        nodeQueue.append((rootDisplay, root.children[0], (0, maxBound)))
    elif (len(root.children) == 2):
        nodeQueue.append((rootDisplay, root.children[0], (0, countLeafNodes(root.children[0]))))
        nodeQueue.append((rootDisplay, root.children[1], (countLeafNodes(root.children[0]), maxBound)))
    while (len(nodeQueue) > 0):
        curNode = nodeQueue.pop(0)
        newChild = DisplayNode()
        newChild.left_bound = curNode[2][0]
        newChild.right_bound = curNode[2][1]
        newChild.text = curNode[1].attributes['Node Type']
        newChild.annotations = curNode[1].annotations
        newChild.depth = curNode[0].depth + 1
        # append to parent
        curNode[0].children.append(newChild)
        if (len(curNode[1].children) == 1):
            nodeQueue.append((newChild, curNode[1].children[0], (newChild.left_bound, newChild.right_bound)))
        elif (len(curNode[1].children) == 2):
            nodeQueue.append((newChild, curNode[1].children[0],
                              (newChild.left_bound, newChild.left_bound + countLeafNodes(curNode[1].children[0]))))
            nodeQueue.append((newChild, curNode[1].children[1],
                              (newChild.left_bound + countLeafNodes(curNode[1].children[0]), newChild.right_bound)))
    return rootDisplay

class ProjectWindow(tk.Tk):
    def scroll_move(self, event):
        self.planCanvas.scan_dragto(event.x, event.y, gain=1)

    def scroll_start(self, event):
        self.planCanvas.scan_mark(event.x, event.y)

    def onObjectClick(self, event):
        x = event.widget.canvasx(event.x)
        y = event.widget.canvasy(event.y)
        self.annoStr.set(self.dictExtraToID[event.widget.find_closest(x, y)[0]])
        if (self.dictExtraToID[event.widget.find_closest(x, y)[0]] != ""):
            self.open_popup(self.dictExtraToID[event.widget.find_closest(x, y)[0]])
    
    def createTextRectangle(self, text: str, canvas: tk.Canvas, x0: int, y0: int):
        rectangle = canvas.create_rectangle(x0, y0, x0 + 100, y0 + 50, fill="#FFFFFF")
        textline = canvas.create_text(x0 + 50, y0 + 25, text=text, justify='center')
        self.textBoxes.append(textline)
        self.planCanvas.tag_bind(rectangle, '<ButtonPress-1>', self.onObjectClick)
        self.planCanvas.tag_bind(textline, '<ButtonPress-1>', self.onObjectClick)
        return (rectangle, textline)

    def open_popup(self, text: str):
        top = tk.Toplevel(self)
        top.title("Annotation")
        lbl = tk.Label(top, text=text, font=('Arial', 12, ''), wraplength=300)
        lbl.pack()
        btn = tk.Button(top, text="Close", command=top.destroy)
        btn.pack()

    def drawCanvasPlan(self, root: Node):
        self.planCanvas.delete("all")
        self.dictExtraToID = {}
        self.scale = 0
        self.textBoxes = []

        rootD = createDisplayNode(root)

        drawQueue: list[Tuple[DisplayNode, Union[DisplayNode, NoneType]]] = [(rootD, None)]
        while (len(drawQueue) > 0):
            curTup = drawQueue.pop(0)
            curNode = curTup[0]
            for child in curNode.children:
                drawQueue.append((child, curNode))
            x = (curNode.left_bound * 200 + curNode.right_bound * 200) / 2 - 50
            y = curNode.depth * 100 + 50 - 25
            (rect, line) = self.createTextRectangle(curNode.text, self.planCanvas, x, y)
            self.dictExtraToID[rect] = curNode.annotations
            self.dictExtraToID[line] = curNode.annotations
            if (curTup[1] != None):
                self.planCanvas.create_line((curNode.left_bound * 200 + curNode.right_bound * 200) / 2,
                                            curNode.depth * 100 + 50 - 25,
                                            (curTup[1].left_bound * 200 + curTup[1].right_bound * 200) / 2,
                                            (curNode.depth - 1) * 100 + 50 + 25)

    def processQuery(self):
        # query = "Select * FROM public.lineitem join public.supplier on public.lineitem.l_suppkey = public.supplier.s_suppkey WHERE public.supplier.s_nationkey = 3"
        query = self.queryTextBox.get(1.0, "end-1c")
        print(query)

        # Clear query
        self.queryTextBox.delete(1.0, "end")
        
        result_dict = get_qep_info(self.connection, query)
        if result_dict == "error":
            print("Please check your sql statements")
            messagebox.showerror(
                title="Warning", message="Please check your sql statement entered.")
            return
        
        root = result_dict['root']
        '''# block_id_per_table
        with open('result_dict.json', 'w') as output_file:
            json.dump(result_dict['block_id_per_table'], output_file, default = lambda x: x.__dict__ ,ensure_ascii = False, indent = 4)'''
        self.create_disk_tab(result_dict['block_id_per_table'])

        traverseTree(root)

        # Draw optimal query tree
        self.drawCanvasPlan(root)

    def centreCanvas(self):
        self.planCanvas.scale("all", 0, 0, pow(0.8, self.scale), pow(0.8, self.scale))
        self.planCanvas.xview_moveto(0.5)
        self.planCanvas.yview_moveto(0)
        writingFont = font.nametofont("TkDefaultFont").copy()
        for text in self.textBoxes:
            self.planCanvas.itemconfig(text, font=writingFont)

        self.scale = 0

    def zoomIn(self):
        self.scale += 1
        self.planCanvas.scale("all", 0, 0, 1.25, 1.25)
        writingFont = font.nametofont("TkDefaultFont").copy()
        writingFont.config(size=floor(writingFont.cget("size") * pow(1.1, self.scale)))
        for text in self.textBoxes:
            self.planCanvas.itemconfig(text, font=writingFont)

    def zoomOut(self):
        self.scale -= 1
        self.planCanvas.scale("all", 0, 0, 0.8, 0.8)
        writingFont = font.nametofont("TkDefaultFont").copy()
        writingFont.config(size=floor(writingFont.cget("size") * pow(1.1, self.scale)))
        for text in self.textBoxes:
            self.planCanvas.itemconfig(text, font=writingFont)

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

    def destroy_disk_tab(self):
        # Destroy disk_tab
        if(self.disk_tab is not None):
            self.disk_tab.destroy()
            self.disk_tab = None

    def click_block_button(self, relation, block, button):
        # Actions to do when block_button is clicked
        self.display_relation(relation, block)
        
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
        block_frame_label = tk.Label(self.block_frame, text='Block Options', wraplength=90,  borderwidth=2, relief="groove")
        block_frame_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, columnspan=2)

        # Create block_canvas to hold scrollbar and dynamic buttons
        self.block_canvas = tk.Canvas(self.block_frame, bg="white", width = 0, height=200)
        self.block_canvas.grid(row=1, column=0, sticky = "nsew")
        
        # Create and place the scrollbar
        block_scrollbar = tk.Scrollbar(self.block_frame, orient="vertical", command=self.block_canvas.yview, width = 0)
        block_scrollbar.grid(row=1, column=1, columnspan = 1, sticky="nsew")
        self.block_canvas.config(yscrollcommand=block_scrollbar.set)
        self.block_canvas.bind('<Configure>', self.on_configure_block_canvas)

        # block_canvas_inner_frame to hold dynamic buttons 
        self.block_canvas_inner_frame = tk.Frame(self.block_canvas)
        self.block_canvas.create_window((0, 0), window=self.block_canvas_inner_frame, anchor='nw')

        # Add dynamic buttons based on the relation clicked
        self.block_buttons = []
        for block in block_IDs:
            self.add_block_button(relation, block)
        self.block_canvas.configure(scrollregion=self.block_canvas.bbox("all"))

    def click_relation_button(self, relation, block_IDs, button):
        # Action to do when relation_button is clicked
        
        # Clear the content at block_content_frame
        self.destroy_block_content_display()

        # Configure block_frame and add in new buttons
        self.config_block_frame(relation, block_IDs)
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
        schema, result = execute_block_query(self.connection, relation, ctid)

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
        
    def create_QEP_tab(self):
        self.QEP_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.QEP_tab, text="QEP_tab")

        inputFrame = tk.Frame(self.QEP_tab, borderwidth=10)
        inputFrame.pack(side=tk.LEFT, expand=True, fill="both")

        planFrame = tk.Frame(self.QEP_tab)
        planFrame.pack(side=tk.RIGHT, expand=True, fill="both")
        
        zoomFrame = tk.Frame(planFrame)
        zoomFrame.pack()
        centreBtn = tk.Button(zoomFrame, text="RESET VIEW", command=self.centreCanvas)
        centreBtn.pack(side=tk.RIGHT)
        zoomInBtn = tk.Button(zoomFrame, text="Zoom In", command=self.zoomIn)
        zoomInBtn.pack(side=tk.LEFT)
        zoomOutBtn = tk.Button(zoomFrame, text="Zoom Out", command=self.zoomOut)
        zoomOutBtn.pack(side=tk.RIGHT)

        self.planCanvas = tk.Canvas(planFrame, bg="#FFFFFF")
        self.planCanvas.pack(expand=True, fill="both")

        self.planCanvas.bind("<ButtonPress-1>", self.scroll_start)
        self.planCanvas.bind("<B1-Motion>", self.scroll_move)

        queryLabel = tk.Label(inputFrame, text="Query:")
        queryLabel.pack(anchor=tk.W)

        self.queryTextBox = tk.Text(inputFrame, height=10, width=30)
        self.queryTextBox.pack(expand=True, fill="both")

        processBtn = tk.Button(inputFrame, text="Process query", command=self.processQuery)
        processBtn.pack()

        self.annoStr = tk.StringVar()
        self.resizable(True, True)

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

        # Partition disk_tab into block_content_frame
        self.block_content_frame = tk.Frame(self.disk_tab, bg = "white", borderwidth=2, relief="groove")
        self.block_content_frame.grid_propagate(0)

        # Adjust layout of disk_tab
        self.disk_tab.grid_columnconfigure(0, weight=2)  
        self.disk_tab.grid_columnconfigure(1, weight=8)  
        self.disk_tab.grid_rowconfigure(0, weight=1)      
        self.disk_tab.grid_rowconfigure(1, weight=1)      

        # Place relation_frame, block_frame, block_content_frame
        self.relation_frame.grid(row=0, column=0, sticky="nsew")
        self.block_frame.grid(row=1, column=0, sticky="nsew")
        self.block_content_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Configure relation_frame to display buttons of relation
        self.config_relation_frame(block_id_per_table)
        

    def __init__(self):
        super().__init__()
        self.scale = 0
        self.dictExtraToID = {}
        self.textBoxes = []

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        screen_width//=2
        screen_height//=2
        self.geometry(f"{screen_width}x{screen_height}")
        self.title("CZ4031 Database Project 2")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
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
        self.block_content_frame = None
        
        self.block_id_per_table = {}
        self.connection = connect_database(database="TPC-H",password="since2001")
        self.create_QEP_tab()
        self.create_disk_tab(self.block_id_per_table)

# Create an instance of your custom window class and start the Tkinter mainloop
if __name__ == "__main__":
    app = ProjectWindow()
    app.mainloop()