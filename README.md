## Leiper: A Homebrew Text Adventure Game

To whom it may concern:

I've always loved **retro** games. One of my favorites is [*Zork, the Underground Empire*](https://textadventures.co.uk/games/view/5zyoqrsugeopel3ffhz_vq/zork).
As a neat way to learn some of the basics of Object Oriented Python programming as well as some web-development, I decided
to make my own shameless rip-off of Zork. 

At the moment, I've only implemented the "scaffolding" of the game (the parser, each class, etc)
so there isn't much to "play". But all that is to come.

#### A brief history (skip, if the details bore you)
My initial plan was to utilize the Natural Language Toolkit (`nltk`) to write some badass parsing 
scripts which could handle a variety of complex sentences with ease. But I found the vanilla
`pos_tag` to be quite inaccurate (i.e., it always though 'blue' was a noun no matter how it was used)
and using ML to accomplish the problem felt like overkill. So I decided to write my own using the `re`
library and some shameless lists. It's not as fancy as something you could do with `nltk`, but it gets the 
job done well enough and provides output that is considerably more helpful than "INVALID COMMAND" etc. when it
doesn't understand a sentence. Maybe one day I will bust out the machine learning to make something
more elegant, but for now this will suffice.

This program uses the following non-standard libraries: 

```buildoutcfg
re
nltk
flask
```

To run the program, just enter `python launch.py <mode>` where mode is either:
* "local", if you would like to run the program in a terminal window or
* "server", if you would like to run the flask application associated with the program and
play the game in a browser (http://localhost:5000).

Enjoy!