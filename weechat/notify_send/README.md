# Notify Send Script

## Installation

Copy the script in the autoload Python directory of WeeChat:
~/.weechat/python/autoload

## Configuration

If required, adapt the script options e.g. using /fset.  
**Options**: plugins.var.python.notify_send.*

## Usage

With the default options, a notification will be sent using 'notify-send' in case of private message or highlight channel message.  

**Formats of the notification:**  

 * private message: buffer name / message
 * highlight channel message: prefix@buffer name / message
