###########################################################
#
# ---%%%  CLASS Handler: Open subprocess for continuous I/O handling  %%%---
#

import logging
import subprocess
import threading

logger = logging.getLogger(__name__)

from .reader import SubprocessReader

# TODO: The whole tempfile stuff could probably be done faster with threading and piping...

class SubprocessHandler(SubprocessReader):
    def __init__(self, command, input_data=[], *args, **kwargs):
        """Open a process with subprocess and read and write to it.
        command: The command to execute.
        input:   The data to write to the process.
        """
        super().__init__(command, stdin=subprocess.PIPE, *args, **kwargs)
        self.thread = threading.Thread(target=self.write_to_process, args=(input_data,))
        self.thread.start()
        logger.debug(f" {self} - Initialized by Handler")

    def write_to_process(self, input_data):
        try:
            for line in input_data:
                processed_line = f"{str(line).rstrip()}\n"
                self.process.stdin.write(processed_line)
            self.process.stdin.close()
        except Exception as e:
            logger.error(f" Error writing to subprocess: {e}")
        logger.debug(f" {self} - Data written to subprocess")

    def close(self):
        self.thread.join()  # Wait for the input thread to finish (this will hang if used like 'snptool | head')
        if self.process:
            self.process.terminate()  # Or .wait() to let it finish
        super().close()

# Example usage
if __name__ == "__main__":
    command = ["your_command_here"]
    with SubprocessHandler(command) as handler:
        handler.write_to_temp_file("Some input")
        for output_line in handler:
            print(output_line)

