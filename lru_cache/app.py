from llist import List, Node

class LRUCache:
    # Linked list data structure to store the least recently used functionality
    linked_list = None

    # Hash map data structure to store key to reference (address of each node object)
    hash_map = None

    def __init__(self):
        self.linked_list = List()
        self.hash_map = {}

    def _delink_node(self, ref: Node) -> bool: # returns if operation was successful or not
        try:
            prev = ref.prev
            nxt  = ref.next

            # If ref is the head
            if prev is None:
                self.linked_list.head = nxt
            else:
                prev.next = nxt

            # If ref is the tail
            if nxt is None:
                self.linked_list.tail = prev
            else:
                nxt.prev = prev

            # fully detach
            ref.prev = None
            ref.next = None
            return True
        except Exception as e:
            print(e)
            return False

    def get(self, key: int) -> int | None:
        if key not in self.hash_map:
            return None
        
        ref = self.hash_map[key]

        # Move the node to the start of the linked list to maintain LRU property
        if not self._delink_node(ref):
            return None
        
        old_head = self.linked_list.head
        ref.prev = None
        ref.next = old_head
        if not old_head:
            # list became empty after delink, this node is both head and tail
            self.linked_list.tail = ref
        else:
            old_head.prev = ref
        
        self.linked_list.head = ref
        return ref.value

    def put(self, key: int, value: int) -> None:
        if key in self.hash_map:
            return

        old_head = self.linked_list.head
        new_node = Node(key=key, value=value, prev=None, next=old_head)

        if old_head:
            old_head.prev = new_node
        else:
            # list was empty → this node is also the tail
            self.linked_list.tail = new_node

        self.linked_list.head = new_node
        self.hash_map[key] = new_node

    def print(self) -> None:
        curr = self.linked_list.head
        while curr:
            print(curr.value)
            curr = curr.next

'''
o = LRUCache()
o.put(1, 1)
o.put(2, 2)
o.put(3, 3)
print("-----")
o.print()
print("GET 2 -----")
print(o.get(2))
print("-----")
o.print()
print("GET 1 -----")
print(o.get(1))
print("-----")
o.print()
print("GET 3 -----")
print(o.get(3))
print("-----")
o.print()
print("-----")
'''
