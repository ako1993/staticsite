from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("A value is required")
        if self.tag is None:
            return self.value
        else:
            if self.tag == "a":
                result = f"<{self.tag} "
                for k, v in self.props.items():
                    result += f"{k}={v}"
                result += f">{self.value}</{self.tag}>"
                return result
            elif self.tag != "a":
                return f"<{self.tag}>{self.value}</{self.tag}>"
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value},{self.props})"


    

