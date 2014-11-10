Chapter 15: Using Conditionals
==============================

Checklist: Conditionals
-----------------------

### if-then Statements

- Is the nominal path through the code clear?

- Do if-then tests branch correctly on equality?

- Is the else clause present and documented?

- Is the else clause correct?

- Are the if and else clauses used correctly -- not reversed?

- Does the normal case follow the if rather than the else?

### if-then-else-if Chains

- Are complicated tests encapsulated in boolean function calls?

- Are the most common cases tested first?

- Are all cases covered?

- Is the if-then-else-if chain the best implementation -- better than
  a case statement?

### case Statements

- Are cases ordered meaningfully?

- Are the actions for each case simple-calling other routines if
  necessary?

- Does the case statement test a real variable, not a phony one that's
  made up solely to use and abuse the case statement?

- Is the use of the default clause legitimate?

- Is the default clause used to detect and report unexpected cases?

- In C, C++, or Java, does the end of each case have a break?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
