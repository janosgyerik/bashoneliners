Chapter 32: Self-Documenting Code
=================================

Checklist: Good Commenting Technique
------------------------------------

### General

- Can someone pick up the code and immediately start to understand it?

- Do comments explain the code's intent or summarize what the code
  does, rather than just repeating the code?

- Is the Pseudocode Programming Process used to reduce commenting
  time?

- Has tricky code been rewritten rather than commented?

- Are comments up to date?

- Are comments clear and correct?

- Does the commenting style allow comments to be easily modified?

### Statements and Paragraphs

- Does the code avoid endline comments?

- Do comments focus on why rather than how?

- Do comments prepare the reader for the code to follow?

- Does every comment count? Have redundant, extraneous, and
  self-indulgent comments been removed or improved?

- Are surprises documented?

- Have abbreviations been avoided?

- Is the distinction between major and minor comments clear?

- Is code that works around an error or undocumented feature
  commented?

### Data Declarations

- Are units on data declarations commented?

- Are the ranges of values on numeric data commented?

- Are coded meanings commented?

- Are limitations on input data commented?

- Are flags documented to the bit level?

- Has each global variable been commented where it is declared?

- Has each global variable been identified as such at each usage, by
  a naming convention, a comment, or both?

- Are magic numbers replaced with named constants or variables rather
  than just documented?

### Control Structures

- Is each control statement commented?

- Are the ends of long or complex control structures commented or,
  when possible, simplified so that they don't need comments?

### Routines

- Is the purpose of each routine commented?

- Are other facts about each routine given in comments, when relevant,
  including input and output data, interface assumptions, limitations,
  error corrections, global effects, and sources of algorithms?

### Files, Classes, and Programs

- Does the program have a short document such as that described in the
  Book Paradigm that gives an overall view of how the program is
  organized?

- Is the purpose of each file described?

- Are the author's name, email address, and phone number in the
  listing?

Checklist: Self-Documenting Code
--------------------------------

### Classes

- Does the class's interface present a consistent abstraction?

- Is the class well named, and does its name describe its central
  purpose?

- Does the class's interface make obvious how you should use the
  class?

- Is the class's interface abstract enough that you don't have to
  think about how its services are implemented?

- Can you treat the class as a black box?

### Routines

- Does each routine's name describe exactly what the routine does?

- Does each routine perform one well-defined task?

- Have all parts of each routine that would benefit from being put
  into their own routines been put into their own routines?

- Is each routine's interface obvious and clear?

### Data Names

- Are type names descriptive enough to help document data
  declarations?

- Are variables named well?

- Are variables used only for the purpose for which they're named?

- Are loop counters given more informative names than i, j, and k?

- Are well-named enumerated types used instead of makeshift flags or
  boolean variables?

- Are named constants used instead of magic numbers or magic strings?

- Do naming conventions distinguish among type names, enumerated
  types, named constants, local variables, class variables, and global
  variables?

### Data Organization

- Are extra variables used for clarity when needed?

- Are references to variables close together?

- Are data types simple so that they minimize complexity?

- Is complicated data accessed through abstract access routines
  (abstract data types)?

### Control

- Is the nominal path through the code clear?

- Are related statements grouped together?

- Have relatively independent groups of statements been packaged into
  their own routines?

- Does the normal case follow the if rather than the else?

- Are control structures simple so that they minimize complexity?

- Does each loop perform one and only one function, as a well-defined
  routine would?

- Is nesting minimized?

- Have boolean expressions been simplified by using additional boolean
  variables, boolean functions, and decision tables?

### Layout

- Does the program's layout show its logical structure?

### Design

- Is the code straightforward, and does it avoid cleverness?

- Are implementation details hidden as much as possible?

- Is the program written in terms of the problem domain as much as
  possible rather than in terms of computer-science or
  programming-language structures?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
