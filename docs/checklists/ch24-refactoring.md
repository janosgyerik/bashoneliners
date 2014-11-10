Chapter 24: Refactoring
=======================

Reasons to Refactor
-------------------

- Code is duplicated

- A routine is too long

- A loop is too long or too deeply nested

- A class has poor cohesion

- A class interface does not provide a consistent level of abstraction

- A parameter list has too many parameters

- Changes within a class tend to be compartmentalized

- Changes require parallel modifications to multiple classes

- Inheritance hierarchies have to be modified in parallel

- Related data items that are used together are not organized into
  classes

- A routine uses more features of another class than of its own class

- A primitive data type is overloaded

- A class doesn't do very much

- A chain of routines passes tramp data

- A middle man object isn't doing anything

- One class is overly intimate with another

- A routine has a poor name

- Data members are public

- A subclass uses only a small percentage of its parents' routines

- Comments are used to explain difficult code

- Global variables are used

- A routine uses setup code before a routine call or takedown code
  after a routine call

- A program contains code that seems like it might be needed someday

Summary of Refactorings
-----------------------

### Data Level Refactorings

- Replace a magic number with a named constant

- Rename a variable with a clearer or more informative name

- Move an expression inline

- Replace an expression with a routine

- Introduce an intermediate variable

- Convert a multi-use variable to a multiple single-use variables

- Use a local variable for local purposes rather than a parameter

- Convert a data primitive to a class

- Convert a set of type codes to a class

- Convert a set of type codes to a class with subclasses

- Change an array to an object

- Encapsulate a collection

- Replace a traditional record with a data class

### Statement Level Refactorings

- Decompose a boolean expression

- Move a complex boolean expression into a well-named boolean function

- Consolidate fragments that are duplicated within different parts of
  a conditional

- Use break or return instead of a loop control variable

- Return as soon as you know the answer instead of assigning a return
  value within nested if-then-else statements

- Replace conditionals with polymorphism (especially repeated case
  statements)

- Create and use null objects instead of testing for null values

### Routine Level Refactorings

- Extract a routine

- Move a routine's code inline

- Convert a long routine to a class

- Substitute a simple algorithm for a complex algorithm

- Add a parameter

- Remove a parameter

- Separate query operations from modification operations

- Combine similar routines by parameterizing them

- Separate routines whose behavior depends on parameters passed in

- Pass a whole object rather than specific fields

- Pass specific fields rather than a whole object

- Encapsulate downcasting

### Class Implementation Refactorings

- Change value objects to reference objects

- Change reference objects to value objects

- Replace virtual routines with data initialization

- Change member routine or data placement

- Extract specialized code into a subclass

- Combine similar code into a superclass

### Class Interface Refactorings

- Move a routine to another class

- Convert one class to two

- Eliminate a class

- Hide a delegate

- Replace inheritance with delegation

- Replace delegation with inheritance

- Remove a middle man

- Introduce a foreign routine

- Introduce a class extension

- Encapsulate an exposed member variable

- Remove Set() routines for fields that cannot be changed

- Hide routines that are not intended to be used outside the class

- Encapsulate unused routines

- Collapse a superclass and subclass if their implementations are very
  similar

### System Level Refactorings

- Duplicate data you can't control

- Change unidirectional class association to bidirectional class
  association

- Change bidirectional class association to unidirectional class
  association

- Provide a factory routine rather than a simple constructor

- Replace error codes with exceptions or vice versa

Checklist: Refactoring Safely
-----------------------------

- Is each change part of a systematic change strategy?

- Did you save the code you started with before beginning refactoring?

- Are you keeping each refactoring small?

- Are you doing refactorings one at a time?

- Have you made a list of steps you intend to take during your
  refactoring?

- Do you have a parking lot so that you can remember ideas that occur
  to you mid-refactoring?

- Have you retested after each refactoring?

- Have changes been reviewed if they are complicated or if they affect
  mission-critical code?

- Have you considered the riskiness of the specific refactoring, and
  adjusted your approach accordingly?

- Does the change enhance the program's internal quality rather than
  degrading it?

- Have you avoided using refactoring as a cover for code and fix or as
  an excuse for not rewriting bad code?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
