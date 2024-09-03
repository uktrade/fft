import os

from app_layer.log import LogService
from app_layer.ports.file_processor import FileProcessor

from hr import models as hr_models
from payroll import models as payroll_models
from transaction import models as transaction_models
from zero_transaction import models as zero_transaction_models

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
        is_valid = os.path.basename(file_path.lower()).startswith(('actualsauto',
                                                                   'budgetauto',
                                                                   'hrauto',
                                                                   'payrollauto',
                                                                   'transactionsauto',
                                                                   'zeroauto'))
        # Extract file_name from file_path
        file_name = os.path.basename(file_path)

        if not is_valid:
            log.err(f'invalid csv file: {file_path}. will not process.')
        else:
            log.deb(f'valid csv file: {file_path}. will process.')
            log.deb(f'processing file: {file_name}...')

            # If file_name == hrauto then use parse the file and store in a dictionary using hr model from  hr.models.py
            if file_name.lower().startswith('hrauto'):
                hr_model = hr_models.HR()
                hr_model.parse_csv(file_path)

            # If file_name == payrollauto then use parse the file and store in a dictionary using payroll model from  hr.models.py
            elif file_name.lower().startswith('payrollauto'):
                payroll_model = payroll_models.Payroll()
                payroll_model.parse_csv(file_path)

            # If file_name == transactionsauto then use parse the file and store in a dictionary using transactions model from transaction.models.py
            elif file_name.lower().startswith('transactionsauto'):
                transactions_model = transaction_models.Transaction()
                transactions_model.parse_csv(file_path)

            # If file_name == zeroauto then use parse the file and store in a dictionary using budget model from zero_transaction.models.py
            elif file_name.lower().startswith('zeroauto'):
                zero_model = zero_transaction_models.ZeroTransaction()
                zero_model.parse_csv(file_path)

            else:
                log.deb(f'unknown file: {file_name}. will not continue processing.')
                return False

        log.deb(f'processed file: {file_name}')
        return is_valid

    def send_to_output(self, log: LogService, output_adapter, file_path: str, content: str):
        output_adapter.send(file_path, content)
