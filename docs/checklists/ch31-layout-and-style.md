Chapter 31: Layout And Style
============================

Checklist: Layout
-----------------

### General

- Is formatting done primarily to illuminate the logical structure of
  the code?

- Can the formatting scheme be used consistently?

- Does the formatting scheme result in code that's easy to maintain?

- Does the formatting scheme improve code readability?

### Control Structures

- Does the code avoid doubly indented begin-end or {} pairs?

- Are sequential blocks separated from each other with blank lines?

- Are complicated expressions formatted for readability?

- Are single-statement blocks formatted consistently?

- Are case statements formatted in a way that's consistent with the
  formatting of other control structures?

- Have gotos been formatted in a way that makes their use obvious?

### Individual Statements

- Is white space used to make logical expressions, array references,
  and routine arguments readable?

- Do incomplete statements end the line in a way that's obviously
  incorrect?

- Are continuation lines indented the standard indentation amount?

- Does each line contain at most one statement?

- Is each statement written without side effects?

- Is there at most one data declaration per line?

### Comments

- Are the comments indented the same number of spaces as the code they
  comment?

- Is the commenting style easy to maintain?

### Routines

- Are the arguments to each routine formatted so that each argument is
  easy to read, modify, and comment?

- Are blank lines used to separate parts of a routine?

### Classes, Files and Programs

- Is there a one-to-one relationship between classes and files for
  most classes and files?

- If a file does contain multiple classes, are all the routines in
  each class grouped together and is the class clearly identified?

- Are routines within a file clearly separated with blank lines?

- In lieu of a stronger organizing principle, are all routines in
  alphabetical sequence?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
