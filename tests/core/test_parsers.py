from JarvisEngine.core import parsers
import argparse

def _parse_args(parser:argparse.ArgumentParser,argv:list[str]) -> argparse.Namespace:
    return parser.parse_args(argv)
    
def test_at_launching():
    parser = parsers.at_launching()

    # test command
    args = _parse_args(parser,["create"])
    assert args.command == "create"

    args = _parse_args(parser,["run"])
    assert args.command == "run"

    try:
        _parse_args(parser,["invalid command"])
        raise AssertionError("Invalid command was recognized!")
    except SystemExit: pass


