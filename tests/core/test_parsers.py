from JarvisEngine.core import parsers

def test_at_launching():
    parser = parsers.at_launching()
    argv = ["create"]
    args = parser.parse_args(argv)
    assert args.command == "create"

    argv = ["run"]
    args = parser.parse_args(argv)
    assert args.command == "run"

    argv = ["invalid command"]
    try:
        parser.parse_args(argv)
        raise AssertionError("Invalid command was recognized!")
    except SystemExit: pass

