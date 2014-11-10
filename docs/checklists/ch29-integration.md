Chapter 29: Integration
=======================

Checklist: Integration
----------------------

### Integration Strategy

- Does the strategy identify the optimal order in which subsystems,
  classes, and routines should be integrated?

- Is the integration order coordinated with the construction order so
  that classes will be ready for integration at the right time?

- Does the strategy lead to easy diagnosis of defects?

- Does the strategy keep scaffolding to a minimum?

- Is the strategy better than other approaches?

- Have the interfaces between components been specified well?
  (Specifying interfaces isn't an integration task, but verifying that
  they have been specified well is.)

### Daily Build and Smoke Test

- Is the project building frequently -- ideally, daily to support
  incremental integration?

- Is a smoke test run with each build so that you know whether the
  build works?

- Have you automated the build and the smoke test?

- Do developers check in their code frequently -- going no more than
  a day or two between check-ins?

- Is a broken build a rare occurrence?

- Do you build and smoke test the software even when you're under
  pressure?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
