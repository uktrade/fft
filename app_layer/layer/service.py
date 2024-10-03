from typing import Any
from app_layer.adapters.csv_file_processor import CsvFileProcessor
from app_layer.adapters.excel_file_processor import ExcelFileProcessor
from hr.models import HRModel


def process_data_input_source_files(file_paths: [str]) -> dict[str, Any]:
    if not file_paths:
        return {'status_code': 204, 'message': 'no files to process'}

    buckets = {}
    for path in file_paths:
        bucket_name, file_name = path.split('/', 1)
        file_type = file_name.split('.')[-1].lower()

        if bucket_name not in buckets:
            buckets[bucket_name] = {}
        buckets[bucket_name][file_name] = file_type

    processors = {
        'csv': CsvFileProcessor(),
        'xlsx': ExcelFileProcessor(),
        'xls': ExcelFileProcessor()
    }

    # Dictionary to store valid data file processors
    valid_file_processors = {}

    # Process each file and store the valid data file processors into database
    for bucket_name, files in buckets.items():
        for file_name, file_type in files.items():
            file_path = f'{bucket_name}/{file_name}'
            processor = processors.get(file_type)
            if processor:
                valid_file_processors[file_path] = processor \
                    if processor.process_file(bucket_name, file_path) \
                    else None
            else:
                return {'status_code': 400, 'message': 'invalid file type'}

    # HR service
    hr_model = HRModel()
    hr_model.update_records_with_basic_pay_superannuation_ernic_values()
    return {'status_code': 200, 'message': 'all input processor files processed'}

