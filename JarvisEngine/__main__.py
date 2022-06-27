from .engine import argument_parsers, create_project, run_project

if __name__ == "__main__":
    parser = argument_parsers.at_launching()
    args, unknow = parser.parse_known_args()

    if args.command == argument_parsers.CREATE:
        create_project.create()
    elif args.command == argument_parsers.RUN:
        run_project.run()
