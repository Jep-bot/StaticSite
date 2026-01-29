class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError

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

    def __init__(self, tag, value, _ = None , props = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            return ValueError
        if self.tag == None:
            return self.value
        return "<{}{}>{}</{}>".format(self.tag, self.props_to_html(), self.value, self.tag)

    def __repr__(self):
        return "HTMLNode({}, {}, {} )".format(self.tag, self.value, self.props)
