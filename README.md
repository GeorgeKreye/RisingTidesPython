<h1>Rising Tides - Python</h1>
<b>Author(s):</b> George Kreye<br />
<b>Version</b>: 1.0.0 (September 2023 - made public June 2024)<br />
<b>Python version:</b> 3.10<br />
<b>Required packages (excluding dependencies):</b> dudraw 1.8.3, requests 2.31.0<br />
<b>License:</b> <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"> CC-BY-NC-SA 4.0</a>

<h2>About</h2>
Rising Tides is a modular assignment written in the Python language which out of the box teaches search algorithms, 
specifically breadth-first search, in the context of rising sea levels caused by climate change. The finished program
will allow a user to simulate flooding from an increase (or decrease) in sea level, allowing them to select an area to 
simulate flooding on as well as the increase in sea level in meters.

Rising Tides can also be modified to teach other concepts in programming, such as how to load data from files using
Python or how to display processed data using dudraw.

Students should see any TODO comment(s) within the files or the assignment writeup provided by their instructor (if applicable)
for their specific task(s).

<h3>Setting up</h3>
If you do not have Python 3.10, download it from <a href="https://www.python.org/downloads/">Python's official website</a>.
If Python 3.10 has reached end of support, please be aware of security risks from using an outdated version of Python;
in addition, if there is a different version of this assignment that uses a still-supported Python version, install that
Python version and use that version of this assignment instead.

All Python installs should have the pip package installer preinstalled. You can ensure that it is (or, if it is not,
install it) by following <a href="https://packaging.python.org/en/latest/tutorials/installing-packages/">these steps</a>.
If your Python install is managed by your operating system or another package manager, make sure you install pip locally.

Once you confirm both Python and pip are installed, run the following command in your OS's terminal:<br/>
<format>python -m pip install -r requirements.txt --force-reinstall</format><br />
This will ensure that all requirements (and their dependencies) are installed at the versions required by this assignment.

You will also need an IDE so you can modify the .py files used by the assignment. Using Python's inbuilt IDLE is not
recommended due to it not checking for syntax and other issues, as well as not promoting best practices when coding in
Python. Instead, a more feature-rich IDE, such as <a href="https://www.jetbrains.com/pycharm/">PyCharm</a> (the Community
version of which was used to construct this assignment), is recommended. This assignment will not need any features only
provided by a paid IDE.

<h3>Custom classes</h3>
Rising Tides uses two custom classes for data storage across its various modules: <b>Terrain</b> and <b>GridLocation</b>. 

Terrain is used to hold the data from a .terrain file after it has been loaded, and contains information such as the
terrain heightmap and any water sources that the flooding algorithm should start from.

GridLocation is used for storing coordinates with no information directly attached to them. Students should be encouraged to
use this class in their code to store any coordinates they might need later.

The assignment also contains a custom exception in <b>BadValueError</b>. In the default code it is used during the loading
of terrain to raise an error if a value read from a file is certain to cause an error down the line. If the assignment has
been altered to be rewriting the portion of code that handles the processing of file data, students should be encouraged
to use the exception class both to safeguard against bad .terrain files and to ensure they are reading .terrain files
correctly.

The display.py module has several classes specific to itself to encode display information:
<ul>
<li><b>Tile:</b> Used to represent a single unit of the display.</li>
<li><b>ThresholdGradient:</b> A sorted list of RGBPoint objects used to represent an elevation gradient's colors. It
also allows the quick retrieval of color values in the gradient using threshold values.</li>
<li><b>RGBPoint:</b> An object containing an RGB color value and a threshold value.</li>
</ul>

<h3>Creating your own .terrain files</h3>
Instructions on how to create additional .terrain files is provided in CreatingYourOwnTerrains.txt within the 'terrains'
folder.

<h3>Loading .terrain files from the Internet</h3>
If you are hosting a .terrain file from a remote location accessible via URL, you can create a local .terrain file with
the URL as its sole contents; provided the remote loading portions of terrain_loader.py are functional and the URL is not
broken, it should be able to download the remote file to cache.

<b><i>Never</i> host or download files from a location that you do not trust.</b>

<h2>For educators</h2>
This assignment makes heavy use of functions as to allow for easy modification. This is so that the assignment can be
adapted for a variety of concepts - file I/O, graphical display, etc.

As such, a complete version of RisingTides.py (RisingTidesComplete.py) is provided. If you are using this assignment
for its original purpose of showing breadth-first (or depth-first, though that works less realistically for this
assignment) search in action, <b>remove RisingTidesComplete.py before distribution to students</b>. Otherwise, see
"modifying this assignment" below.

Creating an assignment writeup is highly recommended. Keith Schwarz's writeup for the original Java version of this
assignment, which can be used as a baseline, is located
<a href="http://nifty.stanford.edu/2023/schwarz-rising-tides/doc/Rising%20Tides.pdf">here</a>.

<h3>Modifying this assignment</h3>
If you wish to modify this assignment to cover a concept other than a search algorithm, the first step is to remove the
original RisingTides.py and replace it by renaming RisingTidesComplete.py. This will have the effect of having 
breadth-first search already built into the assignment as given to students.

Following that step, you will want to locate the file and/or function(s) that are applicable to what you want to teach.
A list of examples is provided below:
<ul>
<li><b>Reading data from a file input: </b>terrain_loader.py</li>
<ul>
<li><b>Processing file data:</b> load_terrain and process_terrain_file</li>
<li><b>Reading a file from the web: </b>load_web_terrain</li>
</ul>
<li><b>Visual display: </b>display.py</li>
<li><b>User interaction:</b> main.py and user_input.py</li>
</ul>

Upon determining which functions associated with the concept(s) you wish to use this assignment to teach, remove content
from functions as you see fit. You may also remove functions entirely if they are intermediate steps in a function being
cleared for students to rewrite. Any functions you are having students rewrite should have a TODO comment within them so
that students can easily locate what they are writing as well as tell them what their objective is. Multiple TODO
comments can be used if you wish to give additional guidance.

If you are having students rewrite load_terrain and are not teaching them to read a file from the web (as in they are not
also rewriting load_web_terrain) <b>do not remove the check for remote sources</b>. This will interfere with remote
files being loaded properly.

Modifications you distribute beyond assignment to students should have an addition to the changelog with your initials
preceding the version numbering. Attribution should also be altered accordingly, and documentation altered as needed.

<h3>Limitations</h3>
Unlike the original Java version of this assignment, this version cannot change what terrain data it is using 
mid-execution due to the limitations of DUDraw. It also does not support directly inputting a water level like that
version does. This may change in the future if the infrastructure needed to support such features is added to DUDraw.

<h2>Changelog</h2>
This short changelog will only cover more recent updates. For a full changelog, see changelog.txt.
<ul>
<li><b>1.0.0</b> - Initial release</li>
</ul>

<h2>Attribution</h2>
This assignment is based on a Java/C++ assignment by Keith Schwarz of Stanford University
(<a href="http://nifty.stanford.edu/2023/schwarz-rising-tides/">link</a>).
The original .terrain files (BayArea, CraterLake, Guam, GulfOfGuinea, Iceland, MarsCraters, MarsOlympusMons, Miami,
MiamiHuge, NewYorkCity, NewYorkCityHuge, PearlRiverDelta, Pohnpei, RioDeJaneiro, Seattle, SeattleHuge, SouthBayArea,
SouthBayAreaHuge, SouthWestNorway, TelkaAMaui, and VelingraSenegal) are also from this source; see ATTRIBUTION.txt in 
the terrains folder for their original attribution.

This Python version was written by George Kreye under direction of Professor Faan Tone Liu of the University of Denver.

Modifications of this assignment may be shared under the terms of the Creative Commons license linked above. Commercial
use of <i>any</i> portion of this assignment, including substantial use of source code, is prohibited.

Attribution for the original code should be similar to the following:<br />
"Based on code by George Kreye of the University of Denver; assignment concept originally by Keith Schawrz of Stanford University. See ATTRIBUTION.txt in 'terrains' folder for .terrain file attribution."

Attribution for any additional .terrain files you are distributing with the assignment should have proper attribution
added to ATTRIBUTIONS.TXT. This includes the creator's name, the source of the data used to create the .terrain file
(following the data source's own attribution standards, if any), and a link to said data.
