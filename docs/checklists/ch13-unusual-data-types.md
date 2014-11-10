Chapter 13: Unusual Data Types
==============================

Checklist: Considerations In Using Unusual Data Types
-----------------------------------------------------

### Structures

- Have you used structures instead of naked variables to organize and
  manipulate groups of related data?

- Have you considered creating a class as an alternative to using
  a structure?

### Global Data

- Are all variables local or class-scope unless they absolutely need
  to be global?

- Do variable naming conventions differentiate among local, class, and
  global data?

- Are all global variables documented?

- Is the code free of pseudoglobal data-mammoth objects containing
  a mishmash of data that's passed to every routine?

- Are access routines used instead of global data?

- Are access routines and data organized into classes?

- Do access routines provide a level of abstraction beyond the
  underlying data-type implementations?

- Are all related access routines at the same level of abstraction?

### Pointers

- Are pointer operations isolated in routines?

- Are pointer references valid, or could the pointer be dangling?

- Does the code check pointers for validity before using them?

- Is the variable that the pointer references checked for validity
  before it's used?

- Are pointers set to NULL after they're freed?

- Does the code use all the pointer variables needed for the sake of
  readability?

- Are pointers in linked lists freed in the right order?

- Does the program allocate a reserve parachute of memory so that it
  can shut down gracefully if it runs out of memory?

- Are pointers used only as a last resort, when no other method is
  available?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
