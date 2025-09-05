class Node:
    def __init__(self, key=None, prev=None, next=None, value=None):
        self.key = key
        self.prev = prev
        self.next = next
        self.value = value
    
    def __repr__(self) -> str:
        return f"Node(Key: {self.key}, Value: {self.value})"

class List:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
