Chapter 25: Code-Tuning Strategies
==================================

Checklist: Code-Tuning Strategy
-------------------------------

### Overall Program Performance

- Have you considered improving performance by changing the program
  requirements?

- Have you considered improving performance by modifying the program's
  design?

- Have you considered improving performance by modifying the class
  design?

- Have you considered improving performance by avoiding operating
  system interactions?

- Have you considered improving performance by avoiding I/O?

- Have you considered improving performance by using a compiled
  language instead of an interpreted language?

- Have you considered improving performance by using compiler
  optimizations?

- Have you considered improving performance by switching to different
  hardware?

- Have you considered code tuning only as a last resort?

### Code-Tuning Approach

- Is your program fully correct before you begin code tuning?

- Have you measured performance bottlenecks before beginning code
  tuning?

- Have you measured the effect of each code-tuning change?

- Have you backed out the code-tuning changes that didn't produce the
  intended improvement?

- Have you tried more than one change to improve performance of each
  bottleneck, i.e., iterated?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
