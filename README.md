# OANDA-Bluefever
Following fantastic Youtube videos to build Algorithmic Trading application (eventually)...

Latest progress: https://www.youtube.com/watch?v=wMnS0QvGaUw&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=46
inside_bar_timings.ipynb

# Back Story

Blue Fever have delivered fantastic training via Youtube, referenced above.  This is NOT a criticism of them:
Online training risks following parrot fashion without fully understanding what you are doing.  When everything works perfectly, this is not a problem.  When things go slightly wrong - which can be as simple as your own typos - you have to go backwards.  I have just hit one of these moments.  I think the underlying problem is:  a timedate stamp is required, but I seem to be trying to get this from an aggregated file.  I also have a detail file, so some re-engineering required...  In the end (i.e. current time of writing), this was effectively a typo by me.  I referenced an aggregated file (ma_results) rather than the detail file (all trades).  Easy mistake, very difficult to trace back.  I hope I've made some significant improvements with doc-strings, and general documentation.  Live and learn.

# Basic Flow

1. Recap1.py:  Creates all of the currency/period files in format Base_Quote_granularity e.g. GBP_JPY_H1.
2. MA_sim.py:  Write analysis data forward to: ma_test_results.csv and 'all trades.csv'