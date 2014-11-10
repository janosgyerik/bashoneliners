Chapter 12: Fundamental Data Types
==================================

Checklist: Fundamental Data
---------------------------

### Numbers in General

- Does the code avoid magic numbers?

- Does the code anticipate divide-by-zero errors?

- Are type conversions obvious?

- If variables with two different types are used in the same
  expression, will the expression be evaluated as you intend it to be?

- Does the code avoid mixed-type comparisons?

- Does the program compile with no warnings?

### Integers

- Do expressions that use integer division work the way they're meant
  to?

- Do integer expressions avoid integer-overflow problems?

### Floating-Point Numbers

- Does the code avoid additions and subtractions on numbers with
  greatly different magnitudes?

- Does the code systematically prevent rounding errors?

- Does the code avoid comparing floating-point numbers for equality?

### Characters and Strings

- Does the code avoid magic characters and strings?

- Are references to strings free of off-by-one errors?

- Does C code treat string pointers and character arrays differently?

- Does C code follow the convention of declaring strings to be length
  constant+1?

- Does C code use arrays of characters rather than pointers, when
  appropriate?

- Does C code initialize strings to NULLs to avoid endless strings?

- Does C code use strncpy() rather than strcpy()? And strncat() and
  strncmp()?

### Boolean Variables

- Does the program use additional boolean variables to document
  conditional tests?

- Does the program use additional boolean variables to simplify
  conditional tests?

### Enumerated Types

- Does the program use enumerated types instead of named constants for
  their improved readability, reliability, and modifiability?

- Does the program use enumerated types instead of boolean variables
  when a variable's use cannot be completely captured with TRUE and
  FALSE?

- Do tests using enumerated types test for invalid values?

- Is the first entry in an enumerated type reserved for "invalid"?

### Named Constants

- Does the program use named constants for data declarations and loop
  limits rather than magic numbers?

- Have named constants been used consistently -- not named constants
  in some places, literals in others?

### Arrays

- Are all array indexes within the bounds of the array?

- Are array references free of off-by-one errors?

- Are all subscripts on multidimensional arrays in the correct order?

- In nested loops, is the correct variable used as the array
  subscript, avoiding loop-index cross talk?

### Creating Types

- Does the program use a different type for each kind of data that
  might change?

- Are type names oriented toward the real-world entities the types
  represent rather than toward programminglanguage types?

- Are the type names descriptive enough to help document data
  declarations?

- Have you avoided redefining predefined types?

- Have you considered creating a new class rather than simply
  redefining a type?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
