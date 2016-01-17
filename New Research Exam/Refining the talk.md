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

We can present the motivation by first showing it's impact and 

##### Background

In our example, the background is used to present the motivation. The quesiton to ask, is this really necessary?



#### Slides

 - Database Applications Are Everywhere
 - Database applications suffer big performance problems
 - App Client - Database Server Architecture
 - Holistic Optimization
 - Tuple at a time example
   - With queries only
   - With queries and programs
 - Query synthesis
 - Batching
 - LINQ
 - FORWARD


### Section 

For each main section, we want to :

 1. Show the running example snippet, if it's a real world example or not, making sure the schema is appropriately labelled, and specify which programming language it is written with.
 2. Show how the particular code fragment is inefficient (the sources of inefficiencies).
 3. Show the expected output for the snippet, and explain why the new snippet is more efficient (skip this step for Forward).
 4. Go through the process of rewriting/compilation into a more efficient form. This description should cover the main components of the rewriting, without too much focus on the details of a particular section. Details will come with more specific questions.
 5. Outline the pros of this technique (this section is technique specific), for example, for query synthesis, show how other snippets can be converted as well (selection and projection). For query batching, show how that the technique can also be applied to insertions.
 6. Provide pros & cons of the technique, based on three criteria
   - Nested Data : can optimize code fragments where the result of the query processing contains a nested collection.
   - Transform time : time to transform a single code fragment into its optimized form.
   - Applicability : restrictions on the source program on top of which the optimization is applied.
   - Fragment Characteristics : characteristics of the fragments that can be rewritten using the technique.