import ConfigParser
import os
import logging

logging.getLogger("config_agent").setLevel(logging.DEBUG)

__all__ = [
    "default_file_path",
    "load_config",
]


PWD = os.path.dirname(os.path.realpath(__file__))
default_file_path = os.path.join(PWD, "default.cfg")


def load_config(paths = None):
    if paths:
        paths.insert(0, default_file_path)
    else:
        paths = [default_file_path]

    config = ConfigParser.SafeConfigParser()
    try:
        config.read(paths)
    except ConfigParser.Error:
        msg = "parsing configuration file %s failed. " \
            "upgrade your instance:" + "\n\n" +\
            "    zwdadmin.py upgrade <full path to instance>" + "\n\n" +\
            "if it still doesn't works, try re-install ZboxWiki" % default_file_path
        logging.exception(msg)

    maintainer_email = config.get("main", "maintainer_email")
    if maintainer_email:
        splits = maintainer_email.split("@")
        config.set("main", "maintainer_email_prefix", splits[0])
        config.set("main", "maintainer_email_suffix", splits[1])

    return config


config = load_config()


def get_full_path(section, name):
    global config

    rel_path = config.get(section, name)
    instance_full_path = config.get("paths", "instance_full_path") or PWD
    rel2full_path = os.path.join(instance_full_path, rel_path)

    if os.path.exists(rel_path):
        path_fixed = os.path.realpath(rel_path)
    elif os.path.exists(rel2full_path):
        path_fixed = rel2full_path
    else:
        raise IOError("composing full path of '%s' failed" % rel_path)

    return path_fixed


if __name__ == "__main__":
    paths = ["/Users/lee/lees_wiki/default.cfg"]
    my_config = load_config(paths)
    t =  my_config.getint("main", "version")
    print type(t), repr(t)

    t =  my_config.get("frontend", "home_link_name")
    print t