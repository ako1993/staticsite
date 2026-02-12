from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required")
        elif  not self.children:
            raise ValueError("Children are required for a parentnode")
        elif self.children is not None:
            result = f"<{self.tag}>"
            for child in self.children:
                node = child.to_html()
                result += node
            return result + f"</{self.tag}>"
        else:
            result = f"<{self.tag}>{self.value}</{self.tag}>"
            return result
        
      
            

            
        
        