# Open URL Panel Plugin

## Usage

When pressing the defined keybinding (default: f1), a panel will be displayed with the list of URLs defined in the settings. The selected URL will be opened in the web browser.

## Settings

The list of URLs can be defined globally in Package Settings ➔ OpenUrlPanel ➔ Settings.  
Additional URLs can be defined per project in the .sublime-project file, like this:

```json
{
    "settings": {
        "open_url_panel": {
            "url_list": [
                [
                    "My Plugins",
                    "https://github.com/valr/stuffs/tree/main/sublime-text/plugins/"
                ],
                [
                    "My Syntax Files",
                    "https://github.com/valr/stuffs/tree/main/sublime-text/syntax/"
                ]
            ]
        }
    }
}
```
