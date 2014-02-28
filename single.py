from __future__ import print_function

from functools import total_ordering


class SinglyLinked(object):
    """
    An implementation of a singly-linked-list.  References are kept for both
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
            self.tail.next_node = self.tail = new_node
        self._length += 1

    def append_head(self, new_value):
        """Add a single item to the front of the list in constant time O(1)."""
        new_node = Node(new_value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next_node, self.head = self.head, new_node
        self._length += 1

    def extend(self, values):
        """
        Add all values in a sequence to the end of the list in O(k) where k is
        the _length of the list to add.
        """
        for value in values:
            self.append_tail(value)

    def insert_after(self, node_or_index, value):
        """
        Insert a new node in the list after a known node or index.
        Inserting after a known node is constant time O(1) whereas inserting
        after an index is linear O(n).  Note that when using an index the new
        node will be at index+1.
        """
        try:
            node_or_index.next_node = Node(value, node_or_index.next_node)
        except AttributeError:
            index = node_or_index
            self[index].next_node = Node(value, self[index].next_node)
        self._length += 1

    def remove(self, node_or_index):
        """
        Remove an item from the list by providing either the node to be
        removed, or its index.  Due to the nature of singly linked lists this
        operation is always O(n) when not removing the head (which can be done
        in constant time).
        """
        if isinstance(node_or_index, Node):
            self._remove_by_node(node_or_index)
        else:
            self._remove_by_index(node_or_index)
        self._length -= 1

    def _remove_by_node(self, node_to_remove):
        """Remove node from list."""
        if node_to_remove is self.head:
            node = self.head = self.head.next_node
        else:
            for node in self:
                if node.next_node is node_to_remove:
                    node.next_node = node_to_remove.next_node
                    break
            else:
                raise ValueError("Node not in list.")
        if node_to_remove is self.tail:
            self.tail = node

    def _remove_by_index(self, index):
        """Remove node at index from list."""
        highest_index = len(self)-1
        if index == -1:
            index = highest_index
        if index == 0:
            node = self.head = self.head.next_node
        elif index <= highest_index:
            node = self[index-1]
            node.next_node = self.get_next(node).next_node
        else:
            raise IndexError("List index {} out of range.".format(index))
        if index == highest_index:
            self.tail = node

    def get_next(self, known_node):
        """
        Returns the next node in constant time O(1) when provided with a
        known node.
        """
        return known_node.next_node

    def iter_values(self):
        """An iterator over the values of the list."""
        for node in self:
            yield node.value

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
            raise IndexError("Slicing not available for SinglyLinked object.")
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
            raise IndexError("Slicing not available for SinglyLinked object.")
        elif self.tail is not None and index == -1:
            self.tail.value = value
        elif index < -1:
            raise IndexError("Negative indexes other than -1 not accepted.")
        else:
            for i, node in enumerate(self):
                if i == index:
                    node.value = value
                    break
            else:
                raise IndexError("List assignment index out of range.")

    def __repr__(self):
        string_values = ", ".join(map(repr, self))
        return "<SingleLinkedNaive({})>".format(string_values)

    def __str__(self):
        return repr(self)


@total_ordering
class Node(object):
    def __init__(self, value, link=None):
        self.value = value
        self.next_node = link

    def __repr__(self):
        return "<Node({})>".format(repr(self.value))

    def __str__(self):
        return repr(self)

    def __nonzero__(self):
        return bool(self.value)

    def __eq__(self, value_or_node):
        try:
            return self.value == value_or_node.value
        except AttributeError:
            return self.value == value_or_node

    def __lt__(self, value_or_node):
        try:
            return self.value < value_or_node.value
        except AttributeError:
            return self.value < value_or_node


if __name__ == "__main__":
    a = SinglyLinked(6,5,2,8,45)
    for value in a:
        print(value)


