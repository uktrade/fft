from typing import Any, Optional, List
from app_layer.adapters.csv_file_processor import CsvFileProcessor
from app_layer.adapters.excel_file_processor import ExcelFileProcessor
from app_layer.adapters.s3_output_bucket import S3OutputBucket
from app_layer.log import LogService
from payroll import models


def process_data_input_source_files(log: LogService, file_paths: [str]) -> dict[str, Any]:
    # Basic validation check
    if not file_paths:
        log.war('no files to process. exiting...')
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
    log.deb('processing data input source files...')
    results: List[Optional[Any]] = [] # only contains payroll data (we do not store this object into the database)
    for bucket_name, files in buckets.items():
        for file_name, file_type in files.items():
            file_path = f"{bucket_name}/{file_name}"
            processor = processors.get(file_type)

            if processor:
                valid_file_processors[file_path] = processor if processor.process_file(bucket_name, file_path, results) else None
            else:
                log.err(f'no processor found for file: {file_name}')

    # HR service
    hr_model = models.HR()
    hr_model.update_records_with_basic_pay_superannuation_ernic_values(results.pop())

    # When ETL service is done, send the processed content to the output adapter
    s3_output_bucket = S3OutputBucket()

    return {'status_code': 200, 'message': 'all input processor files processed'}

