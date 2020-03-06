import random

class TreeNode():

    def __init__(self, value="", left=None, right=None):
        self.value: str = value
        self.left: TreeNode = left
        self.right: TreeNode = right

    def in_order(self):
        """ in order traversal """
        if self.left:
            yield from self.left.in_order()
        yield self.value
        if self.right:
            yield from self.right.in_order()

    def serialize(self) -> str:
        """ serialize values from tree with inorder traversal """
        string = ""
        for c in self.in_order():
            string += str(c)
        return string

    def insert(self, in_value: str):
        """ insert value in tree with L < R value order """
        if self.value:
            if in_value < self.value:
                if self.left is None:
                    self.left = TreeNode(value=in_value)
                else:
                    self.left.insert(in_value)
            elif in_value > self.value:
                if self.right is None:
                    self.right = TreeNode(value=in_value)
                else:
                    self.right.insert(in_value)
        else:
            self.value = in_value

def deserialize(string: str) -> TreeNode:
    """ deserialize string into tree: use first char as root and insert rest under it """
    root = TreeNode(value=string[0]) if string else TreeNode()
    for c in string[1:]:
        root.insert(c)
    return root


if __name__ == "__main__":

    root = TreeNode(value='2')
    root.insert(in_value='1')
    root.insert(in_value='3')
    root.insert(in_value='5')
    root.insert(in_value='4')
    assert root.serialize() == "12345"

    t = deserialize('31524')
    assert t.serialize() == "12345"

    t = deserialize('235235624')
    assert t.serialize() == "23456"

    t = deserialize('0')
    assert t.serialize() == "0"

    t = deserialize('')
    assert t.serialize() == ""

    # a string permutation should create same tree and string
    string = '123456789'
    t1 = deserialize(string)

    l = list(string)
    random.shuffle(l)
    string = ''.join(l)
    t2 = deserialize(string)

    assert t2.serialize() == t1.serialize()

    pass
