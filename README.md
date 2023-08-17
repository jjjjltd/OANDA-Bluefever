# OANDA-Bluefever
Following fantastic Youtube videos to build Algorithmic Trading application (eventually)...

Latest progress: https://www.youtube.com/watch?v=6XFz2inPnhQ&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=61
WebDash directory

# Back Story

Blue Fever have delivered fantastic training via Youtube, referenced above.  This is NOT a criticism of them:
Online training risks following parrot fashion without fully understanding what you are doing.  When everything works perfectly, this is not a problem.  When things go slightly wrong - which can be as simple as your own typos - you have to go backwards.  I have just hit one of these moments.  I think the underlying problem is:  a timedate stamp is required, but I seem to be trying to get this from an aggregated file.  I also have a detail file, so some re-engineering required...  In the end (i.e. current time of writing), this was effectively a typo by me.  I referenced an aggregated file (ma_results) rather than the detail file (all trades).  Easy mistake, very difficult to trace back.  I hope I've made some significant improvements with doc-strings, and general documentation.  Live and learn.

# Basic Flow

At this point, we're - kind of - consolidating.  
1.  ma_sim.py:  A simplified moving averages analysis.
2.  inside_bar_sim.py:  A more sophisticated analysis of inside bar strategy.  Includes more abstraction e.g. an OandaAPI class with various attributes, functions and class methods (functions)
3.  Currently working on candle_patterns.ipynb.  This is a third 'fresh start' but we've got a lot of well estasblished ground at this point.

