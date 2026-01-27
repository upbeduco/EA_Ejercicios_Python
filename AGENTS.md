# General Guidelines for the Project

This is an educational set of examples and exercises about data structures and algorithms based on the Sedgewick "Algorithms, 4th Edition" textbook.

## Project Context

- **Primary Reference**: Sedgewick & Wayne - Algorithms, 4th Edition (https://algs4.cs.princeton.edu/home/)
- **Primary Libraries**: 
  - `algs4` (Python port of textbook algorithms)
  - `introcs` (Princeton's standard I/O libraries)
- **Module Structure**: 
  - `ea01_ADT/`: Abstract Data Types and their representations
  - `ea02_EstructurasBasicas/`: Basic data structures (lists, queues, stacks)
  - `ea03_AnalisisDeAlgoritmos/`: Algorithm analysis and complexity
  - `ea04_MétodosDeOrdenación/`: Sorting algorithms
  - `ea05_MétodosDeSelección/`: Selection algorithms and priority queues
  - `ea06_MétodosDeBúsqueda/`: Search algorithms and symbol tables
  - `ea07_Grafos/`: Graph algorithms

## Coding Guidelines

- Follow standard Python naming conventions (snake_case for functions/attributes, PascalCase for classes)
- Include comprehensive docstrings for all classes, functions, and methods using NumPy/SciPy docstring style
- When defining ADTs, follow proper encapsulation of internal state (use `_` prefix for private attributes)
- Implementations must include an `if __name__ == '__main__':` block with assertion-based tests demonstrating basic functionality
- **Do not use specialized testing frameworks** (pytest, unittest, etc.); use plain `assert` statements instead
- Use type hints where applicable (especially for method signatures)

## Language & Documentation

- Code comments and docstrings should be in English (per the provided examples)
- Attribute descriptions in docstrings should use the format:
  ```
  Atributos/Attributes
  ----------
  _attribute_name : Description
  ```

## ADT Implementation Patterns

- Use Abstract Base Classes (ABC) for defining interfaces and abstract methods
- Concrete implementations should use either regular classes or `@dataclass` decorator
- Encapsulate internal state with private attributes (prefix `_`)
- Implement iteration protocols (`__iter__`, `__next__`) for collection types
- Implement standard dunder methods (`__len__`, `__str__`, `__repr__`, etc.) where appropriate
- For mathematical ADTs, implement operator overloading (`__add__`, `__sub__`, `__abs__`, etc.)

## Testing Philosophy

- Tests must be self-contained within the module using `if __name__ == '__main__':`
- Use assertions to validate expected behavior
- Example pattern:
  ```python
  if __name__ == '__main__':
      # Test creation and basic operations
      obj = MyADT()
      assert obj.operation() == expected_value
      assert len(obj) == 0
  ```

## Dependencies & Environment

- Python 3.10+ (Note: pygame only supports up to Python 3.10)
- Required packages: `algs4`, `numpy`, `pygame`
- Linux users must have `python3-tk` installed
- Additional resources: Download and install `introcs-1.0` from https://introcs.cs.princeton.edu/python/code/dist/introcs-1.0.zip

