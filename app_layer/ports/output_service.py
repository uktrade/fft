# ports/output_service.py

from abc import ABCMeta, abstractmethod


class OutputService(metaclass=ABCMeta):
    """
    This is the documentation for the `OutputService` class.

    Class: OutputService
    --------------------
    This is an abstract base class that defines the interface for sending output. It is meant to be subclassed and
    implemented by concrete output service classes.

    Methods
    -------
    send(file_path: str, content: str)
        This is an abstract method that subclasses must implement. It takes two parameters:
        - file_path: A string representing the file path where the output should be sent.
        - content: A string representing the content of the output.

        Note:
        - This method should be overridden in subclasses with the specific implementation logic for sending the output.

    Exceptions
    ----------
    None

    Example usage
    -------------
    ```
    class MyOutputService(OutputService):
        def send(self, log: LogService, ssm_client: BaseClient, file_path: str, content: str):
            # Implement the logic to send the output to the specified file path
            pass

    output_service = MyOutputService()
    output_service.send('/path/to/file.txt', 'Hello, World!')
    ```
    """
    @abstractmethod
    def send(self, ssm_client, file_path: str, content: str):
        pass
