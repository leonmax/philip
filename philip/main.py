__author__ = 'leonmax'

import update

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", type=str, default="stage", help="profile to run")
    parser.add_argument("-c", "--conffile", type=str, default=None,
                        help="config file of the deployment script, by default locates at ~/.config/philip/config.json")

    subparsers = parser.add_subparsers(help='sub-command help')
    update.register_parser(subparsers)
    args = parser.parse_args()

    # noinspection PyBroadException
    try:
        args.func(args)
        return 0
    except:
        return 1
