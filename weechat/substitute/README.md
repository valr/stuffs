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
plugins.var.python.substitute.nick_list = "valr"  
plugins.var.python.substitute.pattern = "."  
plugins.var.python.substitute.replacement = "*"  
```

## Usage

Messages sent by the nicks in the nick_list will be substituted using the regex pattern and replacement string defined in the options.
The substitution is only done in the given list of (comma separated) channels for the given list of (comma separated) nicks.
