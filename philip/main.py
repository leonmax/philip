from philip import diff

__author__ = 'leonmax'

import update

def main():
    import argparse

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--dry-run", action='store_true', help="dry run this deploy without really execute")
    parent_parser.add_argument("-p", "--profiles", action='append', default=["stage"], help="profile to run")
    parent_parser.add_argument(
        "-c", "--conffile", type=str, default=None,
        help="config file of the deployment script, by default locates at ~/.config/philip/config.json")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    update.register_parser(subparsers.add_parser('update', parents=[parent_parser], help='update an app'))

    args = parser.parse_args()
    args.func(args)
