import argparse
import sys


class HelpOnErrorArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


parent_parser = HelpOnErrorArgumentParser(add_help=False)
parent_parser.add_argument("-p", "--profiles", action='append', default=["default"], help="profile to run")
parent_parser.add_argument("-c", "--conffile", type=str, default=None,
                           help="Config for Philip, by default locates at ~/.config/philip/config.json")

default_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8"
}
