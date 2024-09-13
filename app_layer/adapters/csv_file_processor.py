import os
from typing import Optional, Any, List
from app_layer.ports.file_processor import FileProcessor
from hr.models import HRModel

from payroll import models as payroll_models
from payroll.models import PayrollModel


class CsvFileProcessor(FileProcessor):
    """
    Class CsvFileProcessor

    This class is a subclass of FileProcessor and is responsible for processing CSV files and sending the processed content to an output adapter.

    Methods:
    - process_file(bucket_name: str, file_path: str, results: List[Optional[Any]] = None) -> bool
    - send_to_output(log: LogService, output_adapter, file_path: str, content: str)
    """

    def process_file(self, bucket_name: str, file_path: str):
        # log.deb(f'processing csv file: {file_path}...')
        is_valid = os.path.basename(file_path.lower()).startswith(('hrauto',
                                                                   'payrollauto'))

        if not is_valid:
            return False

        results = []
        file_type_mapping = {
            'hrauto': 'hr',
            'payrollauto': 'payroll'
        }

        # Determine file type based on prefix
        for prefix, filetype in file_type_mapping.items():
            if file_path.lower().startswith(prefix):
                results.append(dict(file_type=filetype))
                break

        # Get file type (without popping from list) from results list (value type dict)
        filetype = results[-1].get('file_type')

        # Extract file_name from file_path
        if filetype == 'hr':
            hr_model = HRModel()
            hr_model.parse_csv(bucket_name, file_path)
        elif filetype == 'payroll':
            payroll_model = PayrollModel()
            payroll_model.parse_csv(bucket_name, file_path)
        else:
            return False

        return True

    def send_to_output(self, output_adapter, file_path: str, content: str):
        output_adapter.send(file_path, content)
