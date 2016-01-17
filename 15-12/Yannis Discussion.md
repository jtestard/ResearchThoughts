### Yannis Discussion

#### November 23rd

 - Ok. I am prepping for the research exam (happens on December 4th), and will be pretty busy with this until then.
 - A little more context : the iCenter actually gave me wrong information in October, they came back to me last week and told me that actually if I wanted to, I could graduate and get the proper work permissions (albeit late) by graduating this quarter. 
 - My reason to stay is very goal-driven : I want to stay and submit a paper with some chances of getting published. My understanding from our Thursday conversation is that the chances of submitting a paper on query decorrelation are high (70%-80%) if this is my focus for the next 4 months. Please confirm this point as soon as possible, as it doesn’t make sense for me to stay is the chances are very low.

OK. Now we're talking.

As I said, I think the chances for SIGMOD/VLDB are low due to the incremental nature. Though I won't mind to try our luck and first submit to VLDB.
However, if we try our luck 2-3 times at ICDE, EDBT, CIKM and we do the work I envision, I feel we have a 80% chance.
 
 - I would also like to have your perspective on whether my strategy is a good one if my goal is to return to research within 1-2 years.


Does not change things dramatically but it is surely positive.
Personally, I will be very satisfied to see you delivering a concrete goal.

#### Widom Principles: November 7th

paper authors,

here is the ultimate guide to writing a paper, by Jennifer Widom 
 
http://cs.stanford.edu/people/widom/paper-writing.html

Two additional comments by me:
* Fully believe Jennifer's points on the importance of introduction. Her 5 steps on writing an introduction are the thing to do in 90% of the cases. If you believe that your paper is in the 10% exception, think again whether it really is. It usually isn't.

* Writing a paper does not really require talent. It only requires relentless attention to the points of this guide. It also requires reading your drafts and asking yourself a lot of times: "what is the purpose served by this paragraph?" 

#### November 7th : remarks

Jules,
your plan is sensible. Two points to note:

(I said this yesterday also) If the PL guys feel that they can identify SQL++, then there are many opportunities, beyond the decorrelation problem. Just from the top of my head:
* Web browser code (Javascript) that performs automatic incremental page maintenance. That's what Costas works on now but with FORWARD. Imagine doing it directly in Javascript. The problem setting is virtually identical to what you have done with decorelation. You simply change "decorelation" to "IVM"

Second Point: The data access paper is poorly written, poorly positioned and lacks important content for a repositioning. It has got two rejections, where we totally confused the reviewers and they rightfully rejected us. I believe the reviews are checked in and you can read them. If not, let me know and I will check them in.

As Ihad told you, I believe it has to be cast as a decorelation paper, with application to both middleware and genuine NoSQL databases, where we can use Asterix.

Indeed, Vicky had argued for this approach but I was against executing it because our decorelation material was too little. Later I found out it also needs fixing.

#### Avlin Cheung

as far as the comparison with Alvin's work is concerned, what you have to exhibit is the benefits of SQL++ queries Vs equivalent combinations of SQL queries.
Therefore, you need examples where multiple individual SQL queries are inferior to a single SQL++ that does the same job.
In your shoes, I wouldn't stray too much into the PL side of Alvin Cheung's work, ie., how are SQL or SQL++ queries detected.


#### Tangents

I can surely become more managerial on dictating what you do.

But work on it yourself also. You exhibit a problem of going into tangents too easily. It happens on a macro scale (what I mentioned on the previous email) and a micro scale. Eg, your weekly research presentations tend to go into too many slides, with too many half-thought-out tangents and too few definitive points on the few points that truly matter. You don't have to bring 30 densely packed slides to meetings. You need a few well thought out ones.

That's a key reason why i suggested ASTERIX SQL++ (very clear goal) and an industry "break". Industry is easy to know what is the goal and to focus on the goal since it is clear what is the goal at any time.
Theory courses also help because math problems have single, clear goals.

In academia focus is a bit of a fine art. I cannot kill creativity with decrees "stop thinking outside the box, never go into tangents" and I cannot stop you from accomplishing alternate requirements (research exam). That's where you need to be alert to find a fine balance between exploring tangents and accomplishing goals.

### Fall Distraction

Yes, I like this plan.

Note that continuous shifts from targets are generally counterproductive distractions and they are 99.9% destructive when the goal is short term results. 
In the Spring you gave up the ASTERIX SQL++, dived deep into polystores, and lost a quite good SQL++ publicity opportunity along the way. Can be recovered but some temporal loss at least has happened. (BTW, it is likely not coincidental that Couchbase has not called back, given its close connection with Mike.)
Now, in the Fall, you took the small PL section of the research exam and put a serious effort in making it a real research target, without knowing yet if the complete firepower to go after such target is here. The downside is that the very tangible plan on the decorellation seems abandoned.

Radical goals are all nice and good but only if full firepower to go after them is assembled. The BigDAWG, headed by MIT, essentially goes after polystores and its agenda is essentially what you'd like to propose. But it is 7 faculty members behind this agenda and it will be an uncountable number of students on the execution.

So, clear the PL situation very quickly because otherwise it will become the Fall 2015 distraction. 


#### Research Exam

Hello Yannis,

Thank you for all this information. I was wondering the following:

1) Did you have time to get in touch with Amazon DynamoDB/ CouchDB yet?

I met the CouchDB guys at VLDB and they apologized for being too busy to not reply to my previous email. One my next one, I will introduce you directly to Gerald.
The DynamoDB email is a bit longer and has not been written yet. There is an outstanding SQL++ endeavor with them and I need to update them on many things, along with your case.
In the meantime, I found one more connection that sounds very interesting for middleware: Composite/Cisco. Let's connect on a Skype when you have time and I'll tell you more. 
 
2) Indeed, I agree that the research exam should be conservative, because I absolutely need to validate it this quarter. I am also interested in going beyond, but I wouldn't do so until after the "conservative" research exam is completed or near to completion. I will let you know when I have a good enough draft for us to discuss on it. The topic, as of now, is the Alvin Cheung work on the intersection between Compilers and Databases.

I concur. The most important point of the exam is ... to pass it. 
The reason I was mentioning tying the exam with a paper is that a paper provides the narrow focus that can compensate for the expansiveness that relatively "centrifugal" thinkers tend to fall for. ( Indeed, obtaining experience in executing under a relatively narrow focus is a key point for which I believe industrial experience can help you.)
 
3) I am meeting with Julie on the 21st and we'll go into the details of how to get the proper work permissions. Notice that while I should get a M.Sc. degree at the end of Fall (as long as I validate the research exam), it is not clear yet whether I will be able to go work right away or have to stay an extra quarter (due to visa and work authorization delays and restricitions). This is what I will be discussing with her. If I were to stay an extra quarter, it could make it easier to do what you are suggesting in your third point.