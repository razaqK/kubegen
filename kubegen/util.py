import six
import yaml
from pyfiglet import figlet_format

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(string, color, font='slant', figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def validate_yaml(config):
    try:
        yaml.safe_load(config)
        return True, config
    except:
        return False, 'Failed to validate k8s policy file.'
