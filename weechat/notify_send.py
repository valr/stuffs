import weechat as weechat


def handle_msg(data, buffer, date, tags, displayed, highlight, prefix, message):
    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")
    buffer_name = weechat.buffer_get_string(buffer, "short_name")

    if buffer_type == "private":
        notify_user(buffer_name, message)
    elif buffer_type == "channel" and int(highlight):
        notify_user("{}@{}:".format(prefix, buffer_name), message)

    return weechat.WEECHAT_RC_OK


def notify_user(origin, message):
    weechat.hook_process_hashtable("notify-send",
                                   {"arg1": "-u", "arg2": "normal",
                                    "arg3": "-t", "arg4": "10000",
                                    "arg5": "-a", "arg6": "weechat",
                                    "arg7": origin, "arg8": message},
                                   20000, "process_cb", "")

    return weechat.WEECHAT_RC_OK


def process_cb(data, command, return_code, out, err):
    if return_code == weechat.WEECHAT_HOOK_PROCESS_ERROR:
        weechat.prnt("", "error with command: '%s'" % command)
    elif return_code > 0:
        weechat.prnt("", "notify-send return_code: %d" % return_code)

    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register("notify_send", "valr", "0.1", "GPL3",
                     "notify_send - a highlight & private notification script",
                     "", "")
    weechat.hook_print("", "", "", 1, "handle_msg", "")
