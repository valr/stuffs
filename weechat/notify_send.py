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
    buffer_type = weechat.buffer_get_string(buf, "localvar_type")
    buffer_name = weechat.buffer_get_string(buf, "short_name")

    if buffer_type == "private":
        if weechat.config_get_plugin("notify_private_message") == "on":
            notify_send(buffer_name, message)
    elif buffer_type == "channel" and int(highlight):
        if weechat.config_get_plugin("notify_highlighted_message") == "on":
            notify_send("{}@{}:".format(prefix, buffer_name), message)

    return weechat.WEECHAT_RC_OK


def notify_send(origin, message):
    weechat.hook_process_hashtable(
        "notify-send",
        {"arg1": "-u", "arg2": weechat.config_get_plugin("notification_urgency"),
         "arg3": "-t", "arg4": weechat.config_get_plugin("notification_timeout"),
         "arg5": "-a", "arg6": weechat.config_get_plugin("notification_application_name"),
         "arg7": "-i", "arg8": weechat.config_get_plugin("notification_icon"),
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
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, value)
            weechat.config_set_desc_plugin(option, description)

    weechat.hook_print("", "", "", 1, "handle_msg", "")
