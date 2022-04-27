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

def at_creating() -> ArgumentParser:
    """
    The parser used at creating JarvisEngine project.
    This returns an Argument Parser inherited 
    `at_launching` and with the following options.
        - `-n`, `--name`
            The name of your JarvisEngine project.
        - `-d`, `--creating_dir`
            The directory in which the project will be generated.
            If not provided, the project will be generated into the `os.getcwd()`.
    """
    parser = at_launching()
    parser.add_argument("-n","--name",type=str,required=True,
                        help="The name of your project.")
    parser.add_argument("-d","--creating_dir", type=str, default="./",
                        help="The directory in which the project will be generated.")

    return parser

