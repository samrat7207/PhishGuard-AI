class Stack:
    """DFS Endpoint Crawler Memory (LIFO Stack)"""
    def __init__(self):
        self.items = []

    def push(self, url):
        if url:
            self.items.append(url)

    def pop(self):
        return self.items.pop() if not self.is_empty() else ""

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    """FIFO Target Inspection Buffer (FIFO Queue)"""
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        if item:
            self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if not self.is_empty() else ""

    def is_empty(self):
        return len(self.items) == 0


class ThreatNode:
    """Singly Linked List Finding Node"""
    def __init__(self, severity, title, endpoint, cve):
        self.severity = severity
        self.title = title
        self.endpoint = endpoint
        self.cve = cve
        self.next = None


class VulnLinkedList:
    """Singly Linked List Threat Memory Engine"""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, severity, title, endpoint, cve):
        new_node = ThreatNode(severity, title, endpoint, cve)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append({
                "severity": current.severity,
                "title": current.title,
                "endpoint": current.endpoint,
                "cve": current.cve
            })
            current = current.next
        return result