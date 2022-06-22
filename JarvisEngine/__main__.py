from . import create_project, run_project
from .core import argument_parsers

if __name__ == "__main__":
    parser = argument_parsers.at_launching()
    args, unknow = parser.parse_known_args()

    if args.command == argument_parsers.CREATE:
        create_project.create()
    elif args.command == argument_parsers.RUN:
        run_project.run()
