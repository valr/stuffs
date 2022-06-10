import re

import weechat

options = {
    "buffer_list": (
        "",
        "comma separated list of buffers where substitution will be done",
    ),
    "nick_list": (
        "",
        "comma separated list of nicks for which substitution will be done",
    ),
    "pattern": (".", "regex pattern matching the line message"),
    "replacement": (".", "string replacing the matching occurences"),
}


def substitute(data, line):
    buffer_list = weechat.config_get_plugin("buffer_list")
    nick_list = weechat.config_get_plugin("nick_list")
    pattern = weechat.config_get_plugin("pattern")
    replacement = weechat.config_get_plugin("replacement")

    if line["buffer_name"] in buffer_list.split(","):
        nick = [
            tag[len("nick_") :]
            for tag in line["tags"].split(",")
            if tag.startswith("nick_")
        ]
        if nick and nick[0] in nick_list.split(","):
            return {"message": re.sub(pattern, replacement, line["message"])}

    return {}


if __name__ == "__main__":
    weechat.register(
        "substitute",
        "valr",
        "0.1",
        "GPL3",
        "a script using regex to substitute text in message (per channel & nick)",
        "",
        "",
    )

    for option, (value, description) in options.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, value)
            weechat.config_set_desc_plugin(option, description)

    weechat.hook_line("", "", "", "substitute", "")
