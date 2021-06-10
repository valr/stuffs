import time

import weechat

options = {
    "notify_private_message": ("on", "send a notification on private message"),
    "notify_highlighted_message": (
        "on",
        "send a notification on highlighted channel message",
    ),
    "notification_urgency": ("normal", "urgency level of the notification"),
    "notification_timeout": ("5000", "timeout of the notification (in milliseconds)"),
    "notification_application_name": (
        "weechat",
        "application name of the notification icon",
    ),
    "notification_icon": ("weechat", "icon of the notification"),
}


def print_cb(start_time, _buffer, _time, tags, displayed, highlight, prefix, message):
    buffer_type = weechat.buffer_get_string(_buffer, "localvar_type")
    buffer_name = weechat.buffer_get_string(_buffer, "localvar_channel")

    if (
        weechat.config_get_plugin("notify_private_message") == "on"
        and buffer_type == "private"
        and int(_time) > int(start_time)
        and "self_msg" not in tags.split(",")
    ):
        notify_send(f"{buffer_name}:", message)
    elif (
        weechat.config_get_plugin("notify_highlighted_message") == "on"
        and buffer_type == "channel"
        and int(_time) > int(start_time)
        and int(highlight)
    ):
        notify_send(f"{prefix}@{buffer_name}:", message)

    return weechat.WEECHAT_RC_OK


def notify_send(origin, message):
    weechat.hook_process_hashtable(
        "notify-send",
        {
            "arg1": "-u",
            "arg2": weechat.config_get_plugin("notification_urgency"),
            "arg3": "-t",
            "arg4": weechat.config_get_plugin("notification_timeout"),
            "arg5": "-a",
            "arg6": weechat.config_get_plugin("notification_application_name"),
            "arg7": "-i",
            "arg8": weechat.config_get_plugin("notification_icon"),
            "arg9": origin,
            "arg10": message,
        },
        5000,
        "notify_send_cb",
        "",
    )

    return weechat.WEECHAT_RC_OK


def notify_send_cb(data, command, return_code, out, err):
    if return_code != 0:
        weechat.prnt(
            "", f"notify_send command: '{command}' has return code {return_code}"
        )

    if out != "":
        weechat.prnt("", f"notify_send output: {out}")

    if err != "":
        weechat.prnt("", f"notify_send error: {err}")

    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register(
        "notify_send",
        "valr",
        "0.4",
        "GPL3",
        "a highlight & private messages notification script",
        "",
        "",
    )

    for option, (value, description) in options.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, value)
            weechat.config_set_desc_plugin(option, description)

    weechat.hook_print("", "", "", 1, "print_cb", str(int(time.time())))
