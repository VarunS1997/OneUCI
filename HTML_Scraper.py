from html.parser import HTMLParser
import urllib.request

class NodeType:
    tag, data = range(2)

class HTMLNode:
    def __init__(self, parent, node_type: NodeType, data: str, attrs=None):
        self.__type = node_type
        self.__data = data
        self.__attrs = attrs

        self.__parent = parent
        self.__children = []

        self.__id = None
        if(attrs != None):
            for attr in attrs:
                if(attr[0].lower() == "id"):
                    self.__id = attr[0]

    def add_child(self, childNode):
        self.__children.append(childNode)

    def get_type(self):
        return self.__type

    def get_id(self):
        return self.__data

    def get_attributes(self):
        return self.__attrs

    def get_parent(self):
        return self.__parent

    def get_children(self):
        return self.__children

    def get_id(self):
        return self.__id or ""

    def __str__(self):
        return self.__data

    def __gt__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() > other.get_id()
        elif isinstance(other, str):
            return self.get_id() > other
        else:
            return self.get_id() > str(other)

    def __ge__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() >= other.get_id()
        elif isinstance(other, str):
            return self.get_id() >= other
        else:
            return self.get_id() >= str(other)

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() == other.get_id()
        elif isinstance(other, str):
            return self.get_id() == other
        else:
            return self.get_id() == str(other)

    def __ne__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() != other.get_id()
        elif isinstance(other, str):
            return self.get_id() != other
        else:
            return self.get_id() != str(other)

    def __lt__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() < other.get_id()
        elif isinstance(other, str):
            return self.get_id() < other
        else:
            return self.get_id() < str(other)

    def __le__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() <= other.get_id()
        elif isinstance(other, str):
            return self.get_id() <= other
        else:
            return self.get_id() <= str(other)


class HTMLTree(HTMLParser):
    def __init__(self):
        self.__html = ""

        self.__current_node = None
        self.__id_nodes = []

        super(HTMLTree, self).__init__()

    def get_HTML_from_file(self, filepath:str):
        try:
            fileobj = open(filepath, "r")
            self.__html = fileobj.read()
        finally:
            if(fileobj):
                fileobj.close()

    def get_HTML_from_url(self, url:str):
        try:
            socket = urllib.request.urlopen(url)
            self.__html = socket.read()
        finally:
            if(socket):
                socket.close()

    def handle_starttag(self, tag, attrs):
        newNode = None
        print("Found tag: " + tag)

        if(self.__current_node == None):
            newNode = HTMLNode(None, NodeType.tag, tag, attrs)
        else:
            newNode = HTMLNode(self.__current_node, NodeType.tag, tag, attrs)

        self.__current_node = newNode

        if (not(newNode.get_id() == "")):
            self.__insert_node(newNode)

    def handle_endtag(self, tag):
        self.__current_node = self.__current_node.get_parent()

    def handle_data(self, data):
        newNode = HTMLNode(self.__current_node, NodeType.data, data)
        if(self.__current_node != None):
            self.__current_node.add_child(newNode)

    def parse_data(self):
        self.feed(self.__html)

    def find_node_by_id(self, id: str):
        pointerIndex = round(len(self.__id_nodes)/2)
        approximated = False
        result = None
        goingDown = None

        while(pointerIndex >= 0 and pointerIndex < len(self.__id_nodes)):
            print("pointer: " + str(pointerIndex))
            if(self.__id_nodes[pointerIndex] == id):
                return self.__id_nodes[pointerIndex]
            elif(self.__id_nodes[pointerIndex] > id):
                if(approximated):
                    if(goingDown == True): # we were going up, but now our values are higher than our target
                        return None
                    else:
                        pointerIndex += 1
                else:
                    if(goingDown == None):
                        goingDown = True
                    elif(goingDown == False): # too high
                        approximated = true
                    pointerIndex = round(pointerIndex/2)
            else:
                if(approximated):
                    if(goingDown == False): # we were going down, but now our values are lower than our target
                        return None
                    else:
                        pointerIndex -= 1
                else:
                    if(goingDown == None):
                        goingDown = False
                    elif(goingDown == True): # too low
                        approximated = true
                    pointerIndex = pointerIndex*1.5
        return None

    def __insert_node(self, node: HTMLNode): # insertion sort implementation
        pointerIndex = 0
        inserted = False

        while(pointerIndex < len(self.__id_nodes) and node > self.__id_nodes[pointerIndex]):
            pointerIndex = pointerIndex + 1

        self.__id_nodes.insert(pointerIndex, node)
