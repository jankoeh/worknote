WorkNote
========

Class that allows to drop comments and figures into a presentation while interactively working with python

Example
-------

```python
from worknotes import Worknote
wn = Worknote("./test")
wn("First slide title", cat='slide')
wn("The Problem we want to slove:", cat='text')
wn("f=\sqrt{x}", cat='equation')
# do some python work ...
from pylab import *
plot(sqrt(arange(10)))
wn("Slide with figure on it", cat='slide')
wn(gcf(), cat='figure')
wn("Slide with a list on it", cat='slide')
wn('some list item', cat='list')
wn('  * implicit list declarationvia "* "')
wn("implicit declaration of text")
wn.build_pdf()   #build function to be implemented , see ./test/beamer.tex
```

Roadmap
-------

  * ~~bUild pdf functionality~~  Can be used with pdflatex
  * Support multiple formats, such as LaTex reports, Markdown, HTML
  * ~~Figure item to handle naming~~ Done
  * ~~Save Worknote as pickle?~~ Done
  * Make helper function for getting a pretty value printout for variables
  * Handle metadata and, if metadata present, add title page (So far, can only be set via ```Worknote.__init__()``` and is ignored apart from saving and loading)
