class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            return

        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next

        if cur is None:
            return

        prev.next = cur.next

    def search_element(self, data: int):
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur = cur.next

    def to_list(self):
        res = []
        cur = self.head
        while cur:
            res.append(cur.data)
            cur = cur.next
        return res

    # 1. Reverse the LinkedList
    def reverse(self):
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # 2. Merge Sort for LinkedList
    @staticmethod
    def _split(head: Node):
        """Split list into two halves. Return (left_head, right_head)."""
        if head is None or head.next is None:
            return head, None

        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        mid = slow.next
        slow.next = None
        return head, mid

    @staticmethod
    def _merge_sorted_nodes(a: Node, b: Node):
        """Merge two sorted linked lists given their heads. Return new head."""
        dummy = Node(0)
        tail = dummy

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        tail.next = a if a else b
        return dummy.next

    @classmethod
    def _merge_sort(cls, head: Node):
        """Return head of sorted list."""
        if head is None or head.next is None:
            return head

        left, right = cls._split(head)
        left = cls._merge_sort(left)
        right = cls._merge_sort(right)
        return cls._merge_sorted_nodes(left, right)

    def sort(self):
        self.head = self._merge_sort(self.head)

    # ---------- TASK 1.3: Merge two sorted LinkedLists ----------
    @staticmethod
    def merge_sorted(list1, list2):
        """Return new LinkedList merged from two sorted LinkedLists."""
        merged = LinkedList()
        merged.head = LinkedList._merge_sorted_nodes(list1.head, list2.head)
        return merged


if __name__ == "__main__":
    # Демонстрація базових операцій
    llist = LinkedList()
    llist.insert_at_beginning(5)
    llist.insert_at_beginning(10)
    llist.insert_at_beginning(15)
    llist.insert_at_end(20)
    llist.insert_at_end(25)

    print("Зв'язний список:")
    llist.print_list()

    llist.delete_node(10)
    print("Після видалення 10:")
    llist.print_list()

    print("Шукаємо 15:")
    element = llist.search_element(15)
    print(element.data if element else "Не знайдено")

    # Реверс та сортування
    print("Реверс списку:")
    llist.reverse()
    print(llist.to_list())

    print("Сортування списку:")
    llist.sort()
    print(llist.to_list())

    print("Злиття двох відсортованих списків:")
    a = LinkedList()
    for x in [1, 4, 7]:
        a.insert_at_end(x)

    b = LinkedList()
    for x in [2, 3, 6, 8]:
        b.insert_at_end(x)

    merged = LinkedList.merge_sorted(a, b)
    print("A:", a.to_list())
    print("B:", b.to_list())
    print("Merged:", merged.to_list())
