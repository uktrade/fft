from typing import Any
from app_layer.adapters.csv_file_processor import CsvFileProcessor
from app_layer.adapters.excel_file_processor import ExcelFileProcessor
from app_layer.adapters.s3_output_bucket import S3OutputBucket
from app_layer.log import LogService


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

    # Process each file and check if it is valid
    log.deb('processing data input source files...')
    for bucket_name, files in buckets.items():
        for file_name, file_type in files.items():
            file_path = f"{bucket_name}/{file_name}"
            processor = processors.get(file_type)

            if processor:
                valid_file_processors[file_path] = processor if processor.process_file(log, file_path) else None
            else:
                log.err(f'no processor found for file: {file_name}')

    # We can now send these data file processors to the etl process.
    log.deb('all oracle processor files are valid. handover to etl service...')

    # When ETL service is done, send the processed content to the output adapter
    s3_output_bucket = S3OutputBucket()

    return {'status_code': 200, 'message': 'all input processor files processed'}

