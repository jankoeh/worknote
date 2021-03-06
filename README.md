WorkNote
========

Class that allows to drop comments and figures into a presentation while interactively working with python

Example
-------

```python
from worknote import Worknote
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
wn.build()
wn.save()
```

### Editing existing slides
Existing items can be removed via `Worknote.remove(index)`, where `index` is a tuple describing the item position. An overview over item positions can be obtained via `print wn`.
The position of two items can be switched via `Worknote.move(source, destination)` where `source` and `destination` are the item indexes.
An item can be inserted at a specific position by passing the index to the worknote call.
Indices can be written either as a tuple, e.g. ```[0,0]``` is the first element on the first slide, or as a colon-separated text string, e.g. ```'0:0'```. You can use any of the two possible notations for any index that you pass, e.g. ```wn.move([0,0], '1:0')``` is perfectly valid.

#### Example
```python
print wn
0 Slide: First slide title with unicode
  0 Text: The Proble...
  1 Equation
1 Slide: Slide implicite generation
  0 Figure: fig1.pdf
wn.move([0, 0], [1, 0])
print wn
0 Slide: First slide title with unicode
  0 Figure: fig1.pdf
  1 Equation
1 Slide: Slide implicite generation
  0 Text: The Proble...
```

Output formats
--------------
`wn.build()` Creates by default a LaTeX Beamer pdf. The following styles are available and can be passed as argument:

  * **'Beamer'** - Build Beamer.tex  and generate Beamer.pdf (default)
  * **'Beamer.tex'** - Builds Beamer.tex
  * **'Report'** - Builds Report.pdf
  * **'Report.tex'** - Builds Report.tex
  * **'Markdown'** - Builds Report.md

Item categories
---------------
Item can be added via `wn(item, cat=category)`, where wn is a `Worknote` object, the item is the object to pass to the worknote and the category is a descriptive string. If no category is given, the Worknote tries to determine the category from implicit declarations of the item object. E.g. `wn("  * Listitem")` is equivalent to `wn('Listitem', cat='list')`.

The following categories are available:

  * **slide** - A slide or section of the worknote, implicit via "Your Title \n---"
  * **text** - A text string, no implicit declaration necessary
  * **equation** - An equation, implicit via "$$ your equation $$"
  * **list** - An item of a list, implicit via "  * Your item"
  * **enumerate** - An item of an enumerated list, implicit declaration via "  #  Your item"
  * **figure** - A figure, implicit via passing a matplotlib figure, or passing the filename of a figure with ending .pdf, .png, .jpg, .jpeg. 
      - Argument: size - Size in textwidth, default = 1
      - Argument: align - Alignment of figure, ('left', 'right', 'center', None), default = 'center'. If None is given as argument, no align environment ist specified and the figure will appear in line with other objects
      - Argument: gfxfmt - output format for matplotlib figures, default = 'pdf'
  * **figurepage** - Same as 'figure', but forces figure on a new slide
  * **table** - A table, implicit via passing a list or a numpy array. Table object need to be a 2D list or array. If the first line contains a string, Ite is assumed to be the table description.
      - size - Can be an arbirary LaTeX fontsize (only relevant for LaTeX right now).
        default='normalsize'. If set to 'auto', size is determined by table length. This assumes an empty slide ...
  * **value** - A numeric value. Must be an instance of either ```int```, ```numpy.int64```, ```float``` or ```numpy.float64```. Additional options are:
     - desc - A description of the variable. Gets printed in front of the value, followed by a colon.
     - units - The units of the variable. Gets printed behind the value.
     - precision - The precision of the floating point output (ignored for integer variables). If the value is too small to be represented in the chosen precision, the value is automatically printed in scientific notation.
     - error - An error for the value. Gets printed using the same precision and formatting as the value itself. 
 
  
Roadmap
-------

See the issues and milestones for features to be implemented.
