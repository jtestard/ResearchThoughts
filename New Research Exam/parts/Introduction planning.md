### Running Example

Running example will be a web analytics application.


|     Running Example     |                      Displays relational data                     |                       Displays nested data                      |                               Use Ruby                              |                     Use Java                     |
|:--------:|:-----------------------------------------------------------------:|:---------------------------------------------------------------:|:-------------------------------------------------------------------:|:------------------------------------------------:|
| In Favor | All four covered techniques can run on the running example easily (10) | Showcases benefit of Forward. Makes a good case for future work | Existing code for analytics  application is in ruby Code is shorter | Same fragment can be used  for every application |
|  Against |                        Needs to be created                        |     Introduces a dimension not  existent for other solutions    |         Not clear how to apply  other solutions on Ruby code        |                     Needs to be created                     |

Possible Solutions : 

 - Relational example with Java only
 - Nested example with Java only
 - Both : intro contains pure relational example. Magic Decorrelation will also use pure relational. When showing FORWARD, show relational example works. Show a change to the application, show nested example in Java. Show FORWARD can also handle it. When demonstrating Sudarshan and Cheung, show the relational example works, and explain that for the nested example, applicability is unknown. 

Should the example contain an ORM?

 - In favor : reduces #lines of code, used by Cheung.
 - Against : Not used by Sudarshan (although he does say he will support it "soon").

It seems this 