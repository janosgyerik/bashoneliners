Chapter 17: Unusual Control Structures
======================================

Checklist: Unusual Control Structures
-------------------------------------

### return

- Does each routine use return only when necessary?

- Do returns enhance readability?

### Recursion

- Does the recursive routine include code to stop the recursion?

- Does the routine use a safety counter to guarantee that the routine
  stops?

- Is recursion limited to one routine?

- Is the routine's depth of recursion within the limits imposed by the
  size of the program's stack?

- Is recursion the best way to implement the routine? Is it better
  than simple iteration?

### goto

- Are gotos used only as a last resort, and then only to make code
  more readable and maintainable?

- If a goto is used for the sake of efficiency, has the gain in
  efficiency been measured and documented?

- Are gotos limited to one label per routine?

- Do all gotos go forward, not backward?

- Are all goto labels used?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
