Chapter 16: Controlling Loops
=============================

Checklist: Loops
----------------

### Loop Selection and Creation

- Is a while loop used instead of a for loop, if appropriate?

- Was the loop created from the inside out?

### Entering the Loop

- Is the loop entered from the top?

- Is initialization code directly before the loop?

- If the loop is an infinite loop or an event loop, is it constructed
  cleanly rather than using a kludge such as for i = 1 to 9999?

- If the loop is a C++, C, or Java for loop, is the loop header
  reserved for loop-control code?

### Inside the Loop

- Does the loop use { and } or their equivalent to prevent problems
  arising from improper modifications?

- Does the loop body have something in it? Is it nonempty?

- Are housekeeping chores grouped, at either the beginning or the end
  of the loop?

- Does the loop perform one and only one function -- as a well-defined
  routine does?

- Is the loop short enough to view all at once?

- Is the loop nested to three levels or less?

- Have long loop contents been moved into their own routine?

- If the loop is long, is it especially clear?

### Loop Indexes

- If the loop is a for loop, does the code inside it avoid monkeying
  with the loop index?

- Is a variable used to save important loop-index values rather than
  using the loop index outside the loop?

- Is the loop index an ordinal type or an enumerated type -- not
  floating point?

- Does the loop index have a meaningful name?

- Does the loop avoid index cross talk?

### Exiting the Loop

- Does the loop end under all possible conditions?

- Does the loop use safety counters -- if you've instituted
  a safety-counter standard?

- Is the loop's termination condition obvious?

- If break or continue are used, are they correct?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
