# Encapsulation Best Practices in Python: Class Notes for DSA

## Introduction

**Encapsulation** is the practice of bundling data (attributes) and the methods that operate on that data within a single unit (a class), while hiding the internal implementation details from the outside world. In Python, encapsulation helps you:

- Protect your data from unintended modifications
- Enforce business rules and invariants
- Make your code more maintainable and refactorable
- Reduce coupling between different parts of your program

Think of encapsulation as building a "contract" between your class and its users: users interact with the class through a public interface, but they don't need to (and shouldn't) know how the class works internally.

---

## Core Principle 1: Minimize Visibility (Information Hiding)

### The Idea

Only expose what clients *need* to use. Keep everything else hidden.

### Python Conventions

Python doesn't have strict access modifiers like Java (`private`, `protected`), but follows naming conventions:

| Convention | Meaning | Usage |
|-----------|---------|-------|
| `public_attribute` | No prefix | Intended for public use; part of the stable API |
| `_protected_attribute` | Single underscore | Internal to the class; discourage external access (hint: don't touch this) |
| `__private_attribute` | Double underscore | Name-mangled; strongly signals "hands off" |

### Example: Good vs. Poor Encapsulation

**Poor Encapsulation (exposing internal details):**

```python
class Stack:
    def __init__(self):
        self.items = []  # Public! Anyone can do stack.items.pop()
    
    def push(self, value):
        self.items.append(value)

# A user might do this, breaking the stack contract:
stack = Stack()
stack.items = [999]  # Oops! Directly modified internal state
stack.items.reverse()  # Broke the LIFO order
```

**Good Encapsulation (hiding implementation):**

```python
class Stack:
    def __init__(self):
        self._items = []  # Protected; users know not to touch
    
    def push(self, value):
        self._items.append(value)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def is_empty(self):
        return len(self._items) == 0

# Now, users interact only through the public interface
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2 — safe and predictable
```

### Key Takeaway

Use `_` or `__` prefixes to signal "this is internal." This protects the integrity of your data structures, especially important in DSA where the structure's invariants are critical.

---

## Core Principle 2: Maintain Class Invariants

### What is an Invariant?

An **invariant** is a condition that must *always* be true for an object to be in a valid state.

**Examples in DSA:**
- A **heap** must satisfy the heap property (parent ≤ child for min-heap).
- A **binary search tree** must have all left children smaller than the node.
- A **balanced tree** must maintain certain height constraints.

### Your Responsibility

Every public method must:
1. **Validate inputs** before modifying state
2. **Maintain invariants** during operations
3. **Return valid state** after execution

### Example: A Binary Search Tree with Invariants

```python
class BSTNode:
    def __init__(self, value):
        self.value = value
        self._left = None   # Protected; users shouldn't assign directly
        self._right = None
    
    def insert(self, value):
        """Insert a value while maintaining the BST invariant."""
        if value < self.value:
            if self._left is None:
                self._left = BSTNode(value)
            else:
                self._left.insert(value)
        elif value > self.value:
            if self._right is None:
                self._right = BSTNode(value)
            else:
                self._right.insert(value)
        # If value == self.value, we ignore duplicates (a design choice)
    
    def search(self, value):
        """Search while relying on the BST invariant."""
        if value == self.value:
            return True
        elif value < self.value:
            return self._left.search(value) if self._left else False
        else:
            return self._right.search(value) if self._right else False
```

**Why this matters:** By keeping `_left` and `_right` protected, we prevent users from breaking the BST property by assigning nodes arbitrarily.

---

## Core Principle 3: Prefer Immutability When Feasible

### Immutable = Encapsulated

An **immutable object** cannot be changed after creation. This is the strongest form of encapsulation because invariants are guaranteed once and forever.

### Example: A Node Class (Immutable)

```python
class Node:
    def __init__(self, value, next_node=None):
        self._value = value       # Set once, never changed
        self._next = next_node    # Set once, never changed
    
    @property
    def value(self):
        return self._value
    
    @property
    def next(self):
        return self._next
    
    # No setters! Once created, a Node is frozen.

# Usage:
head = Node(1, Node(2, Node(3)))
# We can traverse: head -> next -> next
# But we can't accidentally do: head.next = some_other_node
```

### When to Use Immutability

- **Value objects** (like a `Coordinate(x, y)` in a graph)
- **Nodes in data structures** (linked lists, trees)
- **Results** that should not be accidentally modified

### Trade-off

Immutability is strong for encapsulation but can require creating new objects instead of modifying in place. For DSA, this is usually acceptable because correctness > micro-optimizations.

---

## Core Principle 4: Avoid "Anemic" Getters and Setters

### The Problem

Blindly generating getters and setters for every field defeats encapsulation. It turns your object into a "data bag" instead of a proper abstraction.

### Example: Poor Design (Data Bag)

```python
class Account:
    def __init__(self, balance):
        self._balance = balance
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        self._balance = amount  # No validation! Anyone can set negative balance!

# User can break invariants:
account = Account(100)
account.balance = -500  # Invalid! Breaks the invariant "balance >= 0"
```

### Example: Good Design (Rich Object with Behavior)

```python
class Account:
    def __init__(self, initial_balance):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance
    
    def deposit(self, amount):
        """Deposit money; validates the invariant."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount):
        """Withdraw money; maintains the invariant."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
    
    def balance(self):
        """Query the balance (read-only behavior, not a raw getter)."""
        return self._balance

# Now invariants are enforced:
account = Account(100)
account.deposit(50)        # Valid
account.withdraw(30)       # Valid
# account.withdraw(-10)    # Raises ValueError! Protected!
# account._balance = -500  # Possible but signals bad practice
```

### Key Insight

Instead of `get_value()` / `set_value()`, expose **behavior** like `deposit()`, `withdraw()`, `process()`.

---

## Core Principle 5: Validate Inputs at the Boundary

### Fail Fast

Validate parameters as soon as they enter your class. This prevents invalid state from propagating.

### Example: A Queue with Validation

```python
class Queue:
    def __init__(self, max_size=None):
        if max_size is not None and max_size <= 0:
            raise ValueError("Max size must be positive")
        self._items = []
        self._max_size = max_size
    
    def enqueue(self, item):
        """Add to queue, validating constraints."""
        if item is None:
            raise ValueError("Cannot enqueue None")
        if self._max_size and len(self._items) >= self._max_size:
            raise OverflowError("Queue is at max capacity")
        self._items.append(item)
    
    def dequeue(self):
        """Remove from queue; fail fast on invalid state."""
        if not self._items:
            raise IndexError("Cannot dequeue from empty queue")
        return self._items.pop(0)
```

**Benefit:** Errors are caught immediately, at the moment of violation, making debugging easier.

---

## Core Principle 6: Control Mutability of Exposed State

### The Risk: Leaking Mutable References

Even if your fields are private, you can break encapsulation by returning mutable objects that the caller can modify.

### Example: The Problem

```python
class Graph:
    def __init__(self):
        self._adjacency_list = {}
    
    def get_neighbors(self, node):
        """WARNING: This returns the actual internal list!"""
        return self._adjacency_list.get(node, [])

# User can modify the graph without using add_edge():
graph = Graph()
neighbors = graph.get_neighbors(1)
neighbors.append(999)  # Oops! Modified graph internals
```

### Example: The Solution

```python
class Graph:
    def __init__(self):
        self._adjacency_list = {}
    
    def get_neighbors(self, node):
        """Return a copy, not the original."""
        return list(self._adjacency_list.get(node, []))  # Defensive copy

# OR use a tuple (immutable):
    def get_neighbors_tuple(self, node):
        return tuple(self._adjacency_list.get(node, []))

# Now, users can't secretly modify the graph:
neighbors = graph.get_neighbors(1)
neighbors.append(999)  # This doesn't affect the graph
```

### When to Apply This

- Returning lists, dicts, or sets? Return a copy or tuple.
- Returning custom objects? Return an immutable view if possible.
- Returning primitives (int, str)? Safe to return directly (immutable in Python).

---

## Core Principle 7: Separate Internal Representation from Public API

### Why It Matters

Your public API should never reveal how you store or process data internally. This lets you refactor the implementation without breaking user code.

### Example: Changing Representation

**Version 1: Using a List (Original)**

```python
class PriorityQueue:
    def __init__(self):
        self._items = []  # Internal representation: unsorted list
    
    def enqueue(self, priority, value):
        self._items.append((priority, value))
        self._items.sort()  # Sort after each insertion
    
    def dequeue(self):
        if not self._items:
            raise IndexError("Queue is empty")
        return self._items.pop(0)[1]  # Remove and return highest priority
```

**Version 2: Using a Heap (Improved Implementation)**

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []  # Changed: now using a heap!
    
    def enqueue(self, priority, value):
        heapq.heappush(self._heap, (priority, value))
    
    def dequeue(self):
        if not self._heap:
            raise IndexError("Queue is empty")
        return heapq.heappop(self._heap)[1]
```

**The Point:** Because we encapsulated the internal `_items`, we can swap from a list to a heap without any user code breaking. The public interface (`enqueue`, `dequeue`) remains the same.

---

## Core Principle 8: Use Constructors to Enforce Invariants

### Constructor is the Critical Moment

The constructor is where you establish initial validity. Design it so that:
1. The object cannot be created in an invalid state
2. All required data is provided upfront

### Example: A Coordinate Class

```python
class Coordinate:
    def __init__(self, x, y):
        """Initialize a coordinate; must be valid from the start."""
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("x and y must be numbers")
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def distance_to(self, other):
        """Query method: compute distance to another coordinate."""
        return ((self._x - other._x) ** 2 + (self._y - other._y) ** 2) ** 0.5

# Valid usage:
origin = Coordinate(0, 0)
point = Coordinate(3, 4)

# Invalid usage is prevented:
# bad = Coordinate("not a number", 5)  # TypeError raised immediately
```

**Benefit:** Once a Coordinate is created, you know it's valid. You don't have to worry about invalid coordinates later.

---

## Core Principle 9: Follow the Law of Demeter (Tell, Don't Ask)

### The Idea

An object should only interact with its immediate collaborators, not reach through them.

### Bad: Reaching Through Objects (Violates Encapsulation)

```python
class Student:
    def __init__(self, name, school):
        self._name = name
        self._school = school  # Collaborator

class School:
    def __init__(self, principal):
        self._principal = principal  # Collaborator

class Principal:
    def __init__(self, address):
        self._address = address

# Violation: Reaching through two levels of indirection
principal_address = student._school._principal._address
```

### Good: Tell the Object What You Want

```python
class Student:
    def __init__(self, name, school):
        self._name = name
        self._school = school
    
    def get_principal_address(self):
        """Tell the school to give me the principal's address."""
        return self._school.get_principal_address()

class School:
    def __init__(self, principal):
        self._principal = principal
    
    def get_principal_address(self):
        """Tell the principal to give me the address."""
        return self._principal.get_address()

class Principal:
    def __init__(self, address):
        self._address = address
    
    def get_address(self):
        return self._address

# Good: Ask through the chain of responsibility
principal_address = student.get_principal_address()
```

### Why It Matters

If `Principal` changes its structure, only `School` needs to know. `Student` is unaffected. You've reduced coupling.

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Making Everything Private, But with No Interface

```python
# Bad: Too restrictive, users can't do anything
class LinkedList:
    def __init__(self):
        self.__head = None  # Overly hidden
    
    # No public methods to interact with the list!
    # Users are blocked from using this class.
```

**Fix:** Provide a public interface.

```python
# Good: Hidden implementation, public interface
class LinkedList:
    def __init__(self):
        self._head = None
    
    def append(self, value):
        # Implementation
        pass
    
    def traverse(self):
        # Implementation
        pass
```

### Pitfall 2: Exposing Internal Mutable State

```python
# Bad
class Graph:
    def __init__(self):
        self.adjacency = {}  # Public and mutable!

# User breaks the graph:
graph.adjacency[1] = "not a list!"
```

**Fix:** Hide and protect.

```python
# Good
class Graph:
    def __init__(self):
        self._adjacency = {}
    
    def add_edge(self, u, v):
        # Validation and enforcement
        pass
```

### Pitfall 3: Forgetting to Validate in Constructors

```python
# Bad
class Heap:
    def __init__(self, items):
        self._items = items  # What if items isn't a valid heap?

# Good
class Heap:
    def __init__(self, items=None):
        self._items = []
        if items:
            for item in items:
                self.insert(item)  # Use insert() to enforce heap property
```

---

## Best Practices Checklist for DSA

When you design a data structure class, ask yourself:

- [ ] **Do I expose any `_` or `__` prefixed attributes in my API?** (You shouldn't.)
- [ ] **Can my invariants be violated from outside?** (They shouldn't be.)
- [ ] **Am I returning mutable objects that users can modify?** (Avoid this.)
- [ ] **Do I validate inputs at the boundary?** (Always do this.)
- [ ] **Is my constructor the "moment of truth"?** (Design it well.)
- [ ] **Can I change the internal representation without breaking users?** (Good encapsulation enables this.)
- [ ] **Am I exposing behavior, not data?** (E.g., `insert()` not `set_items()`.)
- [ ] **Would a different data structure break my code?** (Tight coupling is bad.)

---

## Summary

**Encapsulation in Python:**

1. **Hide implementation details** using `_` and `__` prefixes.
2. **Protect invariants** by validating all inputs and maintaining state carefully.
3. **Expose behavior, not data** through meaningful methods.
4. **Enforce validity from construction** onward.
5. **Return copies of mutable objects** to prevent external modification.
6. **Design for change** by separating interface from implementation.

By following these principles, your DSA implementations will be:
- **Correct:** Invariants are maintained.
- **Safe:** Users can't accidentally break your structures.
- **Maintainable:** You can refactor internals without cascading changes.
- **Reusable:** Clear, simple interfaces are easier to use in larger systems.

---

## Further Reading

- Python Data Model: https://docs.python.org/3/reference/datamodel.html
- Collections ABC: https://docs.python.org/3/library/collections.abc.html
- Properties and Descriptors: https://docs.python.org/3/howto/descriptor.html
