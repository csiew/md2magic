# md2magic
**md2magic** is a wrapper for [markdown2](https://github.com/trentm/python-markdown2) that allows users to generate websites from markdown files.

### Directory structure
Specific files are necessary to use md2magic effectively. Firstly, each site would have its own directory. Secondly, each site directory would have a file called 'config.pref' and a 'components' directory.

#####Before output
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
                       
#####After output
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