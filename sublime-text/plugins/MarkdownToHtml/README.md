# Markdown to HTML Plugin

## Usage

When saving a Markdown file, the text will be rendered in HTML using the github API: <https://developer.github.com/v3/markdown/>  
The rendered HTML will be saved in a file in the /tmp directory and the file will be opened in Chromium.  
When saving again the Markown file, it will be rendered and reloaded when the browser gets the focus (or when clicking in the browser page).
