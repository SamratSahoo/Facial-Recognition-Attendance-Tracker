Docs
===============
The Docs folder has oen sole purpose: to house the documentation of this project. The HTML files that make up the documentation
can be found in the Docs folder. Within the Docs folder there are 2 subdirectories along with 2 batch files.

Build Subdirectory
------------------
The build subdirectory houses all of the automatically generated HTML files for this project. This subdirectory is automatically
updated when the ``make html`` command is run.

Source Subdirectory
-------------------
The source subdirectory houses all of the RST files for this project. The RST files are very similar to markdown because they allow
for an ease of creating web-based documentation through the ReadTheDocs system without long hours of web development.

Batch Files
------------
The batch files serve as the method to convert the RST files to HTML files. When the ``make html`` command is run, these batch files
scan the RST files and make the respective HTML files based on RST files.