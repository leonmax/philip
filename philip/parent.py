import argparse

__author__ = 'leonmax'

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument("-p", "--profiles", action='append', default=["stage"], help="profile to run")
parent_parser.add_argument("-c", "--conffile", type=str, default=None,
                           help="Config for Philip, by default locates at ~/.config/philip/config.json")
parent_parser.add_argument("-m", "--message", nargs='?', default="Philipfile",
                           help="the message file Philip delivery to marathon")