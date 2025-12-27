# Open URL Panel Plugin

## Usage

When pressing the defined keybinding (default: F1), a panel will be displayed with the list of URLs defined in the settings.
The list is sorted by default. The URL selected in the panel will be opened in the web browser.

## Settings

The settings can be defined globally in the menu: Preferences ➔ Package Settings ➔ OpenUrlPanel ➔ Settings.  
They can be overriden per project in the .sublime-project file, like this:

```json
{
    "settings": {
        "open_url_panel": {
            "sort": true,
            "url_list": [
                [
                    "My Plugins",
                    "https://github.com/valr/stuffs/tree/main/sublime-text/plugins/"
                ],
                [
                    "My Syntax Files",
                    "https://github.com/valr/stuffs/tree/main/sublime-text/syntax/"
                ]
            ],
            "extend_url_list": [
                [
                    "Example website",
                    "https://example.com/"
                ]
            ]
        }
    }
}
```

Available settings:
- **sort** : Sort the list of URLs by their ids  
- **url_list** : The list of URLs to display in the panel  
- **extend_url_list** : Additional URLs to display in the panel
