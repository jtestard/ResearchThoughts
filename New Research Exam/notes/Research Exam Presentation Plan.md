# Research Exam Presentation Plan

The goal of this plan is to provide an outline on :

 - What the topic will be
 - What the goals of the presentation will be
 - Should contain enough information to assess if a presentation which follows this outline will successfully meet the requirements of the research exam.

## Requirements of the research exam

The requirements of the research exam are as follows :

 - Depth. The research exam verifies the student's ability to identify challenges and open problems in a focused area. It is not required that the research exam and the thesis be in the same area. Preparation for the research exam should teach students how to navigate, acquire depth of knowledge, and perform critical analysis in a given research area; the exam should verify such abilities.
   - *The topic of holistic optimization constitutes the focused area. The problem is holisitic optimization of analytic reports. We also need to identify challenges. The challenges will match those of the focused area as well as the complex query aspect, which can be the focus of the talk*.
 - Breadth. The oral part of the research exam verifies the student's breadth of knowledge. Passing the research exam and the course breadth requirements enables CSE graduates to perform research in a variety of topics, both during and after the completion of their studies.
   - *Make sure that any topic discussed during the exam is understood in advance, otherwise nothing of note*.
 - The research exam will have the attributes of a "creative survey". A study list will be defined by the student and the research exam committee. The student is expected to survey the area, identify key themes, and observe open/future directions. It is strongly advised that the exam be more than "the first paper" of the student and its related work.
   - *Before meeting with Ranjit, want to make sure we have identified key themes (impedance mismatch, execution distribution, declarative/imperative specification).*

## Topic

Holistic Optimization of Database applications, in particular in the context of analytics. 


### Jianguo's idea
 - Problem Outline : using SSD's characteristics for algorithm design in IR
 - Background
 - Problem 1 : List Intersection
   - Previous Solutions (HDD)
   - Our Solution
 - Problem 2 : Index Maintenance
   - Previous Solutions
   - Our Solution
 - Problem 3 : Index Cache
   - Previous Solutions
   - Our Solution
 - Conclusion

### My Idea

 1. Motivation : database applications suffer from poor performance
   - because high performance requires better DB expertise.
   - because low performance queries are often easier and more straightforward to write.
 - Background
   - What is the impedance mismatch problem
    - Nested Object data structure vs flat relational tables
    - distribution and copy of data (app server memory and database)
    - declarative vs imperative programming language
 - ORMs to the rescue
    - single language access
    - location transparency
    - imperative, familiar code style	
 - Static Analysis
   - StatusQuo
   - DBridge
 - Dynamic Analysis
   - Switch
 - Semi-structured Declarative Queries
   - Forward : single query can fully specify data needs of an application
 - Conclusion
   - Imperative specification is bad. Declarative is better
   - Let compiler/runtime figure out **how** and **where** to execute your queries.
   - Two solutions :
     - Infer declarative code from imperative code
     - Write using a semi-structured query language

### Flow of the talk

 - Impedance mismatch
 - One popular solution : ORMs
 - Query decorrelation
 - ORMs cause inefficiencies
 - Program Rewriting is the solution
 - Static Analysis
   - StatusQuo
   - DBridge
 - Deep Embedding
   - Switch
 - Single Semi-structured Query
   - Forward
 - Conclusion

## Refining the talk

At this point we have the sketch of a research exam :

 - the problem introduced is known
 - the conclusion/message we want to send is known
 - the details of each previous work is known (up to an extent)
 - the comparisons of the different approaches is known, up to some extent.

What is missing is the clarity with which the message will be understood by the audience, and the balance between :

 - breadth
 - depth
 - big picture and take away from the talk

Taking example from Jianguo :

### Introduction

In Jianguo's talk :

 - **Intro** is detail-free, no examples, no specifics about the meat (sub-problems covered in the talk), focuses on a motivation and research opportunity.
 - **Background** focuses on two key technologies which form to the focus of the talk.

##### Motivation

In our example, the motivation is increased performance in database applications due to bad application programs. We do not yet give a good example of the impact of this motivation.

 - Is performance in database applications critical?
 - Is performance loss due to bad application programs very frequent?
 - Is this kind of bad program the responsability of the programmer?

##### Background

In our example, the ba