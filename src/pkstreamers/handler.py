###########################################################
#
# ---%%%  CLASS Handler: Open subprocess for continuous I/O handling  %%%---
#

import logging
import os
import tempfile

logger = logging.getLogger(__name__)

from .reader import SubprocessReader


class SubprocessHandler(SubprocessReader):
    def __init__(self, command, input=[], *args, **kwargs):
        """Open a process with subprocess and read and write to it.
        command: The command to execute.
        input:   The data to write to the process.
        """
        self.temp_input_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        logger.debug(f" Temporary file created = '{self.temp_input_file.name}'")
        for line in input:
            logger.debug(f" Writing to temp file - '{str(line)}'")
            self.write_to_temp_file(f"{str(line)}\n")
        logger.debug(f" Something")

        myfileobj = open(self.temp_input_file.name, 'r')
        super().__init__(command, stdin=myfileobj, *args, **kwargs)
        logger.debug(f"  {self} - Initialized by Handler")

    def write_to_temp_file(self, input_str):
        self.temp_input_file.write(input_str)
        self.temp_input_file.flush()

    def close_temp_file(self):
        self.temp_input_file.close()
        os.remove(self.temp_input_file.name)

    def close(self):
        self.close_temp_file()
        super().close()

# Example usage
if __name__ == "__main__":
    command = ["your_command_here"]
    with SubprocessHandler(command) as handler:
        handler.write_to_temp_file("Some input")
        for output_line in handler:
            print(output_line)

