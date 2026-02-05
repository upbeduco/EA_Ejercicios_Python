# Python ADT Implementation Guide: ABC, Dataclasses, and Pydantic Explained

## What is an Abstract Data Type?

An **Abstract Data Type (ADT)** is a mathematical model that defines a data structure by its *behavior* (operations) rather than its *implementation*. Think of it like an interface or contract: it specifies *what* you can do with the data, not *how* the data is stored internally.

For example, a **Stack** ADT defines operations like `push()`, `pop()`, and `peek()`, but doesn't specify whether it's implemented using an array, linked list, or any other structure.

---

## Core Implementation Tools in Python

Python provides three primary tools for implementing ADTs, each serving different purposes:

### 1. **ABC (Abstract Base Classes)** - The Interface Layer

**Purpose:** Define contracts and enforce structure

**When to use:**
- Creating plugin systems or strategy patterns
- Defining what methods a collection *must* implement
- Building custom collections that need to integrate with Python's ecosystem

**Key characteristics:**
- No validation
- No automatic methods
- Pure interface definition
- Works with `collections.abc` module

**Example:**
```python
from abc import ABC, abstractmethod

class Stack(ABC):
    """Abstract Stack interface"""
    
    @abstractmethod
    def push(self, item):
        """Add item to top of stack"""
        pass
    
    @abstractmethod
    def pop(self):
        """Remove and return top item"""
        pass
    
    @abstractmethod
    def is_empty(self):
        """Check if stack is empty"""
        pass
```

**Best practice for collections:** Inherit from `collections.abc` types like `Sequence`, `MutableMapping`, or `Iterator` to ensure compatibility with built-in Python functions.

```python
from collections.abc import MutableSequence

class MyList(MutableSequence):
    def __init__(self):
        self._data = []
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def __len__(self):
        return len(self._data)
    
    def insert(self, index, value):
        self._data.insert(index, value)
```

---

### 2. **@dataclass** - Internal Storage

**Purpose:** Reduce boilerplate for data-holding classes

**When to use:**
- Internal state management
- Mathematical or algorithmic logic
- Node structures in trees/graphs
- When performance is critical and you control the data source

**Key characteristics:**
- Automatically generates `__init__`, `__repr__`, `__eq__`
- Lightweight and fast
- No runtime validation by default
- Great for trusted internal data

**Example:**
```python
from dataclasses import dataclass

@dataclass
class TreeNode:
    value: int
    left: 'TreeNode' = None
    right: 'TreeNode' = None

@dataclass
class QueueNode:
    data: any
    next: 'QueueNode' = None
    priority: int = 0
```

**Benefits for DSA:**
- Less code to maintain
- Built-in comparison operators (useful for priority queues)
- Easy to make immutable with `frozen=True`

---

### 3. **Pydantic** - External Boundaries

**Purpose:** Validate and serialize data from external sources

**When to use:**
- REST API request/response models
- Message queue payloads
- Any data coming from untrusted sources (user input, network)
- Data Transfer Objects (DTOs) between system layers

**Key characteristics:**
- Runtime type validation
- Automatic JSON serialization/deserialization
- Type coercion (converts compatible types automatically)
- Excellent error messages

**Example:**
```python
from pydantic import BaseModel, Field, validator

class UserDTO(BaseModel):
    user_id: int
    username: str = Field(min_length=3, max_length=20)
    email: str
    age: int = Field(gt=0, lt=150)
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

# Usage
user = UserDTO(
    user_id=1,
    username="alice",
    email="ALICE@example.com",
    age=25
)
print(user.email)  # "alice@example.com" (lowercased)
print(user.model_dump_json())  # Serialize to JSON
```

---

## Quick Reference Table

| Tool | Purpose | Validation | Speed | Best For |
|------|---------|-----------|-------|----------|
| **ABC** | Define interfaces | ❌ None | ⚡ Fastest | Collection protocols, plugin systems |
| **@dataclass** | Store data | ❌ None (static typing only) | ⚡ Very Fast | Internal nodes, algorithm state |
| **Pydantic** | Validate & exchange | ✅ Runtime strict | 🐢 Moderate | DTOs, API models, external data |

---

## Implementing Common ADTs

### Stack Implementation

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ArrayStack:
    """Stack implementation using Python list"""
    _items: List = None
    
    def __post_init__(self):
        if self._items is None:
            self._items = []
    
    def push(self, item) -> None:
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)
```

### Queue Implementation with Linked Nodes

```python
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Node:
    data: Any
    next: Optional['Node'] = None

class LinkedQueue:
    """Queue using linked nodes"""
    
    def __init__(self):
        self._front: Optional[Node] = None
        self._rear: Optional[Node] = None
        self._size = 0
    
    def enqueue(self, item) -> None:
        new_node = Node(data=item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        
        data = self._front.data
        self._front = self._front.next
        self._size -= 1
        
        if self._front is None:
            self._rear = None
        
        return data
    
    def is_empty(self) -> bool:
        return self._front is None
    
    def size(self) -> int:
        return self._size
```

---

## Iteration Patterns for Collections

### Understanding the Iterator Protocol

Python's iteration system is built on two complementary concepts:

1. **Iterable**: An object that can produce an iterator (implements `__iter__()`)
2. **Iterator**: An object that produces values one at a time (implements `__next__()`)

**The Key Rule:** Every iterator is also an iterable (its `__iter__()` returns `self`), but not every iterable is an iterator.

```python
# Interface definitions
class Iterable:
    def __iter__(self):
        """Return an iterator"""
        pass

class Iterator:
    def __iter__(self):
        """Return self"""
        return self
    
    def __next__(self):
        """Return next item or raise StopIteration"""
        pass
```

---

### Pattern 1: Separate Iterator Class

**When to use:** When you need multiple independent iterations over the same collection.

```python
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Node:
    data: Any
    next: Optional['Node'] = None

class LinkedList:
    """Re-iterable linked list with separate iterator"""
    
    def __init__(self):
        self._head: Optional[Node] = None
        self._size = 0
    
    def append(self, item):
        """Add item to end of list"""
        new_node = Node(data=item)
        
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        
        self._size += 1
    
    def __iter__(self):
        """Return a new iterator for this list"""
        return LinkedListIterator(self._head)
    
    def __len__(self):
        return self._size


class LinkedListIterator:
    """Iterator for LinkedList - maintains its own position"""
    
    def __init__(self, head: Optional[Node]):
        self._current = head
    
    def __iter__(self):
        """Iterators must return themselves"""
        return self
    
    def __next__(self):
        """Return next item or raise StopIteration"""
        if self._current is None:
            raise StopIteration
        
        data = self._current.data
        self._current = self._current.next
        return data


# Usage: Multiple independent iterations
linked_list = LinkedList()
for i in range(5):
    linked_list.append(i)

# First iteration
for item in linked_list:
    print(item, end=' ')  # 0 1 2 3 4
print()

# Second iteration (starts fresh)
for item in linked_list:
    print(item, end=' ')  # 0 1 2 3 4
print()

# Nested iteration (both maintain independent positions)
for i in linked_list:
    for j in linked_list:
        print(f"({i},{j})", end=' ')
    print()
```

**Key benefits:**
- ✅ Supports nested loops
- ✅ Multiple simultaneous traversals
- ✅ Thread-safe for reading (each thread gets its own iterator)

---

### Pattern 2: Generator Functions (yield)

**When to use:** When iteration logic is complex or you need lazy evaluation.

**Advantages:**
- No need to write iterator class
- Automatic state management
- Memory efficient (lazy evaluation)
- Cleaner, more readable code

```python
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class TreeNode:
    value: Any
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None

class BinaryTree:
    """Binary tree with generator-based traversals"""
    
    def __init__(self, root: Optional[TreeNode] = None):
        self.root = root
    
    def inorder(self):
        """Generator for inorder traversal (left-root-right)"""
        def _inorder(node):
            if node:
                yield from _inorder(node.left)   # Recursively yield left
                yield node.value                  # Yield current
                yield from _inorder(node.right)   # Recursively yield right
        
        return _inorder(self.root)
    
    def preorder(self):
        """Generator for preorder traversal (root-left-right)"""
        def _preorder(node):
            if node:
                yield node.value
                yield from _preorder(node.left)
                yield from _preorder(node.right)
        
        return _preorder(self.root)
    
    def postorder(self):
        """Generator for postorder traversal (left-right-root)"""
        def _postorder(node):
            if node:
                yield from _postorder(node.left)
                yield from _postorder(node.right)
                yield node.value
        
        return _postorder(self.root)
    
    def level_order(self):
        """Generator for level-order (breadth-first) traversal"""
        if not self.root:
            return
        
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            yield node.value
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    def __iter__(self):
        """Default iteration uses inorder"""
        return self.inorder()


# Usage
#       1
#      / \
#     2   3
#    / \
#   4   5
tree = BinaryTree(
    TreeNode(1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3)
    )
)

print("Inorder:", list(tree.inorder()))      # [4, 2, 5, 1, 3]
print("Preorder:", list(tree.preorder()))    # [1, 2, 4, 5, 3]
print("Postorder:", list(tree.postorder()))  # [4, 5, 2, 3, 1]
print("Level-order:", list(tree.level_order()))  # [1, 2, 3, 4, 5]

# Default iteration
print("Default:", list(tree))  # [4, 2, 5, 1, 3] (inorder)
```

**Key benefits:**
- ✅ Less boilerplate code
- ✅ Automatic state management
- ✅ Memory efficient
- ✅ Easy to implement multiple traversal strategies

---

### Pattern 3: Generator Expressions

**When to use:** Simple transformations or filtering.

```python
class NumberCollection:
    """Collection with generator-based filtering"""
    
    def __init__(self, numbers):
        self._numbers = list(numbers)
    
    def evens(self):
        """Return generator for even numbers"""
        return (n for n in self._numbers if n % 2 == 0)
    
    def odds(self):
        """Return generator for odd numbers"""
        return (n for n in self._numbers if n % 2 == 1)
    
    def squares(self):
        """Return generator for squared values"""
        return (n ** 2 for n in self._numbers)
    
    def filtered(self, predicate):
        """Generic filter using predicate function"""
        return (n for n in self._numbers if predicate(n))
    
    def __iter__(self):
        return iter(self._numbers)


# Usage
numbers = NumberCollection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print("Evens:", list(numbers.evens()))      # [2, 4, 6, 8, 10]
print("Odds:", list(numbers.odds()))        # [1, 3, 5, 7, 9]
print("Squares:", list(numbers.squares()))  # [1, 4, 9, 16, 25, ...]

# Custom predicate
print("Divisible by 3:", list(numbers.filtered(lambda x: x % 3 == 0)))
# [3, 6, 9]
```

---

### Pattern 4: The Self-Iterator (Single-Use)

**When to use:** For single-pass data sources (files, network streams).

**⚠️ Warning:** This pattern makes the object non-re-iterable!

```python
class FileLineReader:
    """Single-use iterator for reading file lines"""
    
    def __init__(self, filename):
        self._filename = filename
        self._file = None
        self._exhausted = False
    
    def __iter__(self):
        """Iterator returns itself"""
        if self._exhausted:
            raise RuntimeError("Iterator already exhausted")
        
        self._file = open(self._filename, 'r')
        return self
    
    def __next__(self):
        """Read next line"""
        if self._file is None:
            raise StopIteration
        
        line = self._file.readline()
        
        if not line:
            self._file.close()
            self._file = None
            self._exhausted = True
            raise StopIteration
        
        return line.rstrip('\n')
    
    def __enter__(self):
        """Support context manager protocol"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure file is closed"""
        if self._file:
            self._file.close()
        return False


# Usage
with FileLineReader('data.txt') as reader:
    for line in reader:
        print(line)
    
    # Second iteration will fail!
    # for line in reader:  # RuntimeError!
    #     print(line)
```

---

### Pattern 5: Combining Iteration with collections.abc

**When to use:** When building collections compatible with Python's standard library.

```python
from collections.abc import Iterator, Iterable
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Node:
    data: Any
    next: Optional['Node'] = None

class CircularBuffer(Iterable):
    """Fixed-size circular buffer with custom iterator"""
    
    def __init__(self, capacity):
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0
    
    def append(self, item):
        """Add item to buffer (overwrites oldest if full)"""
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        
        if self._size < self._capacity:
            self._size += 1
        else:
            # Buffer full, move head forward
            self._head = (self._head + 1) % self._capacity
    
    def __iter__(self):
        """Return iterator over valid items"""
        return CircularBufferIterator(
            self._buffer,
            self._head,
            self._size,
            self._capacity
        )
    
    def __len__(self):
        return self._size
    
    def __repr__(self):
        return f"CircularBuffer({list(self)})"


class CircularBufferIterator(Iterator):
    """Iterator for CircularBuffer"""
    
    def __init__(self, buffer, head, size, capacity):
        self._buffer = buffer
        self._head = head
        self._size = size
        self._capacity = capacity
        self._current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current >= self._size:
            raise StopIteration
        
        index = (self._head + self._current) % self._capacity
        item = self._buffer[index]
        self._current += 1
        return item


# Usage
buffer = CircularBuffer(capacity=3)
buffer.append(1)
buffer.append(2)
buffer.append(3)
print(buffer)  # CircularBuffer([1, 2, 3])

buffer.append(4)  # Overwrites 1
print(buffer)  # CircularBuffer([2, 3, 4])

# Works with all standard Python iteration tools
print(list(buffer))           # [2, 3, 4]
print(sum(buffer))            # 9
print(max(buffer))            # 4
print(4 in buffer)            # True (uses __iter__)
```

---

## Advanced Iteration Techniques

### Using itertools for Collection Operations

```python
from itertools import chain, islice, cycle, tee

class AdvancedCollection:
    """Collection with itertools-powered methods"""
    
    def __init__(self, data):
        self._data = list(data)
    
    def __iter__(self):
        return iter(self._data)
    
    def chain_with(self, other):
        """Chain this collection with another"""
        return chain(self._data, other)
    
    def take(self, n):
        """Take first n items"""
        return list(islice(self._data, n))
    
    def skip(self, n):
        """Skip first n items"""
        return list(islice(self._data, n, None))
    
    def cycle(self, times=None):
        """Repeat collection indefinitely or n times"""
        if times is None:
            return cycle(self._data)
        else:
            return islice(cycle(self._data), len(self._data) * times)
    
    def split(self, n=2):
        """Split into n independent iterators"""
        return tee(iter(self._data), n)


# Usage
col = AdvancedCollection([1, 2, 3, 4, 5])

# Chain multiple collections
combined = list(col.chain_with([6, 7, 8]))
print(combined)  # [1, 2, 3, 4, 5, 6, 7, 8]

# Take/skip
print(col.take(3))  # [1, 2, 3]
print(col.skip(2))  # [3, 4, 5]

# Cycle
print(list(col.cycle(times=2)))  # [1,2,3,4,5,1,2,3,4,5]

# Split for parallel processing
iter1, iter2 = col.split()
print(list(iter1))  # [1, 2, 3, 4, 5]
print(list(iter2))  # [1, 2, 3, 4, 5]
```

---

### Memory-Efficient Lazy Evaluation

```python
class LazyRange:
    """Memory-efficient range-like collection"""
    
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        """Generator-based iteration (no list storage)"""
        current = self.start
        while current < self.stop:
            yield current
            current += self.step
    
    def __len__(self):
        """Calculate length without materializing"""
        return max(0, (self.stop - self.start + self.step - 1) // self.step)
    
    def __getitem__(self, index):
        """Support indexing without storing data"""
        if isinstance(index, slice):
            # Handle slicing
            start, stop, step = index.indices(len(self))
            return LazyRange(
                self.start + start * self.step,
                min(self.start + stop * self.step, self.stop),
                self.step * step
            )
        else:
            # Handle single index
            if index < 0:
                index += len(self)
            if not 0 <= index < len(self):
                raise IndexError("Index out of range")
            return self.start + index * self.step


# Usage - handles millions of numbers without storing them
big_range = LazyRange(0, 1_000_000, 2)
print(len(big_range))      # 500000 (calculated, not stored)
print(big_range[100])      # 200 (calculated on demand)
print(big_range[0:10:2])   # LazyRange(0, 20, 4)

# Only materializes when needed
evens = list(LazyRange(0, 20, 2))
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

---

## Data Transfer Between Layers (DTOs)

### The Problem
In real applications, data moves between layers:
- User input → Web server
- Web server → Business logic
- Business logic → Database
- Microservice A → Microservice B

Each boundary needs validation and potentially transformation.

### The Solution: Pydantic DTOs

```python
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# API Request DTO
class CreateOrderRequest(BaseModel):
    customer_id: int
    items: List[int] = Field(min_length=1)
    shipping_address: str = Field(min_length=10)

# Internal Domain Model (dataclass)
@dataclass
class Order:
    order_id: int
    customer_id: int
    items: List[int]
    shipping_address: str
    created_at: datetime
    status: str = "pending"

# API Response DTO
class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    item_count: int
    status: str
    created_at: datetime
    
    @classmethod
    def from_domain(cls, order: Order):
        """Convert internal model to API response"""
        return cls(
            order_id=order.order_id,
            customer_id=order.customer_id,
            item_count=len(order.items),
            status=order.status,
            created_at=order.created_at
        )
```

### Why This Pattern?

1. **Pydantic at boundaries** validates untrusted input
2. **@dataclass internally** keeps business logic fast
3. **Separation** prevents leaking internal structure to external APIs

---

## Iteration Best Practices Summary

### ✅ DO:

1. **Separate container from iterator** for re-iterable collections
2. **Use generators** (`yield`) for complex traversal logic
3. **Inherit from collections.abc** for automatic protocol compliance
4. **Implement `__len__`** when size is known in O(1) time
5. **Use generator expressions** for simple transformations
6. **Document single-use iterators** clearly

### ❌ DON'T:

1. **Don't make collections self-iterators** (unless truly single-use)
2. **Don't forget to raise `StopIteration`** in `__next__()`
3. **Don't mutate during iteration** (leads to undefined behavior)
4. **Don't forget `__iter__` returns self** in iterator classes
5. **Don't materialize unnecessarily** (defeats lazy evaluation)

---

## Complete Example: Priority Queue with Iteration

```python
from dataclasses import dataclass, field
from typing import Any, List
import heapq

@dataclass(order=True)
class PrioritizedItem:
    """Wrapper for items with priority"""
    priority: int
    item: Any = field(compare=False)

class PriorityQueue:
    """Priority queue with iteration support"""
    
    def __init__(self):
        self._heap: List[PrioritizedItem] = []
        self._counter = 0  # For stable sorting
    
    def push(self, item: Any, priority: int = 0):
        """Add item with priority (lower = higher priority)"""
        entry = PrioritizedItem(priority, item)
        heapq.heappush(self._heap, entry)
    
    def pop(self) -> Any:
        """Remove and return highest priority item"""
        if not self._heap:
            raise IndexError("Pop from empty priority queue")
        return heapq.heappop(self._heap).item
    
    def peek(self) -> Any:
        """View highest priority item without removing"""
        if not self._heap:
            raise IndexError("Peek from empty priority queue")
        return self._heap[0].item
    
    def __iter__(self):
        """Iterate in priority order (non-destructive)"""
        # Create sorted copy
        sorted_items = sorted(self._heap)
        for entry in sorted_items:
            yield entry.item
    
    def __len__(self):
        return len(self._heap)
    
    def __bool__(self):
        return len(self._heap) > 0
    
    def is_empty(self):
        return len(self._heap) == 0


# Usage
pq = PriorityQueue()
pq.push("Low priority task", priority=10)
pq.push("High priority task", priority=1)
pq.push("Medium priority task", priority=5)

# Iterate without destroying
print("All tasks in priority order:")
for task in pq:
    print(f"  - {task}")

# Still have all items
print(f"\nQueue size: {len(pq)}")

# Pop in priority order
print("\nProcessing tasks:")
while pq:
    print(f"  Processing: {pq.pop()}")
```

---

## Practical Guidelines

### For DSA Coursework:
- Use **@dataclass** for node structures (trees, graphs, linked lists)
- Use **generators** for tree/graph traversals
- Use **ABC** when the assignment requires defining an interface
- Focus on algorithmic efficiency, not validation

### For Real Applications:
- Use **Pydantic** for all external data (APIs, config files, user input)
- Use **@dataclass** for internal business logic
- Use **ABC** to define contracts for plugins or strategies
- Use **generators** for memory-efficient data processing

### Performance Tips:
- `@dataclass` with `slots=True` reduces memory usage
- Generators avoid storing entire sequences in memory
- Pydantic validation has overhead—only use at system boundaries
- For hot paths (inner loops), use plain classes or @dataclass

---

## Common Mistakes to Avoid

1. **Using Pydantic everywhere**: It's overkill for internal data structures
2. **Making collections self-iterators**: Breaks nested loops and re-iteration
3. **Forgetting StopIteration**: Results in infinite loops
4. **Not using ABC for collections**: Miss out on free methods from inheritance
5. **Mixing concerns**: Keep DTOs separate from domain logic
6. **Forgetting immutability**: Use `frozen=True` in dataclasses when data shouldn't change
7. **Materializing generators unnecessarily**: Defeats memory efficiency

---

## Summary

- **ADTs separate behavior from implementation**
- **ABC defines interfaces** (what methods exist)
- **@dataclass stores data efficiently** (internal use)
- **Pydantic validates and serializes** (external boundaries)
- **Iterators enable memory-efficient traversal** of collections
- **Generators simplify iteration** implementation
- **Separate container from iterator** for re-iterability
- **DTOs are the contracts** between system layers
- **Inherit from collections.abc** when building custom collections

Choose the right tool for the right job, and your code will be both maintainable and performant.
