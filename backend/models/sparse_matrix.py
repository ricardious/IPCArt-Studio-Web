import base64
from graphviz import Source, Digraph


class HeaderList:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.first = None
        self.last = None
        self.size = 0

    def __len__(self):
        return self.size

    def insertHeaderNode(self, new):
        if self.first == None and self.last == None:
            self.first = new
            self.last = new
        else:
            # ---------ASCENDING ORDER INSERTION-----------
            # -- CHECK IF NEW NODE IS LESS THAN FIRST NODE
            if new.id < self.first.id:
                new.next = self.first
                self.first.previous = new
                self.first = new
            # -- CHECK IF NEW NODE IS GREATER THAN LAST NODE
            elif new.id > self.last.id:
                self.last.next = new
                new.previous = self.last
                self.last = new
            # -- OTHERWISE, TRAVERSE LIST TO FIND WHERE TO PLACE NEW HEADER NODE BETWEEN FIRST AND LAST
            else:
                current = self.first
                while current != None:
                    if new.id < current.id:
                        new.next = current
                        new.previous = current.previous
                        current.previous.next = new
                        current.previous = new
                        break
                    elif new.id > current.id:
                        current = current.next
                    else:
                        break
        self.size += 1

    def getHeader(self, id):
        current = self.first
        while current != None:
            if current.id == id:
                return current
            current = current.next
        return None

    def showHeaders(self):
        current = self.first
        while current != None:
            print(str(current.id))
            current = current.next


class HeaderNode:
    def __init__(self, id):
        self.id = id
        self.next = None
        self.previous = None
        self.access = None


class CellNode:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.up = None
        self.down = None
        self.left = None
        self.right = None


class SparseMatrix:
    def __init__(self):
        self.rows = HeaderList("row")
        self.columns = HeaderList("column")

    def insert(self, x, y, value):
        # Create new cell node to add
        new = CellNode(x, y, value)
        # 1. Check if headers for rows or columns already exist in matrix
        cell_x = self.rows.getHeader(x)
        cell_y = self.columns.getHeader(y)

        # 2. Check if row header X exists
        if cell_x == None:
            # If it doesn't exist, create new row header at position X
            cell_x = HeaderNode(x)
            self.rows.insertHeaderNode(cell_x)

        # 2. Check if column header Y exists
        if cell_y == None:
            # If it doesn't exist, create new column header at position Y
            cell_y = HeaderNode(y)
            self.columns.insertHeaderNode(cell_y)

        # 3. Proceed to insert new cell into matrix
        # 3.1 INSERT NEW CELL IN ROW
        # 3.1.1. Check if cell X isn't pointing to any internal node (access)
        if cell_x.access == None:
            cell_x.access = new
        # 3.1.2. If internal node already exists in row, proceed to insert cell in row
        else:
            # 3.1.2.1 If new node's column is less than first internal node's column
            if new.y < cell_x.access.y:
                # NEW -> ACCESS
                new.right = cell_x.access
                # NEW <- ACCESS
                cell_x.access.left = new
                # ROWX -> NEW
                cell_x.access = new
            # 3.1.2.2 If new node's column is greater than last internal node's column
            else:
                # TRAVERSE LEFT TO RIGHT IN ROW
                current = cell_x.access
                while current != None:
                    # If new node's column is less than current node's column
                    if new.y < current.y:
                        # NEW -> CURRENT
                        new.right = current
                        # NEW <- CURRENT
                        new.left = current.left
                        # CURRENT <- NEW
                        current.left.right = new
                        # CURRENT -> NEW
                        current.left = new
                        break
                    # IF NEW NODE'S X and Y POSITION EQUALS CURRENT NODE'S X and Y POSITION
                    elif new.x == current.x and new.y == current.y:
                        # IF WE WANT TO OVERWRITE THE value
                        # current.value = value
                        # IF WE DON'T WANT TO OVERWRITE THE value THEN DO NOTHING
                        break
                    # IF NEW NODE'S Y POSITION IS GREATER THAN LAST NODE'S Y POSITION
                    else:
                        # IF CURRENT NODE'S .RIGHT IS NULL THEN INSERT NEW NODE AT END OF ROW
                        if current.right == None:
                            # CURRENT -> NEW
                            current.right = new
                            # NEW <- CURRENT
                            new.left = current
                            break
                        # IF CURRENT NODE HAS RIGHT NODE (NOT LAST NODE IN ROW)
                        else:
                            # MOVE TO NEXT NODE
                            current = current.right

        # 3.2 INSERT NEW CELL IN COLUMN
        # 3.2.1. Check if cell Y isn't pointing to any internal node (access)
        if cell_y.access == None:
            cell_y.access = new
        # 3.2.2. If internal node already exists in column, proceed to insert cell in column
        else:
            # IF NEW NODE'S ROW IS LESS THAN ACCESS NODE'S ROW
            if new.x < cell_y.access.x:
                # NEW -> ACCESS
                new.down = cell_y.access
                # NEW <- ACCESS
                cell_y.access.up = new
                # ROWY -> NEW
                cell_y.access = new
            # INSERT NEW NODE IN COLUMN (TOP TO BOTTOM MOVEMENT)
            else:
                current2 = cell_y.access
                while current2 != None:
                    # IF NEW NODE'S X POSITION IS LESS THAN CURRENT NODE'S X POSITION
                    if new.x < current2.x:
                        # NEW -> CURRENT2
                        new.down = current2
                        # CURRENT2.UP <- NEW
                        new.up = current2.up
                        # CURRENT2.UP -> NEW
                        current2.up.down = new
                        # NEW <- CURRENT2
                        current2.up = new
                        break
                    # IF NEW NODE'S X and Y POSITION EQUALS CURRENT NODE'S X and Y POSITION
                    elif new.x == current2.x and new.y == current2.y:
                        # IF WE WANT TO OVERWRITE THE value
                        # current2.value = value
                        # IF WE DON'T WANT TO OVERWRITE THE value THEN DO NOTHING
                        break
                    # IF NEW NODE'S X POSITION IS GREATER THAN LAST NODE'S X POSITION
                    else:
                        # IF CURRENT2 NODE'S .DOWN IS NULL THEN INSERT NEW NODE AT END OF COLUMN
                        if current2.down == None:
                            # CURRENT2 -> NEW
                            current2.down = new
                            # NEW <- CURRENT2
                            new.up = current2
                            break
                        # IF CURRENT2 NODE HAS DOWN NODE (NOT LAST NODE IN COLUMN)
                        else:
                            # MOVE TO NEXT NODE
                            current2 = current2.down

    def plot(self):

        dotcode = """digraph G {
    graph [pad=\"0.5\", nodesep=\"1\", ranksep=\"1\"];
    label=\"Sparse Matrix\"
    node [shape=box, height=0.8];\n"""

        # 1. PLOT FROM ROWS
        currentRow = self.rows.first
        rowId = ""
        rowConnections = ""
        innerNodes = ""
        innerDirections = ""
        while currentRow != None:
            first = True
            current = currentRow.access
            # PLOT ROW HEADER
            rowId += (
                "\tRow"
                + str(current.x)
                + '[style="filled" label = "'
                + str(currentRow.id)
                + '" fillcolor="white" group = 0];\n'
            )
            # LINK ROW HEADER WITH FIRST NODE IN ROW (ACCESS)
            if currentRow.next != None:
                rowConnections += (
                    "\tRow"
                    + str(current.x)
                    + " -> Row"
                    + str(currentRow.next.access.x)
                    + ";\n"
                )
            innerDirections += "\t{ rank = same; Row" + str(current.x) + "; "
            while current != None:
                innerNodes += (
                    "\tNodeR"
                    + str(current.x)
                    + "_C"
                    + str(current.y)
                    + '[style="filled" label = "'
                    + str(current.value)
                    + '" fillcolor="'
                    + str(current.value)
                    + '" fontcolor="'
                    + str(current.value)
                    + '" group = '
                    + str(current.y)
                    + "];\n"
                )
                innerDirections += (
                    "NodeR" + str(current.x) + "_C" + str(current.y) + "; "
                )
                # FOR ROW HEADER TO POINT TO FIRST NODE IN ROW
                if first == True:
                    innerNodes += (
                        "\tRow"
                        + str(current.x)
                        + " -> NodeR"
                        + str(current.x)
                        + "_C"
                        + str(current.y)
                        + '[dir=""];\n'
                    )
                    if current.right != None:
                        innerNodes += (
                            "\tNodeR"
                            + str(current.x)
                            + "_C"
                            + str(current.y)
                            + " -> NodeR"
                            + str(current.right.x)
                            + "_C"
                            + str(current.right.y)
                            + ";\n"
                        )
                    first = False
                else:
                    if current.right != None:
                        innerNodes += (
                            "\tNodeR"
                            + str(current.x)
                            + "_C"
                            + str(current.y)
                            + " -> NodeR"
                            + str(current.right.x)
                            + "_C"
                            + str(current.right.y)
                            + ";\n"
                        )
                current = current.right
            currentRow = currentRow.next
            innerDirections += "}\n"

        dotcode += (
            rowId
            + """
    edge[dir="both"];
    """
            + rowConnections
            + """
    edge[dir="both"]
    """
        )

        # 2. PLOT COLUMNS
        currentColumn = self.columns.first
        columnId = ""
        columnConnections = ""
        innerDirections2 = "\t{rank = same; "
        while currentColumn != None:
            first = True
            current = currentColumn.access
            columnId += (
                "\tColumn"
                + str(current.y)
                + '[style="filled" label = "'
                + str(current.y)
                + '" fillcolor="white" group = '
                + str(current.y)
                + "];\n"
            )
            innerDirections2 += "Column" + str(current.y) + "; "
            if currentColumn.next != None:
                columnConnections += (
                    "Column"
                    + str(current.y)
                    + " -> Column"
                    + str(currentColumn.next.access.y)
                    + ";\n"
                )
            while current != None:
                if first == True:
                    dotcode += (
                        "Column"
                        + str(current.y)
                        + " -> NodeR"
                        + str(current.x)
                        + "_C"
                        + str(current.y)
                        + '[dir=""];\n'
                    )
                    if current.down != None:
                        dotcode += (
                            "NodeR"
                            + str(current.x)
                            + "_C"
                            + str(current.y)
                            + " -> NodeR"
                            + str(current.down.x)
                            + "_C"
                            + str(current.down.y)
                            + ";\n"
                        )
                    first = False
                else:
                    if current.down != None:
                        dotcode += (
                            "NodeR"
                            + str(current.x)
                            + "_C"
                            + str(current.y)
                            + " -> NodeR"
                            + str(current.down.x)
                            + "_C"
                            + str(current.down.y)
                            + ";\n"
                        )
                current = current.down
            currentColumn = currentColumn.next
        dotcode += columnId
        dotcode += columnConnections + "\n"
        dotcode += innerDirections2 + "}\n"
        dotcode += innerNodes
        dotcode += innerDirections
        dotcode += "\n}"

        graph = Source(dotcode, format="svg")
        image_data = graph.pipe()

        image_base64 = base64.b64encode(image_data).decode("utf-8")

        return image_base64

    def plot_pixel_art(self):
        dot = Digraph(comment="Sparse Matrix", format="svg")
        dot.attr(rankdir="LR", nodesep="0.5", ranksep="1.0")
        dot.attr("node", shape="box", height="0.8")

        # Add row headers
        currentRow = self.rows.first
        while currentRow:
            dot.node(f"Row{currentRow.id}", label=str(currentRow.id), group="0")
            if currentRow.next:
                dot.edge(f"Row{currentRow.id}", f"Row{currentRow.next.id}")
            currentRow = currentRow.next

        # Add column headers
        currentColumn = self.columns.first
        while currentColumn:
            dot.node(
                f"Column{currentColumn.id}",
                label=str(currentColumn.id),
                group=str(currentColumn.id),
            )
            if currentColumn.next:
                dot.edge(f"Column{currentColumn.id}", f"Column{currentColumn.next.id}")
            currentColumn = currentColumn.next

        # Add internal nodes and connections
        currentRow = self.rows.first
        while currentRow:
            current = currentRow.access
            while current:
                dot.node(f"NodeR{current.x}_C{current.y}", label=str(current.value))
                if current.right:
                    dot.edge(
                        f"NodeR{current.x}_C{current.y}",
                        f"NodeR{current.right.x}_C{current.right.y}",
                    )
                if current.down:
                    dot.edge(
                        f"NodeR{current.x}_C{current.y}",
                        f"NodeR{current.down.x}_C{current.down.y}",
                    )
                current = current.right
            currentRow = currentRow.next

        # Render the graph
        image_data = dot.pipe()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        return image_base64
