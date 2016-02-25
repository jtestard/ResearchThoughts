Hi Yannis,

I am tackling a problem, which I can state as follows:

*Consider the Denormalized Set-At-A-Time (DSAAT) formulation of the paper (shown in section 4.3 of the new draft and 4.8 of the rejected paper). Is this formulation:*

 1. *A completely novel contribution*
 2. *A formulation which was already completely specified by prior work.*
 3. *A formulation which was mostly built upon prior work, but to which we added some small novelty. It is straightforward to see how our novelty is derived from the prior work.*

I made my own investigation and this is what I found:

 - None of the prior work cited in the rejected SIGMOD paper shows evidence of either 2 or 3.
 - AsterixDB's current distribution (based on my experimentation) includes some form of rewriting which resembles DSAAT, but no details are available in any of the AsterixDB papers.

My opinion is that either :

 - The AsterixDB team found the rewriting themselves but did not publish specific semantics (I even found a bug in their distribution regarding this rewriting, they make unchecked assumptions).
 - There is some other paper X out there which is not on our list of contributions and does specify either 2 or 3.

If you have any opinion about what the next step should be, please let me know.

Best,

@Vicky: feel free to pitch in if you remember something.

~Jules