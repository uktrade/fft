#  Pixel Code
#  Email: haresh@pixelcode.uk
#
#  Copyright (c) 2024.
#
#  All rights reserved.
#
#  No part of this code may be used or reproduced in any manner whatsoever without the prior written consent of the author.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
#  SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  For permission requests, write to the author, at the email address above.

"""
log.py is a utility module that provides logging functionality for the runtime.

The module provides a LogService class that can be used to log messages at different log levels.
The LogService class uses the aws_lambda_powertools library to provide logging functionality.

The LogLevel enumeration defines the different log levels that can be used in the logger.

The LogService class provides methods to log messages at different log levels, such as INFO, DEBUG, WARNING, ERROR, and
    CRITICAL.
The class also provides a method to set the log level of the logger.

The LogService class uses the inspect and traceback modules to build log messages with additional information such as
    the function name, line number, and exception details.

The LogService class is designed to be used as a utility class to provide logging functionality in the runtime code.

Example usage:

        log_service = LogService()
        log_service.build("MyService", LogLevel.INFO)
        log_service.inf("This is an info message")
        log_service.deb("This is a debug message")
        log_service.war("This is a warning message")
        log_service.err("This is an error message")
        log_service.cri("This is a critical message")
        log_service.set_log_level(LogLevel.DEBUG)
        log_service.deb("This is a debug message with log level DEBUG")
"""

import inspect
import traceback

from enum import Enum
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from runtime.chalicelib.exception import EmptyOrNoneValueException


class LogLevel(Enum):
    """
    LogLevel is an enumeration of the different log levels that can be used in the logger.
    """
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


def _log_message_builder(log_level: LogLevel, frame, message: str, exception: Exception = None,
                         add_trace: bool = False) -> dict:
    """
    Builds a log message with the given log level, frame, and message.

    Parameters
    ----------
    log_level : LogLevel
        The log level of the message (unused but kept for future use).
    frame : frame
        The frame object of the calling function.
    message : str
        The message to log.
    exception : Exception
        The exception to log.
    add_trace : bool
        Flag to add the traceback to the message.

    Returns
    -------
    dict
        The log message as a dictionary.

    Raises
    ------
    EmptyOrNoneValueException
        If the message argument is empty or None.
    """

    # create a dictionary to map, frame.f_code.co_name, frame.f_lineno

    stack_info = {
        'frame': frame.f_code.co_name,
        'line': frame.f_lineno
    }

    if message is None or message == "":
        message = "<no message provided>"

    stack_info['message'] = message


    if exception is not None:
        stack_info['exception'] = str(exception)

    if add_trace:
        stack_info['trace'] = traceback.format_exc()

    # create a json from dictionary
    return stack_info


class LogService(object):
    """
    LogService is a utility class that provides logging functionality.
    """

    def __init__(self):
        self._service_name = None
        self._logger = None

    def build(self, service_name: str, log_level: LogLevel = LogLevel.INFO) -> 'LogService':
        """
        Builds a logger with the given service name and log level.

        Parameters
        ----------
        service_name : str
            The name of the service.
        log_level : LogLevel
            The log level of the logger.

        Raises
        ------
        EmptyOrNoneValueException
            If the service_name argument is empty or None.
        """

        if service_name is None or service_name == "":
            raise EmptyOrNoneValueException.append_message("service_name argument cannot be empty (or none)")

        self._logger = Logger(service=service_name, level=log_level.value, log_record_order=["timestamp", "level", "message"])
        return self

    def inject_lambda_context(self, lambda_handler):
        """
        Decorator to inject the Lambda context into the logger.

        Parameters
        ----------
        lambda_handler : function
            The lambda handler function.

        Returns
        -------
        function
            The decorated lambda handler function.

        Example usage
        -------------
        @log_service.inject_lambda_context
        def lambda_handler(event, context):
            log_service.inf("This is an info message")
            return "Hello, World!"
        """

        def decorate(event, context: LambdaContext):
            self._logger.structure_logs(append=True, cold_start=self._logger.cold_start, lambda_context=context)
            return lambda_handler(event, context)

        return decorate

    def set_correlation_id_from_event(self, event: dict):
        """
        Sets the correlation id for the logger based on the event.

        Parameters
        ----------
        event : dict
            The event dictionary.
        """
        if event is None:
            self._logger.warn("event argument cannot be None. unable to set correlation id for logger")
            return

        request = APIGatewayProxyEvent(event)
        self._logger.set_correlation_id(request.request_context.request_id)

    def get_logger(self) -> Logger:
        """
        Returns the logger instance.

        Returns
        -------
        Logger
            The logger instance.
        """

        return self._logger

    def inf(self, message: str):
        """
        Logs an INFO message.

        Parameters
        ----------
        message : str
            The message to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.INFO,
                                           inspect.currentframe().f_back,
                                           message)
        self._logger.info(log_message)

    def deb(self, message: str):
        """
        Logs a DEBUG message.

        Parameters
        ----------
        message : str
            The message to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.DEBUG,
                                           inspect.currentframe().f_back,
                                           message)
        self._logger.debug(log_message)

    def war(self, message: str):
        """
        Logs a WARNING message.

        Parameters
        ----------
        message : str
            The message to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.WARNING,
                                           inspect.currentframe().f_back,
                                           message)
        self._logger.warning(log_message)

    def err(self, message: str):
        """
        Logs an ERROR message.

        Parameters
        ----------
        message : str
            The message to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.ERROR,
                                           inspect.currentframe().f_back,
                                           message)
        self._logger.error(log_message)

    def exc(self, message: str, exception: Exception):
        """
        Logs an ERROR message with an exception.

        Parameters
        ----------
        message : str
            The message to log.
        exception : Exception
            The exception to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.ERROR,
                                           inspect.currentframe().f_back,
                                           message,
                                           exception)
        self._logger.exception(log_message)

    def cri(self, message: str):
        """
        Logs a CRITICAL message.

        Parameters
        ----------
        message : str
            The message to log.

        Raises
        ------
        EmptyOrNoneValueException
            If the message argument is empty or None.
        """
        log_message = _log_message_builder(LogLevel.CRITICAL,
                                           inspect.currentframe().f_back,
                                           message)
        self._logger.critical(log_message)

    def set_log_level(self, log_level: LogLevel):
        """
        Sets the log level of the logger.

        Parameters
        ----------
        log_level : LogLevel
            The log level to set.
        """
        self._logger.setLevel(log_level.__str__())
