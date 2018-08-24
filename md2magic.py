import os, sys
from markdown2 import MarkdownWithExtras


class md2magic:
    valid_params = True

    source = ""
    destination = ""
    config = ""

    source_fp = 0
    destination_fp = 0

    markdowner = MarkdownWithExtras(extras=["tables", "wiki-tables"])

    def __init__(self):
        if len(sys.argv) == 3:
            if (sys.argv[1])[-3:] == ".md":         # Source file is a must!
                self.source = sys.argv[1]
            if (sys.argv[2])[-5:] == ".html":       # Direct, simple translation to HTML
                self.destination = sys.argv[2]
            elif (sys.argv[2])[-6:] == "config":    # Translation with styling
                self.config = sys.argv[2]
        # elif len(sys.argv) == 2:
        #     if (sys.argv[1])[-3:] == ".md":
        #         self.source = sys.argv[1]
        #         self.destination = (sys.argv[1])[:-3] + ".html"
        else:
            print("md2magic needs 2 parameters:\n\n\tmd2magic [source].md [path/]config\n")
            self.valid_params = False

    def main(self):
        print("Source      --> " + self.source)
        print("Destination --> " + self.destination)

        self.source_fp = open(self.source, "r")
        # Assemble HTML file
        if self.source_fp:
            # Read-in and convert content of markdown
            tmp_input = self.source_fp.read()
            tmp_output = self.markdowner.convert(tmp_input)
            self.source_fp.close()

            # Assemble HTML file
            html_top = "<html>\n<head>\n<title>Hello World</title>\n</head>\n<body>\n"
            html_bottom = "</body>\n</html>"
            html_final = html_top + tmp_output + html_bottom

            # Write to output file
            self.destination_fp = open(self.destination, "w")
            self.destination_fp.write(html_final)
            self.destination_fp.close()


if __name__ == "__main__":
    md2magic = md2magic()
    if md2magic.valid_params:
        md2magic.main()
