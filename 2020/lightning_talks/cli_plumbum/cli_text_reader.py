import os
from plumbum import cli
from loguru import logger


# # Create CLI

class TextReader(cli.Application):
    verbose = cli.Flag(["v", "verbose"], help = "If given, I will be very talkative")

    def main(self, filename):
        if self.verbose:
            logger.info(f'Reading the file "{filename}"')
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'No file found at path "{filename}"')
        with open(filename, mode='r', encoding='utf-8') as fh:
            return fh.read()


# # Run CLI
#
# Only if this file is not imported as a module but run directly.

if __name__ == "__main__":
    TextReader.run()
