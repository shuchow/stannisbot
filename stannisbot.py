import logging
import re
import textblob

try:
    import weechat as w
except:
   print("STANNISBOT must be run under weechat. http://www.weechat.org")
   import_ok = False

abstract_nouns = []
concrete_nouns = []
abstract_nouns_file = "/absolute/path/to/stannisbot/abstract_nouns.txt"
concrete_nouns_file = "/absolute/path/to/stannisbot/concrete_nouns.txt"

STANNISBOT_NAME    = "stannisbot"
STANNISBOT_AUTHOR  = "Shu-Wai Chow <schow@alumni.rutgers.edu>"
STANNISBOT_VERSION = "0.1.1"
STANNISBOT_LICENSE = "GPL3"
STANNISBOT_CLOSE   = "close_log"
STANNISBOT_DESC    = "A Stannis Baratheon Bot."


def close_log():
    logging.debug("Closing....")
    return w.WEECHAT_RC_OK


def catch_message(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    """
    server_name = (w.buffer_get_string(bufferp, "name").split("."))[0]
    own_name =  w.info_get("irc_nick", server_name)
    message_from = w.buffer_get_string(bufferp, "localvar_nick")

    logging.debug("Message caught!")
    logging.debug("From:" + message_from)
    logging.debug("Own Name:" + own_name)
    logging.debug("Server Name:" + server_name)
    logging.debug(w.buffer_get_string(bufferp, "localvar_type"))
    logging.debug(msg)
    """

    # Stop if message is from yourself.
    #    if len(msg) == 0 or own_name == message_from:
    if len(msg) == 0:
        return w.WEECHAT_RC_OK

    caught = has_less(msg)

    if caught is True:
        if textblob_analysis(msg) is True:
            #write fewer
            w.command(bufferp, "Stannisbot: fewer")

    return w.WEECHAT_RC_OK


def has_less(message):
    if re.search(r"\bless\b", message, flags=re.I):
        #"Less" in the message.
        return True
    else:
        return False


def textblob_analysis(message):
    logging.debug(abstract_nouns)
    evaluate_after_less = False

    try:
        blobbed = textblob.TextBlob(message.decode('utf-8'))
    except:
        logging.debug("Can't get textblob from the message!" + message)

    for word, tag in blobbed.tags:
        """
        #Case1: Not fewer : shouldn't write.
        #Case2: Less, Abstract Noun: Souldn't write.
        #Case3: Less, less: Continue to next word
        #Case4: Less, not abstract: Fewer!
        #Case5: Less at end: shouldn't write.
        """
        if word.upper() == "LESS":
            # If word found is "less" flag it and move on to the next word.
            evaluate_after_less = True
            continue

        # Flag is now set.  Check if the following word is a noun/abstract noun.
        # Check whitelist first.
        if (evaluate_after_less is True) and (is_concrete_noun(word) is True):
                return True

        if (evaluate_after_less is True) and (tag == 'NN' or tag == 'NNS'):
            if is_abstract_noun(word) is False:
                return True

        evaluate_after_less = False

    return False


def is_abstract_noun(word):
    return True if word in abstract_nouns else False


def is_concrete_noun(word):
    return True if word in concrete_nouns else False

if __name__ == "__main__":
    logging.basicConfig(filename='/tmp/stannisbotout.log', level=logging.DEBUG)

    w.register(STANNISBOT_NAME, STANNISBOT_AUTHOR, STANNISBOT_VERSION, STANNISBOT_LICENSE, STANNISBOT_DESC, STANNISBOT_CLOSE, "")

    logging.debug('STARTING UP STANNISBOT!! YEAH!!!  BEND THE KNEE!!')
    w.hook_print("", "", "", 1, "catch_message", "")

    #Hrmmm.... Weechat's not letting this import.
    with open(abstract_nouns_file) as f:
        abstract_nouns = [x.strip('\n') for x in f.readlines()]

    with open(concrete_nouns_file) as f:
        concrete_nouns = [x.strip('\n') for x in f.readlines()]
