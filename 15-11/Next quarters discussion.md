### Feedback

- Compare more with existing work, not necessarily involving static analysis :
  - [Torsten Gurst] *Switch* and *Ferry*
  - [Benjamin Delaware] *Fiat: Deductive Synthesis of Abstract
Data Types in a Proof Assistant*
  - [Ezra Cooper] *The script-writer’s dream : how to write great SQL in your own language, and be sure it will succeed*
- Experiments (not just code fragments) which show the performance improvement brought by our technique on fragments plain Alvin Cheung does not identify.
- Show the idea is not just incremental on top of Alvin Cheung. Clarify the conceptual leap.
- Prepare a show document (or abstract) clarifying the conceptual leap assuming SQL++ can be identified and converted.


### Notes

- Converting to SQL++ through static analysis is possible, at least if the fragment is identified.
- I did not cover your idea :
  - *Web browser code (Javascript) that performs automatic incremental page maintenance. That's what Costas works on now but with FORWARD. Imagine doing it directly in Javascript. The problem setting is virtually identical to what you have done with decorelation. You simply change "decorelation" to "IVM".*

### Issues

 - Amazon has hired me for April (and they would like me to start even sooner if possible), time constraints make this project difficult.

### Options

 1. Leave for Amazon at the end of the fall quarter. Before I leave, prepare the abstract for the PL group and get to execution upon my return. 
 2. Leave for Amazon at the end of winter quarter. Before the end of this quarter, prepare the abstract for PL group. Do the decorrelation paper in Winter (has to be doable in a single quarter + december, given the TAing [no courses]).
 3. Leave for Amazon at the end of spring quarter and go for execution with the PL opportunity, assuming Amazon will go for it. For that last option, I need a letter from you justifying to Amazon why I am taking so long to join them. I also would prefer not to have to TA in this case, as this endeavour will take all of my attention.


### Yannis comments

We need datasets, that either show increase in performance, or productivity. 

They looked into code that are utilizing that are accessing the dataabse un order to fetch data for a clustering alogirthm. Your application would be much faster if you have fused clustering and data access. Name of paper?
