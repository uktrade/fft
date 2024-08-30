import os

from app_layer.log import LogService
from app_layer.ports.file_processor import FileProcessor


class CsvFileProcessor(FileProcessor):
    """
    Class CsvFileProcessor

    This class is a subclass of FileProcessor and is responsible for processing CSV files and sending the processed content to an output adapter.

    Methods:
    - process_file(file_path: str) -> str:
        This method takes a file path as input and reads the CSV file. It processes the DataFrame if needed and returns the string representation of the DataFrame.

    - send_to_output(output_adapter, file_path: str, content: str):
        This method takes an output adapter, file path, and content as input. It sends the content to the output adapter using the send() method of the adapter.

    """

    def process_file(self, log: LogService, file_path: str):
        log.deb(f'processing csv file: {file_path}...')
        is_valid = os.path.basename(file_path.lower()).startswith(('actualsdbt',
                                                                   'hrdbt',
                                                                   'payrolldbt',
                                                                   'transactionsdbt',
                                                                   'budget'))
        log.deb(f'processing csv file: {file_path} - valid[{is_valid}]')
        return is_valid

    def send_to_output(self, log: LogService, output_adapter, file_path: str, content: str):
        output_adapter.send(file_path, content)
