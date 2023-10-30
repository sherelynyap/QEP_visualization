import tkinter as tk
from tkinter import ttk
import json

class ExecutionPlanNode:
    def __init__(self, node_id, node_type, content):
        self.node_id = node_id
        self.node_type = node_type
        self.content = content
        self.children = []

def parse_execution_plan(json_data, parent_id=None):
    def parse_node(node, parent_id):
        node_type = node.get("Node Type", "Unknown")
        content = {key: value for key, value in node.items() if key != "Plans"}
        execution_node = ExecutionPlanNode(len(execution_plan), node_type, content)
        execution_node.parent_id = parent_id
        execution_plan.append(execution_node)
        if "Plans" in node:
            for child in node["Plans"]:
                parse_node(child, execution_node.node_id)

    execution_plan = []
    parse_node(json_data, parent_id)
    return execution_plan

def display_tree(parent_id, parent_item):
    for node in execution_plan:
        if node.parent_id == parent_id:
            item_text = f"{node.node_type} ({node.node_id})"
            item = tree.insert(parent_item, "end", text=item_text)
            display_tree(node.node_id, item)

def display_details(event):
    selected_item = tree.selection()
    if selected_item:
        selected_node_text = tree.item(selected_item, "text")
        node_id = int(selected_node_text.split()[-1].strip('()'))
        selected_node = find_execution_node(node_id, execution_plan)
        if selected_node:
            details_text.config(state="normal")
            details_text.delete("1.0", "end")
            details_text.insert("1.0", json.dumps(selected_node.content, indent=2))
            details_text.config(state="disabled")

def find_execution_node(node_id, nodes):
    for node in nodes:
        if node.node_id == node_id:
            return node
    return None

root = tk.Tk()
root.title("Query Execution Plan Viewer")

# Replace this with your JSON input
execution_plan_json_str = '''
{
  "Node Type": "Gather",
  "Parallel Aware": false,
  "Async Capable": false,
  "Startup Cost": 5367.82,
  "Total Cost": 39354.5,
  "Plan Rows": 10,
  "Plan Width": 127,
  "Workers Planned": 2,
  "Single Copy": false,
  "Plans": [
    {
      "Node Type": "Hash Join",
      "Parent Relationship": "Outer",
      "Parallel Aware": false,
      "Async Capable": false,
      "Join Type": "Inner",
      "Startup Cost": 4367.82,
      "Total Cost": 38353.5,
      "Plan Rows": 4,
      "Plan Width": 127,
      "Inner Unique": true,
      "Hash Cond": "(c.c_nationkey = n.n_nationkey)",
      "Plans": [
        {
          "Node Type": "Hash Join",
          "Parent Relationship": "Outer",
          "Parallel Aware": true,
          "Async Capable": false,
          "Join Type": "Inner",
          "Startup Cost": 4366.26,
          "Total Cost": 38351.93,
          "Plan Rows": 4,
          "Plan Width": 27,
          "Inner Unique": true,
          "Hash Cond": "(o.o_custkey = c.c_custkey)",
          "Plans": [
            {
              "Node Type": "Seq Scan",
              "Parent Relationship": "Outer",
              "Parallel Aware": true,
              "Async Capable": false,
              "Relation Name": "orders",
              "Alias": "o",
              "Startup Cost": 0.0,
              "Total Cost": 32345.0,
              "Plan Rows": 625000,
              "Plan Width": 8
            },
            {
              "Node Type": "Hash",
              "Parent Relationship": "Inner",
              "Parallel Aware": true,
              "Async Capable": false,
              "Startup Cost": 4366.25,
              "Total Cost": 4366.25,
              "Plan Rows": 1,
              "Plan Width": 27,
              "Plans": [
                {
                  "Node Type": "Seq Scan",
                  "Parent Relationship": "Outer",
                  "Parallel Aware": true,
                  "Async Capable": false,
                  "Relation Name": "customer",
                  "Alias": "c",
                  "Startup Cost": 0.0,
                  "Total Cost": 4366.25,
                  "Plan Rows": 1,
                  "Plan Width": 27,
                  "Filter": "((c_name)::text = 'Customer#000000316'::text)"
                }
              ]
            }
          ]
        },
        {
          "Node Type": "Hash",
          "Parent Relationship": "Inner",
          "Parallel Aware": false,
          "Async Capable": false,
          "Startup Cost": 1.25,
          "Total Cost": 1.25,
          "Plan Rows": 25,
          "Plan Width": 108,
          "Plans": [
            {
              "Node Type": "Seq Scan",
              "Parent Relationship": "Outer",
              "Parallel Aware": false,
              "Async Capable": false,
              "Relation Name": "nation",
              "Alias": "n",
              "Startup Cost": 0.0,
              "Total Cost": 1.25,
              "Plan Rows": 25,
              "Plan Width": 108
            }
          ]
        }
      ]
    }
  ]
}
'''

execution_plan_json = json.loads(execution_plan_json_str)

execution_plan = parse_execution_plan(execution_plan_json)

tree_frame = tk.Frame(root)
tree_frame.pack()

tree = ttk.Treeview(tree_frame, show = "tree")
tree.pack()

display_tree(None, "")

tree.bind("<<TreeviewSelect>>", display_details)

details_frame = tk.Frame(root)
details_frame.pack()

details_text = tk.Text(details_frame, wrap="none", state="disabled", width=60, height=20)
details_text.pack()

root.mainloop()
