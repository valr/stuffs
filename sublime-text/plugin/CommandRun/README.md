# Command Run Plugin

## Installation

Copy the plugin directory in the Sublime Text package directory:
~/.config/sublime-text-3/Packages/CommandRun

## Usage

Install an executable command (binary or script) named 'the_project_name'.sublime-command in the sublime project directory.  
The command will be run on the predefined event types.

List of predefined event types:
- on_post_save

List of parameters passed to the command (with examples):
1. the event type: 'on_post_save'  
2. the syntax: 'Python'
3. the filename: '/home/charlie/coucou.py'
