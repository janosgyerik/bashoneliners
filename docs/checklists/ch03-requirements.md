Chapter 3: Measure Twice Cut Once: Upstream Prerequisites
=========================================================

Checklist: Requirements
-----------------------

The requirements checklist contains a list of questions to ask
yourself about your project's requirements.  This book doesn't tell
you how to do good requirements development, and the list won't tell
you how to do one either.  Use the list as a sanity check at
construction time to determine how solid the ground that you're
standing on is where you are on the requirements Richter scale.  Not
all of the checklist questions will apply to your project.  If you're
working on an informal project, you'll find some that you don't even
need to think about.  You'll find others that you need to think about
but don't need to answer formally.  If you're working on a large,
formal project, however, you may need to consider every one.

### Specific Functional Requirements

- Are all the inputs to the system specified, including their source,
  accuracy, range of values, and frequency?

- Are all the outputs from the system specified, including their
  destination, accuracy, range of values, frequency, and format?

- Are all output formats specified for web pages, reports, and so on?

- Are all the external hardware and software interfaces specified?

- Are all the external communication interfaces specified, including
  handshaking, error-checking, and communication protocols?

- Are all the tasks the user wants to perform specified?

- Is the data used in each task and the data resulting from each task
  specified?

### Specific Non-Functional (Quality) Requirements

- Is the expected response time, from the user's point of view,
  specified for all necessary operations?

- Are other timing considerations specified, such as processing time,
  data-transfer rate, and system throughput?

- Is the level of security specified?

- Is the reliability specified, including the consequences of software
  failure, the vital information that needs to be protected from
  failure, and the strategy for error detection and recovery?

- Is maximum memory specified?

- Is the maximum storage specified?

- Is the maintainability of the system specified, including its
  ability to adapt to changes in specific functionality, changes in
  the operating environment, and changes in its interfaces with other
  software?

- Is the definition of success included? Of failure?

### Requirements Quality

- Are the requirements written in the user's language? Do the users
  think so?

- Does each requirement avoid conflicts with other requirements?

- Are acceptable trade-offs between competing attributes specified—for
  example, between robustness and correctness?

- Do the requirements avoid specifying the design?

- Are the requirements at a fairly consistent level of detail? Should
  any requirement be specified in more detail? Should any requirement
  be specified in less detail?

- Are the requirements clear enough to be turned over to an
  independent group for construction and still be understood?

- Is each item relevant to the problem and its solution? Can each item
  be traced to its origin in the problem environment?

- Is each requirement testable? Will it be possible for independent
  testing to determine whether each requirement has been satisfied?

- Are all possible changes to the requirements specified, including
  the likelihood of each change?

### Requirements Completeness

- Where information isn't available before development begins, are the
  areas of incompleteness specified?

- Are the requirements complete in the sense that if the product
  satisfies every requirement, it will be acceptable?

- Are you comfortable with all the requirements? Have you eliminated
  requirements that are impossible to implement and included just to
  appease your customer or your boss?


Checklist: Architecture
-----------------------

Here's a list of issues that a good architecture should address.  The
list isn't intended to be a comprehensive guide to architecture but to
be a pragmatic way of evaluating the nutritional content of what you
get at the programmer's end of the software food chain.  Use this
checklist as a starting point for your own checklist.

As with the requirements checklist, if you're working on an informal
project, you'll find some items that you don't even need to think
about.  If you're working on a larger project, most of the items will
be useful.

### Specific Architectural Topics

- Is the overall organization of the program clear, including a good
  architectural overview and justification?

- Are major building blocks well defined, including their areas of
  responsibility and their interfaces to other building blocks?

- Are all the functions listed in the requirements covered sensibly,
  by neither too many nor too few building blocks?

- Are the most critical classes described and justified?

- Is the data design described and justified?

- Is the database organization and content specified?

- Are all key business rules identified and their impact on the system
  described?

- Is a strategy for the user interface design described?

- Is the user interface modularized so that changes in it won't affect
  the rest of the program?

- Is a strategy for handling I/O described and justified?

- Are resource-use estimates and a strategy for resource management
  described and justified?

- Are the architecture's security requirements described?

- Does the architecture set space and speed budgets for each class,
  subsystem, or functionality area?

- Does the architecture describe how scalability will be achieved?

- Does the architecture address interoperability?

- Is a strategy for internationalization/localization described?

- Is a coherent error-handling strategy provided?

- Is the approach to fault tolerance defined (if any is needed)?

- Has technical feasibility of all parts of the system been
  established?

- Is an approach to overengineering specified?

- Are necessary buy-vs.-build decisions included?

- Does the architecture describe how reused code will be made to
  conform to other architectural objectives?

- Is the architecture designed to accommodate likely changes?

- Does the architecture describe how reused code will be made to
  conform to other architectural objectives?

### General Architectural Quality

- Does the architecture account for all the requirements?

- Is any part over- or under-architected? Are expectations in this
  area set out explicitly?

- Does the whole architecture hang together conceptually?

- Is the top-level design independent of the machine and language that
  will be used to implement it?

- Are the motivations for all major decisions provided?

- Are you, as a programmer who will implement the system, comfortable
  with the architecture?


Checklist: Upstream Prerequisites
---------------------------------

- Have you identified the kind of software project you're working on
  and tailored your approach appropriately?

- Are the requirements sufficiently well-defined and stable enough to
  begin construction (see the requirements checklist for details)?

- Is the architecture sufficiently well defined to begin construction
  (see the architecture checklist for details)?

- Have other risks unique to your particular project been addressed,
  such that construction is not exposed to more risk than necessary?


Footnote
--------
This material is copied and/or adapted from the Code Complete 2
Website at cc2e.com. This material is Copyright (c) 1993-2004 Steven
C. McConnell. Permission is hereby given to copy, adapt, and
distribute this material as long as this notice is included on all
such materials and the materials are not sold, licensed, or otherwise
distributed for commercial gain.
