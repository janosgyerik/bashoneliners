Chapter 11: Power of Variable Names
===================================

Checklist: Naming Variables
---------------------------

### General Naming Considerations

- Does the name fully and accurately describe what the variable
  represents?

- Does the name refer to the real-world problem rather than to the
  programming-language solution?

- Is the name long enough that you don't have to puzzle it out?

- Are computed-value qualifiers, if any, at the end of the name?

- Does the name use Count or Index instead of Num?  Naming Specific
  Kinds Of Data

- Are loop index names meaningful (something other than i, j, or k if
  the loop is more than one or two lines long or is nested)?

- Have all "temporary" variables been renamed to something more
  meaningful?

- Are boolean variables named so that their meanings when they're True
  are clear?

- Do enumerated-type names include a prefix or suffix that indicates
  the category -- for example, Color for Color Red, Color Green, Color
  Blue, and so on?

- Are named constants named for the abstract entities they represent
  rather than the numbers they refer to?

### Naming Conventions

- Does the convention distinguish among local, class, and global data?

- Does the convention distinguish among type names, named constants,
  enumerated types, and variables?

- Does the convention identify input-only parameters to routines in
  languages that don't enforce them?

- Is the convention as compatible as possible with standard
  conventions for the language?

- Are names formatted for readability?  Short Names

- Does the code use long names (unless it's necessary to use short
  ones)?

- Does the code avoid abbreviations that save only one character?

- Are all words abbreviated consistently?

- Are the names pronounceable?

- Are names that could be mispronounced avoided?

- Are short names documented in translation tables?

### Common Naming Problems: Have You Avoided...

- ...names that are misleading?

- ...names with similar meanings?

- ...names that are different by only one or two characters?

- ...names that sound similar?

- ...names that use numerals?

- ...names intentionally misspelled to make them shorter?

- ...names that are commonly misspelled in English?

- ...names that conflict with standard library-routine names or with
  predefined variable names?

- ...totally arbitrary names?

- ...hard-to-read characters?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
