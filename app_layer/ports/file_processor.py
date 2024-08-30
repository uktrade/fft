from abc import ABCMeta, abstractmethod


class FileProcessor(metaclass=ABCMeta):
    """
    This code defines an abstract base class called FileProcessor.

    It is designed to be subclassed by other classes that will implement the functionality of processing a file and
    sending the processed content to an output adapter.

    The class has two abstract methods:

    1. process_file(self, file_path: str):
       - This method is responsible for processing the content of a file located at the given file_path.
       - Subclasses must override this method and provide their own implementation.

    2. send_to_output(self, output_adapter, file_path: str, content: str):
       - This method is responsible for sending the processed content to an output adapter.
       - It takes an output_adapter object, the file_path of the processed file, and the content that needs to be sent.
       - Subclasses must override this method and provide their own implementation.

    This class should not be instantiated directly. Instead, it should be used as a base class for implementing specific
    file processing functionality.
    """
    @abstractmethod
    def process_file(self, log, file_path: str):
        """
        This method is an abstract method that should be overridden by a subclass.

        Parameters:
        - log: An instance of the LogService class used for logging.
        - file_path: The path of the file to be processed.
        - file_path: str

        Returns:
        None

        This method is an abstract method and must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def send_to_output(self, log, output_adapter, file_path: str, content: str):
        """
        send_to_output(self, log: LogService, output_adapter, file_path: str, content: str)

        Sends the specified content to the output using the provided output adapter.

        Parameters:
        - log (LogService): The log service to use for logging events and errors.
        - output_adapter: The output adapter that handles the specific output mechanism.
        - file_path (str): The path to the file where the content will be sent.
        - content (str): The content to send.

        Returns:
        None

        This method is an abstract method and must be implemented by subclasses.
        """
        pass