# Substitute Script

## Installation

Copy the script in the autoload Python directory of WeeChat:
~/.weechat/python/autoload

## Configuration

Adapt the script options using /fset  

**Options**: plugins.var.python.substitute.\*  

**Example**:  
```
plugins.var.python.substitute.buffer_list = "irc.libera.#python,irc.libera.#python-fr"  
plugins.var.python.substitute.nicklist = "valr"  
plugins.var.python.substitute.pattern = "."  
plugins.var.python.substitute.replacement = "*"  
```  

The buffer_list option contains a comma separated list of buffer masks as defined in the hook_line API documentation (argument buffer_name): https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_hook_line  

The nicklist option contains a comma separated list of nicks.

## Usage

Messages sent by the nicks in the nicklist will be substituted using the regex pattern and replacement string defined in the options.
The substitution is only done in the given list of buffers for the given list of nicks.
