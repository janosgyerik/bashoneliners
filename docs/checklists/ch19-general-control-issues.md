Chapter 19: General Control Issues
==================================

Checklist: Control Structure Issues
-----------------------------------

- Do expressions use True and False rather than 1 and 0?

- Are boolean values compared to True and False implicitly?

- Are numeric values compared to their test values explicitly?

- Have expressions been simplified by the addition of new boolean
  variables and the use of boolean functions and decision tables?

- Are boolean expressions stated positively?

- Do pairs of braces balance?

- Are braces used everywhere they're needed for clarity?

- Are logical expressions fully parenthesized?

- Have tests been written in number-line order?

- Do Java tests uses a.equals(b) style instead of a == b when
  appropriate?

- Are null statements obvious?

- Have nested statements been simplified by retesting part of the
  conditional, converting to if-then-else or case statements, moving
  nested code into its own routine, converting to a more
  object-oriented design, or improved in some other way?

- If a routine has a decision count of more than 10, is there a good
  reason for not redesigning it?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
