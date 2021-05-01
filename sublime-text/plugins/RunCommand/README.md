# Run Command Plugin

## Usage

The Text Command 'run_command' allows executing any command via the command palette.  
The format to define in the .sublime-commands file is described below.

## Format

Examples:

```json
[
  {
    "caption": "Minimal Example",
    "command": "run_command"
  },
  {
    "caption": "Git Status",
    "command": "run_command",
    "args": {
      "command": "git status -sb",
      "cwd": "$project_path",
      "timeout": 5,
      "source": "none",
      "target": "window"
    }
  },
  {
    "caption": "Prettier",
    "command": "run_command",
    "args": {
      "command": "prettier --parser ${arg_parser} --tab-width ${arg_tab_width|4}"
    }
  }
]
```

The first sublime-command is the smallest possible definition.  
It will be displayed in the command palette as an entry with 'Minimal Example' name.  
When the entry is selected, the command palette will ask the command to execute as it isn't provided in the arguments.

The second sublime-command is a complete definition.  
It will be displayed in the command palette as an entry with 'Git Status' name.

The third sublime-command contains an example of command having arguments that will be asked via the command palette before execution.

The possible arguments in 'args' are:

- **command** contains the command to execute.  
  It can contain arguments in the format _${arg_xxx}_ or _${arg_xxx|yyy}_ where _xxx_ is the name of the argument and _yyy_ is a default value for that argument.

- **cwd** contains the working directory where the command will be executed.  
  It can be a path like _'/home/foo/bar'_ or a variable like _'$project_path'_.  
  The variable is one of those accepted by the extract_variables function as defined in the [Sublime Text API](https://www.sublimetext.com/docs/3/api_reference.html).  
  If not provided, the default working directory is the one where Sublime Text was started.

- **timeout** contains the number of seconds allowed for the command execution.  
  When the timeout is reached the process running the command will be killed and the remaining part of the 'run_command' Text Command will be skipped.  
  If not provided, the default timeout is set to 30 seconds.

- **source** defines the source for the input text provided to the command.  
  The possible values are:

  | Source    | Description                                      |
  | --------- | ------------------------------------------------ |
  | selection | the selected text from the current window (view) |
  | window    | the entire text from the current window (view)   |
  | none      | no input text will be provided to the command    |

  If not provided, the default source is 'selection'.

- **target** defines the target for the output text provided by the command.  
  The possible values are:

  | Target    | Description                                                                                       |
  | --------- | ------------------------------------------------------------------------------------------------- |
  | selection | the selected text in the current window (view) will be replaced by the output text of the command |
  | window    | a new window will be created to receive the output text of the command                            |
  | none      | the output text of the command won't be used                                                      |

  If not provided, the default target is 'selection'.
