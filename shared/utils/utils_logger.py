# ********************************
# IMPORTS python
# ********************************
import pprint

# change this to false to stop the print in where ever it is being used
ALLOW_PRINT_DEBUG = True


def log_print(param_title, param_message, param_oneline=False):
    """
    print debug statements no need to start finding all your debug prints
    to comment them out when you are done
    just disable it here

    Args:
        :param param_title: the print title
        :param param_message: the print message
        :param param_oneline: if True will print just a single-line without header
    Returns:
        :rtype void:
    """
    if ALLOW_PRINT_DEBUG:
        if param_oneline:
            print("|")
            print("PRINT_DEBUG")
            print("|")
            pprint.pprint(param_message)
            print("|")
        else:
            print("|")
            print("|")
            print("======================================================================")
            print("PRINT_DEBUG")
            print("|")
            print("TITLE : " + param_title)
            print("|")
            print("---------------------------------------------------------------------")
            print("|")
            pprint.pprint(param_message)
            print("|")
            print("======================================================================")
    else:
        pass


def print_prety(param_title, param_message, param_oneline=False):
    """
    print wrapper

    Args:
        :param param_title: the print title
        :param param_message: the print message
        :param param_oneline: if True will print just a single-line without header
    Returns:
        :rtype void:
    """
    if param_oneline:
        print("|")
        pprint.pprint(param_message)
        print("|")
    else:
        print("|")
        print("|")
        print("======================================================================")
        print("|")
        print("TITLE : " + param_title)
        print("|")
        print("---------------------------------------------------------------------")
        print("|")
        pprint.pprint(param_message)
        print("|")
        print("======================================================================")
