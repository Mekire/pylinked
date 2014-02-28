from __future__ import print_function

from functools import total_ordering


class Double(object):
    """
    An implementation of a Doubly-linked-list.  References are kept for both
    the head and the tail making insertion at the front or the back of the list
    a O(1) constant time operation.
    """
    def __init__(self, *values):
        self._length = 0
        self.head = None
        self.tail = None
        self.extend(values)

    def append_tail(self, new_value):
        """Add a single item to the end of the list in constant time O(1)."""
        new_node = Node(new_value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next_node, new_node.last_node = new_node, self.tail
            self.tail = new_node
        self._length += 1

    def append_head(self, new_value):
        """Add a single item to the front of the list in constant time O(1)."""
        new_node = Node(new_value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.head.last_node, new_node.next_node = new_node, self.head
            self.head = new_node
        self._length += 1

    def extend(self, values):
        """
        Add all values in a sequence to the end of the list in O(k) where k is
        the length of the list to add.
        """
        for value in values:
            self.append_tail(value)

    def insert_after(self, after, value):
        """
        Insert a new node in the list after a known node or index.
        Inserting after a known node is constant time O(1) whereas inserting
        after an index is linear O(n).  Note that when using an index the new
        node will be at index+1.
        """
        node = after if isinstance(after, Node) else self[after]
        new_node = Node(value, node, node.next_node)
        if node is self.tail:
            self.tail = new_node
        else:
            node.next_node.last_node = new_node
        node.next_node = new_node
        self._length += 1

    def insert_before(self, before, value):
        """
        Insert a new node in the list before a known node or index.
        Inserting before a known node is constant time O(1) whereas inserting
        before an index is linear O(n).
        """
        node = before if isinstance(before, Node) else self[before]
        new_node = Node(value, node.last_node, node)
        if node is self.head:
            self.head = new_node
        else:
            node.last_node.next_node = new_node
        node.last_node = new_node
        self._length += 1

    def remove(self, to_remove):
        """
        Remove an item from the list by providing either the node to be
        removed, or its index.  Due to the nature of singly linked lists this
        operation is always O(n) when not removing the head (which can be done
        in constant time).
        """
        node = to_remove if isinstance(to_remove, Node) else self[to_remove]
        if node is not self.head:
            node.last_node.next_node = node.next_node
        else:
            self.head = node.next_node
        if node is not self.tail:
            node.next_node.last_node = node.last_node
        else:
            self.tail = node.last_node
        self._length -= 1

    def get_next(self, known_node):
        """
        Returns the next node in constant time O(1) when provided with a
        known node.
        """
        return known_node.next_node

    def get_previous(self, known_node):
        """
        Returns the previous node in constant time O(1) when provided with a
        known node.
        """
        return known_node.last_node

    def iter_values(self):
        """An iterator over the values of the list."""
        for node in self:
            yield node.value

    def iter_reverse(self):
        """Iterate through the list in reverse."""
        node = self.tail
        while node is not None:
            yield node
            node = node.last_node

    def __eq__(self, other):
        """
        Check if two lists are equivalent based on the order and value
        attributes of the contained nodes.
        """
        try:
            node, other_node = self.head, other.head
        except AttributeError:
            return False
        while True:
            if node.value != other_node.value:
                return False
            if node is self.tail and other_node is other.tail:
                return True
            node = self.get_next(node)
            other_node = other.get_next(other_node)
            if node is None or other_node is None:
                return False

    def __len__(self):
        """Enable use of the len() built in function."""
        return self._length

    def __iter__(self):
        """Make our singly linked list iterable."""
        node = self.head
        while node is not None:
            yield node
            node = node.next_node

    def __getitem__(self, index):
        """
        Getting a node by index is generally a O(n) operation, but constant
        time for the head or tail.  The tail can be retrieved with index -1,
        but no other negative indexes will be accepted.
        """
        if isinstance(index, slice):
            raise IndexError("Slicing not available for Double object.")
        elif self.tail is not None and index == -1:
            return self.tail
        elif index < -1:
            raise IndexError("Negative indexes other than -1 not accepted.")
        else:
            for i, node in enumerate(self):
                if i == index:
                    return node
            raise IndexError("List index out of range.")

    def __setitem__(self, index, value):
        """
        Setting a node by index is generally a O(n) operation, but constant
        time for the head or tail.  The tail can be retrieved with index -1,
        but no other negative indexes will be accepted.
        """
        if isinstance(index, slice):
            raise IndexError("Slicing not available for Double object.")
        elif self.tail is not None and index == -1:
            self.tail.value = value
        elif index < -1:
            raise IndexError("Negative indexes other than -1 not accepted.")
        else:
            for i, node in enumerate(self):
                if i == index:
                    node.value = value
                    return
            raise IndexError("List index {} out of range.".format(index))

    def __repr__(self):
        string_values = ", ".join(map(repr, self))
        return "Double({})".format(string_values)

    def __str__(self):
        return repr(self)


@total_ordering
class Node(object):
    """A node class for use with the Double class.  Boolean and
    comparison operation are based on the value attribute of the class."""
    def __init__(self, value, last_link=None, next_link=None):
        self.value = value
        self.next_node = next_link
        self.last_node = last_link

    def __repr__(self):
        return "Node({})".format(repr(self.value))

    def __nonzero__(self):
        """
        Boolean evaluation of the node is based on the boolean evaluation
        of the node's value attribute.
        """
        return bool(self.value)

    def __eq__(self, value_or_node):
        """Nodes are considered equal if their value attributes are equal."""
        try:
            return self.value == value_or_node.value
        except AttributeError:
            return self.value == value_or_node

    def __lt__(self, value_or_node):
        """
        Less-than determined by comparing value attributes.  All other
        comparison operators created by the functools.total_ordering decorator.
        """
        try:
            return self.value < value_or_node.value
        except AttributeError:
            return self.value < value_or_node


if __name__ == "__main__":
    a = Double(6,5,2,8,45)
    for value in a:
        print(value)


