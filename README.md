WorkNote
========

Class that allows to drop comments and figures into a presentation while interactively working with python

Example
-------

```python
from worknotes import Worknote
wn = Worknote("./test", title='Test Worknotes', author='Author', date='\\today')
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
wn("Demonstrating value functionality", cat='slide')
wn(pi, desc = 'Value of pi')
wn(pi, precision = 5, desc = 'More precise value of pi')
wn('We can also automatically handle values smaller than the precision...\n')
wn(pi/1e8, desc = 'A really small value')
wn('... as well as units:\n')
wn(9.81, desc = 'Earth gravity acceleration', units = 'm/s^2', precision = 2)
wn('And we break automatically after a text line...\n')
wn('... if the text line ends in newline as above.')
wn.build_pdf()
wn.save()
```

Item categories
---------------
Item can be added via `wn(item, cat=category)`, where wn is a `Worknote` object, the item is the object to pass to the worknote and the category is a descriptive string. If no category is given, the Worknote tries to determine the category from implicit declarations of the item object. E.g. `wn("  * Listitem")` is equivalent to `wn('Listitem', cat='list')`.

The following categories are available:

  * 'slide' - A slide or section of the worknote, implicit via "Your Title \n---"
  * 'text' - A text string, no implicit declaration necessary
  * 'equation' - An equation, implicit via "$$ your equation $$"
  * 'list' - An item of a list, implicit via "  * Your item"
  * 'figure' - A figure, implicit via passing a matplotlib figure, or passing the filename of a figure with ending .pdf, .png, .jpg, .jpeg. 
      - Argument: size - Size in textwidth, default = 1
      - Argument: align - Alignment of figure, ('left', 'right', 'center', None), default = 'center'. If None is given as argument, no align environment ist specified and the figure will appear in line with other objects
      - Argument: gfxfmt - output format for matplotlib figures, default = 'pdf'
  * 'figurepage' - Same as 'figure', but forces figure on a new slide
  * 'table' - A table, implicit via passing a list or a numpy array. Table object need to be a 2D list or array. If the first line contains a string, Ite is assumed to be the table description.
  
If a numeric variable (type int, int64, float, float64) gets passed, the variable's value will be printed. There are 3 additional optional arguments available:

 * desc - A description of the variable. Gets printed in front of the value, followed by a colon.
 * units - The units of the variable. Gets printed behind the value.
 * precision - The precision of the floating point output (ignored for integer variables). If the value is too small to be represented in the chosen precision, the value is automatically printed in scientific notation.
 
  
Roadmap
-------

See the issues and milestones for features to be implemented.
