WorkNote
========

Class that allows to drop comments and figures into a presentation while interactively working with python

Example
-------

```python
from worknotes import Worknote
wn = Worknote("./test")
wn = Worknote("./test")
wn.set_metdata(title = 'Test Worknotes', author = 'John Doe mit ö', date = '\\today')
wn("First slide title", cat='slide')
wn("The Problem we want to solve:", cat='text')
wn("f=\sqrt{x}", cat='equation')
# do some python work ...
from pylab import *
plot(sqrt(arange(10)))
xlabel("fluor/MeV")
ylabel("Intensity g s/Liter")
wn("Slide implicite generation\n------------------")
wn(gcf(), cat='figure', size=.9)
wn("Slide with a list on it", cat='slide')
wn('some ist item', cat='list')
wn('  * implicit list declaration via "* "')
wn("implicit declaration of text")
#implicit declaration of a table
wn([['First column','Second Column', 'Third Column'],[1.,2.,3.],[4,5,6]])
wn.build_pdf()
wn.save()
```

Roadmap
-------

  * ~~bUild pdf functionality~~  Can be used with pdflatex
  * Support multiple formats, such as LaTex reports, Markdown, HTML
  * ~~Figure item to handle naming~~ Done
  * ~~Save Worknote as pickle?~~ Done
  * ~~Make helper function for getting a pretty value printout for variables~~ Not doing that anymore, we are implementing it differently
  * ~~Handle metadata and, if metadata present, add title page (So far, can only be set via ```Worknote.__init__()``` and is ignored apart from saving and loading)~~ Done
