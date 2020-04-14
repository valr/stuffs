import weechat as weechat

options = {
    "notify_private_message": ("on", "send a notification on private message"),
    "notify_highlighted_message": ("on", "send a notification on highlighted channel message"),
    "notification_urgency": ("normal", "urgency level of the notification"),
    "notification_timeout": ("10000", "timeout of the notification (in milliseconds)"),
    "notification_application_name": ("weechat", "application name of the notification icon"),
    "notification_icon":  ("weechat", "icon of the notification")
}


def handle_msg(data, buf, date, tags, displayed, highlight, prefix, message):
    private = weechat.config_get_plugin("notify_private_message")
    highlighted = weechat.config_get_plugin("notify_highlighted_message")

    buffer_type = weechat.buffer_get_string(buf, "localvar_type")
    buffer_name = weechat.buffer_get_string(buf, "short_name")

    if private == "on" and buffer_type == "private":
        notify_send(buffer_name, message)
    elif highlighted == "on" and buffer_type == "channel" and int(highlight):
        notify_send("{}@{}:".format(prefix, buffer_name), message)

    return weechat.WEECHAT_RC_OK


def notify_send(origin, message):
    urgency = weechat.config_get_plugin("notification_urgency")
    timeout = weechat.config_get_plugin("notification_timeout")
    application = weechat.config_get_plugin("notification_application_name")
    icon = weechat.config_get_plugin("notification_icon")

    weechat.hook_process_hashtable("notify-send",
                                   {"arg1": "-u", "arg2": urgency,
                                    "arg3": "-t", "arg4": timeout,
                                    "arg5": "-a", "arg6": application,
                                    "arg7": "-i", "arg8": icon,
                                    "arg9": origin, "arg10": message},
                                   20000, "notify_send_cb", "")

    return weechat.WEECHAT_RC_OK


def notify_send_cb(data, command, return_code, out, err):
    if return_code == weechat.WEECHAT_HOOK_PROCESS_ERROR:
        weechat.prnt("", "error with command: '%s'" % command)
    elif return_code > 0:
        weechat.prnt("", "notify-send return_code: %d" % return_code)

    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register("notify_send", "valr", "0.2", "GPL3",
                     "notify_send - a highlight & private notification script",
                     "", "")

    for option, (value, description) in options.items():
        # weechat.config_unset_plugin(option)
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, value)
            weechat.config_set_desc_plugin(option, description)

    weechat.hook_print("", "", "", 1, "handle_msg", "")


"""
check plugins documentation of weechat

https://weechat.org/files/doc/stable/weechat_scripting.en.html
https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_config_set_desc_plugin

def hook_config_cb(data, option, value):
    print("data: " + data + " option: " + option + " value: " + value)
    return weechat.WEECHAT_RC_OK

weechat.hook_config("plugins.var.python.notify_send.*", "hook_config_cb", "")
"""
