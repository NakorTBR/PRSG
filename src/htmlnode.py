class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should override to_html().")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        retval = ""
        for key in self.props.keys():
            retval += f" {key}={self.props[key]}"
        
        return retval
    
    def __repr__(self):
        return f"HTMLNode -> Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
    def __eq__(self, other):
        if self.tag != other.tag:
            return False
        if self.value != other.value:
            return False
        
        if self.children is None and other.children is not None:
            return False
        if other.children is None and self.children is not None:
            return False
        
        if self.children is not None and other.children is not None:
            sorted_self_children = sorted(self.children)
            sorted_other_children = sorted(other.children)
            if sorted_self_children != sorted_other_children:
                return False
            if self.props != other.props:
                return False
        
        return True
    
    class LeafNode():
        def __init__(self, value: str, tag: str = None, props: dict = None):
            super().__init__()
            self.value = value
            self.tag = tag
            self.props = props
        
        def to_html(self):
            if self.value == None or self.value == "":
                raise ValueError("All leaf nodes must have a value.")
            if self.tag == None or self.tag == "":
                return self.value
            
            match (self.tag):
                case "p":
                    return f"<p>{self.value}</p>"
                case "a":
                    return f"<a href=\"{self.props['href']}\">{self.value}</a>"
                
            raise ValueError("Unknown HTML tag.")