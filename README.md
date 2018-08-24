# md2magic
**md2magic** is a wrapper for [markdown2](https://github.com/trentm/python-markdown2) that allows users to generate websites from markdown files.

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

### Resources
- [Markdown syntax guide](https://daringfireball.net/projects/markdown/syntax)
- [markdown2](https://github.com/trentm/python-markdown2)