###########################################################
#
# ---%%%  CLASS Reader: Open subprocess and read input  %%%---
#

# -%  Perform Basic Setup  %-

import logging
import queue
import subprocess
import threading

logger = logging.getLogger(__name__)

# TODO: check_errors() isn't finished...

class SubprocessReader:
    def __init__(self, command, *args, **kwargs):
        """Open a process with subprocess and read from it.
        command: The command to execute.
        """
        logger.info(f" Executing command = '{repr(command)}'")
        self.process = subprocess.Popen(
            command,
            *args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            **kwargs
        )
        self.error_queue = queue.Queue()
        self._start_error_monitor()
        SubprocessReader._validate(self)
        logger.debug(f" {self} - Initialized by Reader")

    def _start_error_monitor(self):
        """Start the error monnitoring child thread."""
        self.stderr_thread = threading.Thread(target=self._monitor_stderr)
        self.stderr_thread.start()
        logger.debug(f" {self} - Started Error Tracker")

    def _monitor_stderr(self):
        """Monitor function which runs in the child thread."""
        for line in self.process.stderr:
            self._handle_error(line.strip())

    def _handle_error(self, error_message):
        """Defines error handling"""
        self.error_queue.put(error_message)
        logger.debug(f" {self} - Detected an error: {error_message}")

    @staticmethod
    def _validate(self):
        """Validate stuff..."""
        # Check if the Popen call generated errors:
        self.check_errors()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Check the error queue 
        self.check_errors()
        self.close()

    def __iter__(self):
        logger.debug(f" {self} - Starting Iteration")
        return self

    def __next__(self):
        if self.process.poll() is not None:
            line = next(self.process.stdout)
            if line == '':
                raise StopIteration
            else:
                return line.strip()

        line = next(self.process.stdout)
        if line:
            return line.strip()
        else:
            raise StopIteration

    def check_errors(self):
        """Check if there are any errors and handle them"""
        while not self.error_queue.empty():
            error_message = self.error_queue.get()
            # Handle the error message (e.g., log, print, raise exception)
            logger.error(f" {error_message}")

    def close(self):
        if self.process.stdout:
            self.process.stdout.close()
        if self.process.stderr:
            self.process.stderr.close()
        self.process.terminate()
        self.process.wait()
        self.stderr_thread.join()
        logger.debug(f" {self} - Closed")
