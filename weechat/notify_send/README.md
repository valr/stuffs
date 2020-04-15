# Notify Send Plugin

## Installation

Copy the plugin in the autoload python directory of weechat:
~/.weechat/python/autoload

## Configuration

If required, adapt the options of the plugin e.g. using /fset.  
**Options**: plugins.var.python.notify_send.*

## Usage

With the default options, a notification will be sent using 'notify_send' in case of private message or highlight channel message.  

**Formats of the notification:**  

 * private message: buffer name / message
 * highlight channel message: prefix@buffer name / message
