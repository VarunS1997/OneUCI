from html.parser import HTMLParser
from UDA_debugging import *
import urllib.request

class RetrievalFailure(Exception):
    """ Indicates a failure to get html data  from a source"""
    pass

class NodeType:
    tag, data = range(2)

class HTMLNode:
    def __init__(self, parent, node_type: NodeType, data: str, attrs=None):
        self.__type = node_type
        self.__data = data
        self.__attrs = attrs

        self.__parent = parent
        self.__children = []

        self.__id = ""
        if(attrs != None):
            for attr in attrs:
                if(attr[0].lower() == "id"):
                    debug_print("Found ID: " + attr[1])
                    self.__id = attr[1]

    def add_child(self, childNode):
        self.__children.append(childNode)

    def has_children(self):
        return len(self.__children) > 0

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

    def get_id(self):
        return self.__data

    def get_attributes(self):
        return self.__attrs

    def get_attribute(self, target):
        if(self.__attrs == None):
            return None
        else:
            for attr in self.__attrs:
                if attr[0] == target:
                    return attr[1]
            return None

    def get_parent(self):
        return self.__parent

    def get_children(self):
        return self.__children

    def get_id(self):
        return self.__id

    def find_child(self, attr: str, value, recursive = False):
        for child in self.__children:
            if(child.get_attribute(attr) == value):
                return child

        if(recursive):
            for child in self.__children:
                rresult = child.find_child(attr, value, recursive)
                if(rresult != None):
                    return rresult

        return None

    def __str__(self):
        if(self.__type == NodeType.tag):
            return "[ <{0}> tag, attributes: {1}, children: {2} ]".format(self.__data, self.__attrs, [child.get_data() for child in self.__children])
        elif(self.__type == NodeType.data):
            return "[ <DATA> node, data: " + self.__data + " ]"

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
            return self.get_id() == other.get_id() and self.get_data() == other.get_data()
        elif isinstance(other, str):
            return self.get_id() == other
        else:
            return self.get_id() == str(other)

    def __ne__(self, other):
        if isinstance(other, HTMLNode):
            return self.get_id() != other.get_id() or self.get_data() != other.get_data()
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


class ReferencedHTMLTree(HTMLParser):
    processed_chars = 0

    def __init__(self):
        debug_print("Constructing Tree")
        self.__html = ""

        self.__current_node = None
        self.__top_node = None

        self.__id_nodes = []

        super(ReferencedHTMLTree, self).__init__()
        debug_print("Tree constructed")

    def reset_data_struct(self):
        self.__current_node = None
        self.__top_node = None

        self.__id_nodes = []

    def get_HTML_from_string(self, html_data:str):
        self.__html = html_data

    def get_HTML_from_file(self, filepath:str):
        debug_print("Attempting to read file data")
        try:
            fileobj = open(filepath, "r")
            self.__html = fileobj.read()
        finally:
            if(fileobj):
                fileobj.close()
            if(self.__html == ""):
                debug_print("File data reading failed")
                raise RetrievalFailure("File data reading failed")
            else:
                debug_print("File data reading succeeded")

    def get_HTML_from_url(self, url:str):
        debug_print("Attempting to read url data")
        try:
            socket = urllib.request.urlopen(url)
            self.__html = socket.read().decode(encoding = "utf-8")
        finally:
            if(socket):
                socket.close()
            if(self.__html == ""):
                debug_print("Url data reading failed")
                raise RetrievalFailure("File data reading failed")
            else:
                debug_print("Url data reading succeeded")

    def handle_starttag(self, tag, attrs):
        newNode = None
        debug_print("Found tag: " + tag)

        if(self.__current_node == None):
            newNode = HTMLNode(None, NodeType.tag, tag, attrs)
            self.__top_node = newNode
        else:
            newNode = HTMLNode(self.__current_node, NodeType.tag, tag, attrs)
            self.__current_node.add_child(newNode)

        self.__current_node = newNode

        if (not(newNode.get_id() == "")):
            self.__insert_node(newNode)

    def handle_endtag(self, tag):
        self.__current_node = self.__current_node.get_parent() or self.__current_node

    def handle_data(self, data_in):
        if(data_in.strip() == ""):
            return
        else:
            data_in = data_in.strip()

        debug_print("Found data: " + data_in)
        newNode = HTMLNode(self.__current_node, NodeType.data, data_in)
        if(self.__current_node != None):
            self.__current_node.add_child(newNode)

    def parse_data(self):
        debug_print("Parsing... ")
        self.reset_data_struct()
        ReferencedHTMLTree.processed_chars += len(self.__html)
        self.feed(self.__html)
        debug_print("Parsing: Complete; chars processed: " + str(int(len(self.__html))))

    def find_nodes_by_attribute(self, attr: str, value: str, short=False):
        debug_print("Searching for attribute: {0} == {1} in:\n".format(attr, value))
        debug_print(str(self))
        debug_print("Top Node: " + str(self.__top_node))

        result = []

        to_search = [self.__top_node]

        while(len(to_search) > 0):
            node = to_search.pop()
            debug_print("Scanning node: " + str(node))
            debug_print("Remaining Scans: ", [str(node) for node in to_search])

            if(node.get_attribute(attr) == value):
                debug_print("Attribute found")
                if(short):
                    return [node]
                result.append(node)

            if(node.has_children()):
                to_search = to_search + node.get_children()

        debug_print("No results" if len(result) == 0 else "Results found")
        return result

    def find_nodes_by_tag(self, tag: str):
        debug_print("Searching for tag: {0} in:\n".format(tag))
        debug_print(str(self))
        debug_print("Top Node: " + str(self.__top_node))

        result = []

        to_search = [self.__top_node]

        while(len(to_search) > 0):
            node = to_search.pop()
            debug_print("Scanning node: " + str(node))
            debug_print("Remaining Scans: ", [str(node) for node in to_search])

            if(node.get_type() == NodeType.tag and node.get_data() == tag):
                debug_print("Tag found")
                result.append(node)

            if(node.has_children()):
                to_search = to_search + node.get_children()

        debug_print("No results" if len(result) == 0 else "Results found")
        return result

    def find_nodes_by_attributes(self, attr: [str], value: [str]):
        debug_print("Searching for attributes: {0} == {1} in:\n".format(str(attr), str(value)))
        debug_print(str(self))
        debug_print("Top Node: " + str(self.__top_node))

        result = []

        to_search = [self.__top_node]

        while(len(to_search) > 0):
            node = to_search.pop()
            debug_print("Scanning node: " + str(node))
            debug_print("Remaining Scans: ", [str(node) for node in to_search])

            match = True
            for attribute in attr:
                if(node.get_attribute(attribute) == None):
                    match = False
                    break
            if(match):
                debug_print("Attributes found")
                result.append(node)

            if(node.has_children()):
                to_search = to_search + node.get_children()

        debug_print("No results" if len(result) == 0 else "Results found")
        return result

    def find_node_by_id(self, tid: str):
        debug_print("Searching for " + tid + " in:\n")
        debug_print("".join([str(node) + "\n" for node in self.__id_nodes]))
        pointerIndex = round((len(self.__id_nodes)-1)/2) or 1
        approximated = False

        iteratingDown = None
        jumpingDown = None

        while(pointerIndex > 0 and pointerIndex < len(self.__id_nodes)):
            debug_print("Pointer: {0}, ID Value: {1}".format(str(pointerIndex), self.__id_nodes[pointerIndex].get_id()))
            if(self.__id_nodes[pointerIndex] == tid):
                debug_print("ID found")
                return self.__id_nodes[pointerIndex]
            elif(self.__id_nodes[pointerIndex] > tid):
                if(approximated):
                    if(iteratingDown == False): # we overshot low, but now value is above id
                        debug_print("ID not found")
                        return None
                    else:
                        pointerIndex -= 1
                else:
                    if(jumpingDown == None):
                        jumpingDown = True
                    elif(jumpingDown == False): # too high
                        iteratingDown = True
                        approximated = True
                        continue
                    pointerIndex = round(pointerIndex/2)
            else:
                if(approximated):
                    if(iteratingDown == True): # we overshot high, but now the value is below id
                        debug_print("ID not found")
                        return None
                    else:
                        pointerIndex += 1
                else:
                    if(jumpingDown == None):
                        jumpingDown = False
                    elif(jumpingDown == True): # too low
                        iteratingDown = False
                        approximated = True
                        continue
                    pointerIndex = round(pointerIndex*1.5)

        if(pointerIndex == 0 and self.__id_nodes[pointerIndex] == tid):
            debug_print("ID found")
            return self.__id_nodes[pointerIndex]
        else:
            debug_print("ID not found")
            return None

    def __str__(self):
        if isinstance(self.__top_node, HTMLNode):
            node = self.__top_node
            result = str(node) + "\n"

            to_add = list(node.get_children())

            while(len(to_add) > 0):
                node = to_add.pop()
                result += str(node) + "\n"

                if(node.has_children()):
                    to_add = to_add + node.get_children()

            return result
        else:
            return "<Empty Tree>"

    def __insert_node(self, node: HTMLNode): # insertion sort implementation
        pointerIndex = 0
        inserted = False

        while(pointerIndex < len(self.__id_nodes) and node > self.__id_nodes[pointerIndex]):
            pointerIndex = pointerIndex + 1

        self.__id_nodes.insert(pointerIndex, node)

if __name__ == '__main__':
    print("TESTING FILE")
    urlFormat = input("[URL/FILE]: ").lower() == "url"
    destination = input("Enter test location: ")
    set_debugging(input("Debugging? (Y/N) ").lower() == "y")

    testTree = ReferencedHTMLTree()

    if(urlFormat):
        testTree.get_HTML_from_url(destination)
    else:
        testTree.get_HTML_from_file("testFiles/" + destination)

    testTree.parse_data()

    command = input("[ID/ATTR/PROC/QUIT]: ").lower()
    while(command != "quit"):
        if(command == "id"):
            results = testTree.find_node_by_id(input("ID: "))
            print("Results: ", str(results))
        elif(command == "attr"):
            results = testTree.find_nodes_by_attribute(input("Attribute: "), input("Attribute value: "))
            print("Results: ", [str(node) for node in results])
        elif(command == "proc"):
            print(ReferencedHTMLTree.processed_chars)
        command = input("[ID/ATTR/PROC/QUIT]: ").lower()
    print("TESTS CONCLUDED")
