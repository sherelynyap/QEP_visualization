class Node():
    def __init__(self) -> None:
        self.children = []
        self.attributes = {}
        self.annotations = ""

def build_tree(plan):
    root = Node()
    
    for key, val in plan.items():
        if key != "Plans":
            root.attributes[key] = val
    
    ### If not leaf node
    if "Plans" in plan:
        for child_plan in plan["Plans"]:
            child_node = build_tree(child_plan)
            root.children.append(child_node)

    return root

def print_tree(root):
    queue = []
    queue.append(root)
    while len(queue) != 0:
        print("===================")
        childlength = len(queue)
        # Add appropriate children ndoes
        for i in range(childlength):
            node = queue.pop(0)
            if node != None:
                print(node.attributes['Node Type'] + "->cost: ", node.attributes['Total Cost'], end='\n')
            for child in node.children:
                queue.append(child)

false = False
true = True

plan = {
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

root = build_tree(plan)
print_tree(root)