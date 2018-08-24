import sys, re
from markdown2 import MarkdownWithExtras


class md2magic:
    valid_params = True

    # File paths
    source = ""
    destination = ""
    config = ""

    # Options
    config_options = {}

    # Markdown service
    markdowner = MarkdownWithExtras(extras=["tables", "wiki-tables"])

    def __init__(self):
        if len(sys.argv) == 3:
            if (sys.argv[1])[-3:] == ".md":         # Source file is a must!
                self.source = sys.argv[1]
            if (sys.argv[2])[-5:] == ".html":       # Direct, simple translation to HTML
                self.destination = sys.argv[2]
            elif (sys.argv[2])[-6:] == "config":    # Translation with styling
                self.config = sys.argv[2]
                self.destination = (sys.argv[1])[:-3] + ".html"
        else:
            print("md2magic needs 2 parameters:\n\n\tmd2magic [source].md [path/]config\n")
            self.valid_params = False

    def main(self):
        print("Source      --> " + self.source)
        print("Destination --> " + self.destination)

        self.get_config()

        source_fp = open(self.source, "r")
        # Assemble HTML file
        if source_fp:
            # Read-in and convert content of markdown
            tmp_input = source_fp.read()
            tmp_output = self.markdowner.convert(tmp_input)
            source_fp.close()

            # Assemble HTML file

            # Get stylesheet if available
            config_style = ""
            if self.config_options['style_src'] and (self.config_options['style_src'])[-4:] == ".css":
                config_style = "<link href='" + self.config_options['style_src'] + "' rel='stylesheet'>\n"

            # Get page title if available
            config_title = ""
            if self.config_options['title']:
                config_title = "<title>" + self.config_options['title'] + "</title>\n"

            config_header = ""
            config_footer = ""
            components_dict = self.get_component_content()
            if len(components_dict['header']) > 0:
                config_header = components_dict['header']
            if len(components_dict['footer']) > 0:
                config_footer = components_dict['footer']

            # Assemble file
            html_top = "<html>\n<head>\n" + config_style + config_title + "</head>\n<body>\n"
            html_bottom = "</body>\n</html>"
            html_final =\
                html_top +\
                config_header +\
                tmp_output +\
                config_footer +\
                html_bottom

            # Write to output file
            destination_fp = open(self.destination, "w")
            destination_fp.write(html_final)
            destination_fp.close()

    def get_config(self):
        config_fp = open(self.config, "r")
        for option in config_fp.readlines():
            option_param = option.split(': ')
            if len(option_param) == 2:
                parsed_value = re.search('"(.*)"\n', option_param[1])
                self.config_options[option_param[0]] = parsed_value.group(1)
            else:
                print("Invalid config option: " + str(option_param))
        print("Config read complete:")
        print(self.config_options)

    def get_component_content(self):
        # Header
        config_header = ""
        if self.config_options['header_src'] and (self.config_options['header_src'])[-3:] == ".md":
            try:
                # Get header from components dir, same dir context as config file
                header_fp = open(str((sys.argv[2])[:-6] + self.config_options['header_src']), "r")
                content = self.markdowner.convert(header_fp.read())
                header_fp.close()
                if len(content) > 0:
                    config_header = "<header>" + content + "</header>\n"
            except FileNotFoundError:
                print("Config error for header_src:\n\t" + self.config_options['header_src'] + " not found!")

        # Footer
        config_footer = ""
        if self.config_options['footer_src'] and (self.config_options['footer_src'])[-3:] == ".md":
            try:
                # Get footer from components dir, same dir context as config file
                header_fp = open(str((sys.argv[2])[:-6] + self.config_options['footer_src']), "r")
                content = self.markdowner.convert(header_fp.read())
                header_fp.close()
                if len(content) > 0:
                    config_footer = "<footer>" + content + "</footer>\n"
            except FileNotFoundError:
                print("Config error for footer_src:\n\t" + self.config_options['footer_src'] + " not found!")

        return {'header': config_header, 'footer': config_footer}


if __name__ == "__main__":
    md2magic = md2magic()
    if md2magic.valid_params:
        md2magic.main()
