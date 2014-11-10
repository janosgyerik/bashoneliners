Chapter 4: Key Construction Decisions
=====================================

Checklist: Major Construction Practices
---------------------------------------

The following checklist summarizes the specific practices you should
consciously decide to include or exclude during construction.  Details
of the practices are contained throughout Code Complete 2nd Ed.

### Coding

- Have you defined coding conventions for names, comments, and
  formatting?

- Have you defined specific coding practices that are implied by the
  architecture, such as how error conditions will be handled, how
  security will be addressed, and so on?

- Have you identified your location on the technology wave and
  adjusted your approach to match? If necessary, have you identified
  how you will program into the language rather than being limited by
  programming in it?

### Teamwork

- Have you defined an integration procedure, that is, have you defined
  the specific steps a programmer must go through before checking code
  into the master sources?

- Will programmers program in pairs, or individually, or some
  combination of the two?

### Quality Assurance

- Will programmers write test cases for their code before writing the
  code itself?

- Will programmers write unit tests for their code regardless of
  whether they write them first or last?

- Will programmers step through their code in the debugger before they
  check it in?

- Will programmers integration-test their code before they check it
  in?

- Will programmers review or inspect each others' code?

### Tools

- Have you selected a revision control tool?

- Have you selected a language and language version or compiler
  version?

- Have you decided whether to allow use of non-standard language
  features?

- Have you identified and acquired other tools you'll be using editor,
  refactoring tool, debugger, test framework, syntax checker, and so
  on?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
