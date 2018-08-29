# md2magic
**md2magic** is a wrapper for [markdown2](https://github.com/trentm/python-markdown2) that allows users to generate websites from markdown files. It also supports generic HTML files for headers, footers, and content rather than markdown files. The distinction in their file types are automatically detected.

### Usage
Instructions to create a basic website:
1. Create a directory to store the *md2magic.py* script and your site directories. Put *md2magic.py* in there.
2. Create a directory for a site (its name should not have spaces). Create a *config.pref* file (see sample site). You may define the (immediate) path of the CSS file and header/footer markdown files here too.
3. Place your markdown files within the directory.
4. Run md2magic like so:


    python3 md2magic.py [site directory name]

### Directory structure
Specific files are necessary to use md2magic effectively. Firstly, each site would have its own directory. Secondly, each site directory would have a file called 'config.pref' and a 'components' directory.

##### Before output
    [md2magic]
       |--- md2magic.py
       |--- [sample_site]
               |--- config.pref
               |--- main.css
               |--- index.md
               |--- about.md
               |--- [components]
                       |--- header.md
                       |--- footer.md
                       
##### After output
    [md2magic]
       |--- md2magic.py
       |--- [sample_site]
               |--- config.pref
               |--- main.css
               |--- index.md
               |--- about.md
               |--- [components]
                       |--- header.md
                       |--- footer.md
               |--- [out]
                       |--- main.css
                       |--- index.html
                       |--- about.html

### TODO
- Add recursive directory iteration (e.g. not just files in directory 'blog', but 'blog/posts' too).
- Generation of headers and footers from a config constructor file (just state metadata and headers + footers generated automatically on build).
- 'build' and 'diff-build' commands to differentiate doing a full site build vs only building new files/entries.
- 'init' command to generate project/site directory with config file.

### Resources
- [Markdown syntax guide](https://daringfireball.net/projects/markdown/syntax)
- [markdown2](https://github.com/trentm/python-markdown2)