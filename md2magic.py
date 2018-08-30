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
                if filename.endswith(".md") or filename.endswith(".html"):
                    print(" - " + filename + " [" + os.path.abspath(self.source + "/" + filename) + "]")
                    source_path = os.path.abspath(self.source + "/" + filename)
                    if filename.endswith(".md"):
                        output_path = (os.path.abspath(self.source + "/out/" + filename))[:-3] + ".html"
                        self.file_conversion("md", source_path, output_path)
                    elif filename.endswith(".html"):
                        output_path = (os.path.abspath(self.source + "/out/" + filename))[:-5] + ".html"
                        self.file_conversion("html", source_path, output_path)
                elif not filename.endswith(".pref"):
                    file_path = os.path.abspath(self.source + "/" + filename)
                    output_path = os.path.abspath(self.source + "/out/" + filename)
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        source_fp = open(file_path, "r")
                        output_fp = open(output_path, "w+")
                        output_fp.write(source_fp.read())
                        source_fp.close()
                        output_fp.close()
                        print("Copied " + filename)
            """
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
            """
        except FileNotFoundError:
            print("Can not access site directory at: " + self.source)

    def file_conversion(self, filetype, source_path, output_path):
        print("Source      --> " + source_path)
        print("Destination --> " + output_path)

        source_fp = open(source_path, "r")
        # Assemble HTML file
        if source_fp:
            if filetype == "md":
                # Read-in and convert content of markdown
                tmp_input = source_fp.read()
                tmp_output = self.markdowner.convert(tmp_input)
            elif filetype == "html":
                tmp_output = source_fp.read()
            source_fp.close()

            # Assemble HTML file
            self.assemble_file(tmp_output, source_path, output_path)
        
    def assemble_file(self, content, source_path, output_path):
        config_style = ""
        config_title = ""
        config_top = ""
        config_bottom = ""
        config_header = ""
        config_footer = ""
        components_dict = self.get_component_content()
        if len(components_dict['top']) > 0:
            config_header = components_dict['top']
        else:
            # Get stylesheet if available
            if self.config_options['style_src'] and (self.config_options['style_src'])[-4:] == ".css":
                config_style = "<link href='" + self.config_options['style_src'] + "' rel='stylesheet'>\n"
            # Get page title if available
            if self.config_options['title']:
                config_title = "<title>" + self.config_options['title'] + "</title>\n"
        if len(components_dict['bottom']) > 0:
            config_footer = components_dict['bottom']
        if len(components_dict['header']) > 0:
            config_header = components_dict['header']
        if len(components_dict['footer']) > 0:
            config_footer = components_dict['footer']

        # Assemble file
        if len(config_top) == 0:
            html_top = "<html>\n<head>\n" + config_style + config_title + "</head>\n<body>\n"
        else:
            html_top = config_top
        if len(config_bottom) == 0:
            html_bottom = "</body>\n</html>"
        else:
            html_bottom = config_bottom
        html_final =\
            html_top +\
            config_header +\
            content +\
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
        # Top
        config_top = ""
        if self.config_options['top_src'] and (self.config_options['top_src'])[-5:] == ".html":
            top_path = os.path.abspath(self.source + "/" + self.config_options['top_src'])
            try:
                # Get top from components dir, same dir context as config file
                top_fp = open(top_path, "r")
                content = top_fp.read()
                top_fp.close()
                if len(content) > 0:
                    config_top = content + "\n"
            except FileNotFoundError:
                print("Config error for top_src: " + self.config_options['top_src'] + " not found at: " + top_path)

        # Bottom
        config_bottom = ""
        if self.config_options['bottom_src'] and (self.config_options['bottom_src'])[-5:] == ".html":
            bottom_path = os.path.abspath(self.source + "/" + self.config_options['bottom_src'])
            try:
                # Get top from components dir, same dir context as config file
                bottom_tp = open(bottom_path, "r")
                content = bottom_tp.read()
                bottom_tp.close()
                if len(content) > 0:
                    config_bottom = "\n" + content
            except FileNotFoundError:
                print("Config error for bottom_src: " + self.config_options['bottom_src'] + " not found at: " + bottom_path)

        # Header
        config_header = ""
        if self.config_options['header_src']:
            header_path = os.path.abspath(self.source + "/" + self.config_options['header_src'])
            try:
                # Get header from components dir, same dir context as config file
                header_fp = open(header_path, "r")
                if (self.config_options['header_src'])[-3:] == ".md":
                    content = self.markdowner.convert(header_fp.read())
                elif (self.config_options['header_src'])[-5:] == ".html":
                    content = header_fp.read()
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
                footer_fp = open(footer_path, "r")
                if (self.config_options['footer_src'])[-3:] == ".md":
                    content = self.markdowner.convert(footer_fp.read())
                elif (self.config_options['footer_src'])[-5:] == ".html":
                    content = footer_fp.read()
                footer_fp.close()
                if len(content) > 0:
                    config_footer = "<footer>" + content + "</footer>\n"
            except FileNotFoundError:
                print("Config error for footer_src: " + self.config_options['footer_src'] + " not found at: " + footer_path)

        return {'top': config_top, 'bottom': config_bottom, 'header': config_header, 'footer': config_footer}


if __name__ == "__main__":
    md2magic = md2magic()
    if md2magic.valid_params:
        md2magic.find_files()
