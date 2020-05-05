class ColorScheme:
    def __init__(self):
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk, Gdk
        self.css = b'#base {background: none; background-color:white; }#accent {background: none;background-color:white; }#background  {background: none; background-color:white; }'
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(self.css)
        self.context = Gtk.StyleContext()
        self.screen = Gdk.Screen.get_default()
        self.context.add_provider_for_screen(self.screen, self.css_provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.notifier = None
        self.main_window = Gtk.Window(title="Color Scheme")
        self.main_window.set_resizable(False)
        self.grid = Gtk.Grid()
        self.grid.set_hexpand(True)
        self.grid.set_vexpand(True)
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_border_width(5)
        self.main_window.add(self.grid)

        self.generate_button = Gtk.Button(label="New color scheme")
        self.generate_button.set_hexpand(True)
        self.generate_button.connect("clicked", self.generate_color_scheme)
        self.grid.attach(self.generate_button, 0, 0, 3, 1)

        self.base_color_button = Gtk.Button(label="  \n\n")
        self.base_color_button.set_name("base")
        self.base_color_button.connect("clicked", self.copy_color_to_clipboard)
        self.base_color_button.set_vexpand(True)
        self.grid.attach(self.base_color_button, 0, 2, 1, 3)

        self.accent_color_button = Gtk.Button(label="  \n\n")
        self.accent_color_button.set_name("accent")
        self.accent_color_button.connect(
            "clicked", self.copy_color_to_clipboard)
        self.accent_color_button.set_vexpand(True)
        self.grid.attach(self.accent_color_button, 1, 2, 1, 3)

        self.background_color_button = Gtk.Button(label="  \n\n")
        self.background_color_button.set_name("background")
        self.background_color_button.connect(
            "clicked", self.copy_color_to_clipboard)
        self.background_color_button.set_vexpand(True)
        self.grid.attach(self.background_color_button, 2, 2, 1, 3)

        self.generate_template_button = Gtk.Button(
            label="Generate website template")
        self.generate_template_button.set_hexpand(True)
        self.generate_template_button.connect(
            "clicked", self.generate_website_template)
        self.grid.attach(self.generate_template_button, 0, 1, 3, 1)

        self.exit_button = Gtk.Button(label="Exit")
        self.exit_button.set_hexpand(True)
        self.exit_button.connect("clicked", self.exit_app, Gtk)
        self.grid.attach(self.exit_button, 0, 5, 3, 1)

        self.main_window.connect("destroy", self.exit_app, Gtk)
        self.main_window.resize_children()
        self.main_window.show_all()
        self.generate_color_scheme(None)
        Gtk.main()

    def generate_color(self):
        import random
        return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    def color_to_css_hex(self, color):
        hex_color = "#"
        hex_color += str(hex(color[0]))[2:] if len(str(hex(color[0]))
                                                   [2:]) > 1 else "0" + str(hex(color[0]))[2:]
        hex_color += str(hex(color[1]))[2:] if len(str(hex(color[1]))
                                                   [2:]) > 1 else "0" + str(hex(color[1]))[2:]
        hex_color += str(hex(color[2]))[2:] if len(str(hex(color[2]))
                                                   [2:]) > 1 else "0" + str(hex(color[2]))[2:]
        return hex_color

    def exit_app(self, caller, gtk):
        print("Exit")
        gtk.main_quit()

    def show_notification(self, title, content):
        if self.notifier == None:
            import gi
            gi.require_version('Notify', '0.7')
            from gi.repository import Notify
            Notify.init("Color Scheme")
            self.notifier = Notify
        self.notifier.Notification.new(
            title, content, "dialog-information").show()

    def copy_color_to_clipboard(self, caller):
        name = caller.get_name()
        color = ""
        if name:
            if name == "base":
                color = self.color_to_css_hex(self.colors[0])
            elif name == "accent":
                color = self.color_to_css_hex(self.colors[1])
            elif name == "background":
                color = self.color_to_css_hex(self.colors[2])

            self.clipboard.set_text(color, -1)
            print(color + " has been copied to the clipboard")
            self.show_notification(
                "Copied to clipboard!", color + " has been copied to the clipboard")

    def generate_color_scheme(self, caller):
        self.colors = [self.generate_color(), self.generate_color(),
                       self.generate_color()]
        self.css = "#base  {background: none;background-color:" + \
            self.color_to_css_hex(self.colors[0]) + "; }"
        self.css += "#accent  {background: none;background-color:" + \
            self.color_to_css_hex(self.colors[1]) + "; }"
        self.css += "#background  {background: none;background-color:" + \
            self.color_to_css_hex(self.colors[2]) + "; }"
        self.css_provider.load_from_data(bytes(self.css, "ASCII"))

    def generate_website_template(self, caller):
        print("Generating website template...")
        from pathlib import Path
        import os
        home_dir = str(Path.home())
        print("User directory:", home_dir)
        output_dir = Path(home_dir + "/ColorScheme")
        print("Output directory:", output_dir)

        if not Path.is_dir(output_dir):
            os.mkdir(output_dir)
            print("Created", str(output_dir))
        else:
            if Path(str(output_dir) + "/index.html").is_file():
                os.remove(str(output_dir)+"/index.html")
                print("Removed", str(output_dir)+"/index.html")
            if Path(str(output_dir) + "/style.css").is_file():
                os.remove(str(output_dir)+"/style.css")
                print("Removed", str(output_dir)+"/style.css")

        index_file = open(str(output_dir)+"/index.html", "w")

        index_file_content = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Website template</title>
</head>

<body>
    <div id="header">
        <div class="container">
            <h1>Website template</h1>
        </div>
    </div>
    <div class="container">
        <div id="nav">
            <a href="#">LINK</a>
            <a href="#">LINK</a>
            <a href="#">LINK</a>
            <a href="#">LINK</a>
            <a href="#">LINK</a>
        </div>
        <div id="posts">
            <div class="post">
                <div class="post-title">
                    <h2>Post title</h2>
                </div>
                <div class="post-wrap">
                    <p> Lorem ipsum dolor sit amet</p>
                    <div class="read-more-button">More...</div>
                </div>
            </div>
            <div class="post">
                <div class="post-title">
                    <h2>Post title</h2>
                </div>
                <div class="post-wrap">
                    <p> Lorem ipsum dolor sit amet</p>
                    <div class="read-more-button">More...</div>
                </div>
            </div>
            <div class="post">
                <div class="post-title">
                    <h2>Post title</h2>
                </div>
                <div class="post-wrap">
                    <p> Lorem ipsum dolor sit amet</p>
                    <div class="read-more-button">More...</div>
                </div>
            </div>
            <div class="post">
                <div class="post-title">
                    <h2>Post title</h2>
                </div>
                <div class="post-wrap">
                    <p> Lorem ipsum dolor sit amet</p>
                    <div class="read-more-button">More...</div>
                </div>
            </div>
            <div class="post">
                <div class="post-title">
                    <h2>Post title</h2>
                </div>
                <div class="post-wrap">
                    <p> Lorem ipsum dolor sit amet</p>
                    <div class="read-more-button">More...</div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>'''

        index_file.write(index_file_content)

        css_file = open(str(output_dir)+"/style.css", "w")

        css_file_content = ''':root {
    --base-color: [base-color];
    --accent-color: [accent-color];
    --background-color: [background-color];
}

html,
body {
    margin: 0;
    padding: 0;
    font-family: sans-serif;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    margin: 0;
}

.container {
    max-width: 1000px;
    margin: auto;
}

#header {
    width: 100%;
    background-color: var(--base-color);
    color: white;
    padding: 20px 0px;
}

#nav {
    width: 195px;
    float: left;
    padding: 20px 0px 20px 5px;
    background-color: var(--background-color);
    margin-top: 40px;
}

#nav a {
    display: inline-block;
    width: 100%;
    text-decoration: none;
    color: var(--accent-color);
}

#nav a:hover {
    filter: brightness(1.2);
}

#posts {
    width: 760px;
    float: left;
    padding: 40px 20px;
}

.post {
    background-color: var(--background-color);
    margin-bottom: 20px;
}

.post-title {
    background-color: var(--base-color);
    color: white;
    padding: 20px;
}

.post-wrap {
    padding: 20px;
}

.post-wrap p {
    margin-bottom: 40px;
}

.read-more-button {
    padding: 10px;
    color: var(--accent-color);
    padding: 10px;
    clear: both;
    display: inline;
    cursor: pointer;
    user-select: none;
}

.read-more-button:hover {
    filter: brightness(1.2);
}

@media screen and (max-width: 1000px) {

    #nav {
        width: calc(100% - 40px);
        margin-left: 20px;
    }

    #posts {
        width: calc(100% - 35px);
    }

    #header {
        text-align: center;
    }

}'''
        css_file.write(css_file_content.replace("[base-color]", self.color_to_css_hex(self.colors[0])).replace(
            "[accent-color]", self.color_to_css_hex(self.colors[1])).replace("[background-color]", self.color_to_css_hex(self.colors[2])))
        self.show_notification("Website template generated",
                               "Website template generated in " + str(output_dir))
