Chapter 26: Code Tuning Techniques
==================================

Checklist: Code-Tuning Techniques
---------------------------------

### Improve Both Speed and Size

- Substitute table lookups for complicated logic

- Jam loops

- Use integer instead of floating-point variables

- Initialize data at compile time

- Use constants of the correct type

- Precompute results

- Eliminate common subexpressions

- Translate key routines to assembler

### Improve Speed Only

- Stop testing when you know the answer

- Order tests in case statements and if-then-else chains by frequency

- Compare performance of similar logic structures

- Use lazy evaluation

- Unswitch loops that contain if tests

- Unroll loops

- Minimize work performed inside loops

- Use sentinels in search loops

- Put the busiest loop on the inside of nested loops

- Reduce the strength of operations performed inside loops

- Change multiple-dimension arrays to a single dimension

- Minimize array references

- Augment data types with indexes

- Cache frequently used values

- Exploit algebraic identities

- Reduce strength in logical and mathematical expressions

- Be wary of system routines

- Rewrite routines in line


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
