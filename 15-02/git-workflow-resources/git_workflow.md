## Git Workflow

### Prerequisites

Before we start the talk, I will assume that you have some knowledge of the following concepts, whether in the context of Git or not:

 - branching/merging
 - repositories
 - commits
 
This talk is based on a set of slides written by a Sony software engineer, [Lemi Orhan Ergin](https://speakerdeck.com/lemiorhan). The slides are available online [here](https://speakerdeck.com/lemiorhan/git-branching-model-for-efficient-development).

### The objectives of the talk

There are two things I wish you will take away from this talk :

 1. Why Git is a good version control system for you as a researcher
 - Give you an example of a "good" development workflow for your programming projects and even latex paper descriptions.

### Slide 2 Why Git is Good?
 
Git has attracted a tremendous amount of attention in the software industry in the past 5-6 years, and in this slides are some of the reasons why.

##### 1. Cheap local branching, everything is local

Git is decentralized, hence the local repository is not necessarily a copy of the remote. In fact, there might be multiple remotes, but we won't go there for this talk.

As such, a branch can exist locally but not in the remote repository, which makes it very cheap and desirable to create local branches. As we will see later on, this will allow a much cleaner commit history, which is important if you want to know how differently some paritcular feature was implemented two years ago, or how retrieve some latex file containing some information that was irrelevant earlier but relevant now.

##### 2. Git is fast, git is small

Always a good feature to have.

##### 3. The staging area

Before being committed, changes in Git have to be added to the staging area, a concept absent from other version control systems such as Subversion. While this adds a little complexity (the need to add each file you want to commit to the staging area), it allows you to partition logically different changes into multiple commits, further improving opportunities to keep the commit history clean.

##### 4. Distributed, any workflow

Decentralization means many different workflows are possible, although we will concentrate on one workflow in this talk.

##### 5. GitHub : Git is the new standard with a huge community

Git is extremely popular, very well documented and open source, and if you don't know yet how to use it, you just need to look for a online tutorial and it won't be long before you do.

### Slide 3 Some concepts

##### 1. Branch

One of the prerequisites for this talk. A seperate line of work.

##### 2. Public Branch

A public branch is one that more than one person pulls from (i.e. multiple committers).

##### 3. Feature Branch

A private branch that you alone are using, and will not be exposed in the public repository.

##### 4. Tracking Branch

When a public branch is pulled (downloaded) from the remote repository into the local, a newly created branch is created with the contents of the public branch. This branch is set to track its remote counterpart, allowing to push (upload) local changes onto the public branch or pull contents from other committers.

### Slide 4 Merging and Branching in Git

In SVN, branches are (somewhat) costly. In Git they are dirt cheap, and should be used as much as possible (in particular locally).

### Slides 5-6 Workflow

This talk's workflow targets the software industry, but this isn't too far from a workflow that is relevant to us researchers.

### Slide 7 Repository Management in Git

The team setup you have in your research lab will probably look something like what is shown in the picture. All four committers make changes to the same remote, but have very different looking repositories.

### Slides 8-9 Main Branches

In this examples, this author suggests three main branches. But probably as a researcher it is unlikely you will need more than `origin/master`.

### Slide 10 Release

In the project I have been working on (AsterixDB in collaboration with UCI), releases were managed seperately by compiling the master branch at regular intervals when enough new features were added to deserve a new release. The release workflow suggested here is another possibility.

### Slide 11 Supporting Branches

Also called feature branches. In our workflow, the supporting branches should always be local.

### Slides 12-15 Feature development and release mananement

Go over slides 12 and 13 somewhat carefully. Take the example on slide 15 but write it on the board with the origin and local annotations :

 - `origin/master`
 - `local/master`
 - `local/f1`
 - `local/f2`

### Slide 17-19 Merging vs Rebasing

Follow the slides.

### Slide 20

You can see how the Git and Merge approaches results in different commit history trees.

### Slide 21-22

Follow the slides.

### Slide 23

![Golden rule of rebasing example](git-workflow-resources/golden-rule.png)

### Slide 24 Merge or Rebase

##### Fast-Forward Merge

When you try to merge one commit with a commit that can be reached by following the first commit’s history, Git simplifies things by moving the pointer forward and **does not create a new commit**, because there is no divergent work to merge together – this is called a “fast-forward.”

### Slide 25-34

Follow the slides.

#### A few links

 - [Using GitHub as an academic (testimony)](http://www.hybridpedagogy.com/journal/push-pull-fork-github-for-academics/)
 - [GitLab](https://about.gitlab.com/)
