class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = ""
        if self.props == None:
            return res
        for key,value in self.props.items():
            res += " {}=\"{}\"".format(key, value)
        return res

    def __eq__(self, other):
        return (
        self.tag == other.tag and
        self.value == other.value and
        self.children == other.children and
        self.props == other.props       
        )

    def __repr__(self):
        return "HTMLNode({}, {}, {}, {})".format(self.tag, self.value, self.children, self.props)
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None, _ = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value found") 
        if self.tag == None:
            return self.value
        return "<{}{}>{}</{}>".format(self.tag, self.props_to_html(), self.value, self.tag)

    def __repr__(self):
        return "LeafNode({}, {}, {})".format(self.tag, self.value, self.props)

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None, _ = None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag found" ) 
        if self.children == None:
            raise ValueError("No children found" ) 
        res = "<{}{}>".format( self.tag, self.props_to_html() )
        for child in self.children:
            res += child.to_html()
        res += "</{}>".format( self.tag )
        return res 

    def __repr__(self):
        return "ParentNode({}, {}, {})".format(self.tag, self.children, self.props)


