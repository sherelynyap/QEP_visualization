class Annotation:
	def traverseTree(self, root):
		if not root:
			return
		
		self.generateAnnotation(root)
		if root.children:
			for child in root.children:
				self.traverseTree(child)

	# def comparison(self, node):
	# 	if len(node.alternate_plans) != 0:
	# 		for altScan in node.alternate_plans:
	# 			annotation = f"\nCompared to {node.attributes['Node Type']}, {altScan} is {node.alternate_plans.get(altScan):.2f} " \
	# 							f"times as expensive.\n"
	# 			node.annotations += annotation
	# 	else:
	# 		annotation = f"{node.attributes['Node Type']} is used across all AQPs.\n"
	# 		node.annotations += annotation

	def getKeys(self, node):
		group_key = []
		if "Group Key" in node.attributes:
			group_key = node.attributes['Group Key']

		list_of_keys = []
		for key in group_key:
			list_of_keys.append(key)
		stringOfKeys = ', '.join(list_of_keys)
		if len(stringOfKeys) > 1:
			stringOfKeys = ', '.join(list_of_keys)
		else:
			stringOfKeys = list_of_keys[0]
		return stringOfKeys

	def getTables(self, cond):
		cond = cond.replace(" ", "")
		cond = cond.lstrip("(").rstrip(")")
		condsplit = cond.split('.')
		table1 = condsplit[0]
		condsplit2 = condsplit[1].split('=')
		table2 = condsplit2[1]
		return table1, table2

	def formatCondition(self, cond):
		cond = cond.replace(" ", "")
		cond = cond.replace(")AND(", ", ")
		cond = cond.replace(")OR(", ", ")
		cond = cond.replace("(", "")
		cond = cond.replace(")", "")
		return cond

	def generateAnnotation(self, node):
		# nodeType = node.attributes['Node Type']
		for k, v in node.attributes.items():
			node.annotations+= f"{k}: {v}\n"
		
		# For scans
		# if nodeType == "Seq Scan":
		# 	table = node.attributes['Relation Name']
		# 	node.annotations += f"Sequential Scan {table}\nCost: {node.attributes['Startup Cost']}"
		# 	node.annotations += ".\n"

		# if nodeType == "Index Scan":
		# 	table = node.attributes['Relation Name']
		# 	node.annotations += f"Index scan {table}"
		# 	if "Index Cond" in node.attributes:
		# 		cond = node.attributes['Index Cond']
		# 		cond = self.formatCondition(cond)
		# 		node.annotations += " with conditions {}".format(cond)
		# 	node.annotations += ".\n"

		# if nodeType == "Index Only Scan":
		# 	table = node.attributes['Relation Name']
		# 	node.annotations += f"Index only scan {table}"
		# 	if "Index Cond" in node.attributes:
		# 		cond = self.formatCondition(cond)
		# 		node.annotations += " with conditions {}".format(cond)
		# 	node.annotations += ".\n"

		# # For joins
		# if nodeType == "Hash Join":
		# 	cond = node.attributes['Hash Cond']
		# 	try:
		# 		cond = self.formatCondition(cond)

		# 		condsplit = cond.split('.')
		# 		table1 = condsplit[0]
		# 		condsplit2 = condsplit[1].split('=')
		# 		table2 = condsplit2[1]
		# 		annotation = f"Hash join {table1} and {table2}, with the conditions {cond}.\n"
		# 	except:
		# 		annotation = f"Hash join on conditions {cond}.\n"
		# 	node.annotations += annotation

		# if nodeType == "Merge Join":
		# 	cond = node.attributes['Merge Cond']
		# 	try:
		# 		cond = self.formatCondition(cond)

		# 		condsplit = cond.split('.')
		# 		table1 = condsplit[0]
		# 		condsplit2 = condsplit[1].split('=')
		# 		table2 = condsplit2[1]
		# 		annotation = f"Merge join {table1} and {table2}, with conditions {cond}.\n"
		# 	except:
		# 		annotation = "Merge join on conditions {}.\n".format(cond)
		# 	node.annotations += annotation

		# if nodeType == "Nested Loop":
		# 	node.annotations += "Nested Loop join\n"

		# # All other operators
		# if nodeType == "Hash":
		# 	if "Output" in node.attributes:
		# 		output = node.attributes['Output']
		# 		temp = output[0].split('.')
		# 		temp1 = temp[0]
		# 		annotation = f"Hash table {temp1}.\n"
		# 	else:	
		# 		annotation = "Hash table\n"
		# 	node.annotations += annotation

		# if nodeType == "Aggregate":
		# 	strategy = node.attributes['Strategy']
		# 	if strategy == "Sorted":
		# 		if "Group Key" in node.attributes:
		# 			stringOfKeys = self.getKeys(node)
		# 			annotation = "Sort Aggregate grouping on keys: {}.\n".format(stringOfKeys)
		# 		else:
		# 			annotation = "Sort Aggregate.\n"
		# 	elif strategy == "Hashed":
		# 		if "Group Key" in node.attributes:
		# 			stringOfKeys = self.getKeys(node)
		# 			annotation = "Hash Aggregate grouping on {}.\n".format(stringOfKeys)
		# 		else:
		# 			annotation = "Hash Aggregate.\n"
		# 	else:
		# 		if "Group Key" in node.attributes:
		# 			stringOfKeys = self.getKeys(node)
		# 			annotation = "Aggregate grouping on {}.\n".format(stringOfKeys)
		# 		else:
		# 			annotation = "Aggregate.\n"
		# 	node.annotations += annotation

		# if nodeType == "Sort":
		# 	annotation = "Sort the table on keys "
		# 	desc = False
		# 	for key in node.attributes['Sort Key']:
		# 		if "DESC" in key:
		# 			desc = True
		# 		else:
		# 			annotation += f"{key}, "
		# 	annotation = annotation[:-2]
		# 	if desc:
		# 		annotation += ' decscendingly.'
		# 	else:
		# 		annotation += ' ascendingly.'
		# 	annotation += '\n\n'
		# 	node.annotations += annotation

		# if nodeType == "Unique":
		# 	annotation = "Remove Duplicates\n"
		# 	node.annotations += annotation

		# if nodeType == "Gather":
		# 	annotation = "Gather.\n"
		# 	node.annotations += annotation

		# if nodeType == "Gather Merge":
		# 	annotation = "Gather Merge operation is performed, combining the output of child nodes.\n"
		# 	node.annotations += annotation

		# if nodeType == "Append":
		# 	annotation = "Append Tables.\n"
		# 	node.annotations += annotation

		# if nodeType == "Bitmap Index Scan":
		# 	annotation = "Bitmap index scan is used as multiple indices are constructed for this table.\n"
		# 	node.annotations += annotation

		# if nodeType == "Bitmap Heap Scan":
		# 	annotation = "Bitmap heap scan is used as multiple indices as constructed. A heap is used to " \
		# 					"sort the indices and quickly cut down the number of tuples scanned.\n "
		# 	node.annotations += annotation

		# if nodeType == "CTE Scan":
		# 	annotation = "CTE Scan is performed on table {}.\n".format(node.attributes['CTE Name'])
		# 	node.annotations += annotation

		# if nodeType == "Foreign Scan":
		# 	annotation = "Foreign Scan is performed on table {}.\n".format(node.attributes['Relation Name'])
		# 	node.annotations += annotation

		# if nodeType == "Limit":
		# 	numRows = node.attributes['Plan Rows']
		# 	annotation = "The Limit operation limits the scanning of the table, with a limitation of {} rows\n".format(numRows)
		# 	node.annotations += annotation

		# if nodeType == "Materialize":
		# 	annotation = "The Materialize operation is performed, storing the result of the child operation in memory.\n"
		# 	node.annotations += annotation

		# if nodeType == "GroupAggregate":
		# 	if "Group Key" in node.attributes:
		# 		stringOfKeys = self.getKeys(node)
		# 		annotation = "The Group Aggregate operation will perform grouping on keys: {}.\n".format(stringOfKeys)
		# 	else:
		# 		annotation = "The Group Aggregate operation will be performed.\n"
		# 	node.annotations += annotation

		# if nodeType == "HashAggregate":
		# 	if "Group Key" in node.attributes:
		# 		stringOfKeys = self.getKeys(node)
		# 		annotation = "The Hash Aggregate operation will perform grouping on keys: {}.\n".format(stringOfKeys)
		# 	else:
		# 		annotation = "The Hash Aggregate operation will be performed.\n"
		# 	node.annotations += annotation