from argparse import ArgumentParser
import logging

def at_launching() -> ArgumentParser:
    """
    The parser used at lauching JarvisEngine.
    An Argument Parser class with the following options is returned.
        - command
            The running mode of JarvisEngine.
            If "create", Engine creates a project according to the template.
            If "run", Engine runs your project.

        - `-ll`,`--log_level`
            The log level when running JarvisEngine processes.
            The level names follow the standard python library logging.
    """
    parser = ArgumentParser()
    parser.add_argument("command",type=str,choices=["create", "run"],
                        help="Running mode of JarvisEngine")
    parser.add_argument("-ll","--log_level", type=str, default="DEBUG",
                        choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],
                        help="The log level when running JarvisEngine processes.")

    return parser

