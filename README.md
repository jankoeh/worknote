WorkNote
========

Class that allows to drop comments in figures into a presentation while interactively working with python

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

  * Build pdf functionality
  * Support multiple formats, such as LaTex reports, Markdown, HTML
  * Figure item to handle naming
  * Save Worknote as pickle?