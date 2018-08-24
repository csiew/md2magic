import sys
import os
import re
import errno
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
        if len(sys.argv) == 2:
            if os.path.exists(os.path.abspath(self.source)):
                self.source = sys.argv[1]
            else:
                print("Can not find site directory!")
                self.valid_params = False
        else:
            print("md2magic usage:\n\n\tmd2magic [project directory name]\n")
            self.valid_params = False

        if not self.get_config():
            self.valid_params = False

    def find_files(self):
        # Iterate through directory
        directory = os.fsencode(self.source)
        print("Directory: " + self.source)
        if not os.path.exists(os.path.dirname(str(self.source + "/out/"))):
            try:
                os.makedirs(os.path.dirname(str(self.source + "/out/")))
                print("Creating output directory")
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        try:
            # Convert individual files
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".md"):
                    print(" - " + filename + " [" + os.path.abspath(self.source + "/" + filename) + "]")
                    source_path = os.path.abspath(self.source + "/" + filename)
                    output_path = (os.path.abspath(self.source + "/out/" + filename))[:-3] + ".html"
                    self.file_conversion(source_path, output_path)
            # Make copy of CSS
            style_path = os.path.abspath(self.source + "/" + self.config_options['style_src'])
            style_out_path = os.path.abspath(self.source + "/out/" + self.config_options['style_src'])
            if os.path.exists(style_path):
                style_fp = open(style_path, "r")
                style_out_fp = open(style_out_path, "w+")
                style_out_fp.write(style_fp.read())
                style_out_fp.close()
                style_fp.close()
                print("Copied CSS: " + self.config_options['style_src'])
        except FileNotFoundError:
            print("Can not access site directory at: " + self.source)

    def file_conversion(self, source_path, output_path):
        print("Source      --> " + source_path)
        print("Destination --> " + output_path)

        source_fp = open(source_path, "r")
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
            destination_fp = open(output_path, "w+")
            destination_fp.write(html_final)
            destination_fp.close()

    def get_config(self):
        self.config = os.path.abspath(self.source + "/config.pref")
        if os.path.exists(os.path.abspath(self.config)):
            try:
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
                return True
            except FileNotFoundError:
                print("Can not access config at: " + self.config)
                return False
        else:
            print("Can not find config at: " + self.config)
            return False

    def get_component_content(self):
        # Header
        config_header = ""
        if self.config_options['header_src'] and (self.config_options['header_src'])[-3:] == ".md":
            header_path = os.path.abspath(self.source + "/" + self.config_options['header_src'])
            try:
                # Get header from components dir, same dir context as config file
                header_fp = open(header_path, "r")
                content = self.markdowner.convert(header_fp.read())
                header_fp.close()
                if len(content) > 0:
                    config_header = "<header>" + content + "</header>\n"
            except FileNotFoundError:
                print("Config error for header_src: " + self.config_options['header_src'] + " not found at: " + header_path)

        # Footer
        config_footer = ""
        if self.config_options['footer_src'] and (self.config_options['footer_src'])[-3:] == ".md":
            footer_path = os.path.abspath(self.source + "/" + self.config_options['header_src'])
            try:
                # Get footer from components dir, same dir context as config file
                header_fp = open(footer_path, "r")
                content = self.markdowner.convert(header_fp.read())
                header_fp.close()
                if len(content) > 0:
                    config_footer = "<footer>" + content + "</footer>\n"
            except FileNotFoundError:
                print("Config error for footer_src: " + self.config_options['footer_src'] + " not found at: " + footer_path)

        return {'header': config_header, 'footer': config_footer}


if __name__ == "__main__":
    md2magic = md2magic()
    if md2magic.valid_params:
        md2magic.find_files()
