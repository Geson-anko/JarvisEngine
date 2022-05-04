from . import run_project
from . import create_project
from .core import parsers


if __name__ == "__main__":
    parser = parsers.at_launching()
    args,unknow = parser.parse_known_args()
    
    if args.command ==  parsers.CREATE:
        create_project.create()
    elif args.command == parsers.RUN:
        run_project.run()
    
