import os
from typing import Optional, Any, List

from app_layer.log import LogService
from app_layer.ports.file_processor import FileProcessor

from payroll import models as payroll_models

class CsvFileProcessor(FileProcessor):
    """
    Class CsvFileProcessor

    This class is a subclass of FileProcessor and is responsible for processing CSV files and sending the processed content to an output adapter.

    Methods:
    - process_file(bucket_name: str, file_path: str, results: List[Optional[Any]] = None) -> bool
    - send_to_output(log: LogService, output_adapter, file_path: str, content: str)
    """

    def process_file(self, bucket_name: str, file_path: str, results: List[Optional[Any]] = None):
        # log.deb(f'processing csv file: {file_path}...')
        is_valid = os.path.basename(file_path.lower()).startswith(('hrauto',
                                                                   'payrollauto'))


        if not is_valid:
        #     log.err(f'invalid csv file: {file_path}. will not process.')
            return False

        # Extract file_name from file_path
        file_name = os.path.basename(file_path)
        if file_name.lower().startswith('hrauto'):
            hr_model = payroll_models.HR()
            hr_model.parse_csv(bucket_name, file_path)
        elif file_name.lower().startswith('payrollauto'):
            payroll_model = payroll_models.Payroll()
            payroll_data = payroll_model.parse_csv(bucket_name, file_path)
            if results is not None:
                results.append(payroll_data)
        else:
            # log.deb(f'unknown file: {file_name}. will not continue processing.')
            return False

        # log.deb(f'processed file: {file_name}')
        return True

    def send_to_output(self, log: LogService, output_adapter, file_path: str, content: str):
        output_adapter.send(file_path, content)
