from app import bus_viewer, main_app
import sys
import argparse


class App:
    def __init__(self, args):
        parser = argparse.ArgumentParser(
            description="A simple text editor",
            usage="""ded <command> [<args>]

Available commands:
   debugger   Shows all messages sent on the PIDComm bus
   editor     Opens the text editor (starting a new PIDComm bus if needed)
""",
        )
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args(args[1:2])

        if not hasattr(self, args.command):
            print(f"Command {args.command} not found")
            parser.print_help()
            exit(1)

        getattr(self, args.command)(args)

    def debugger(self, args):
        bus_viewer()

    def editor(self, args):
        main_app()


if __name__ == "__main__":
    App(sys.argv)
