from typing import Any
from botocore.client import BaseClient
from app_layer.adapters.csv_file_processor import CsvFileProcessor
from app_layer.adapters.excel_file_processor import ExcelFileProcessor
from app_layer.adapters.s3_output_bucket import S3OutputBucket


def process_data_input_source_files(log, ssm_client: BaseClient, file_paths: [str]) -> dict[str, Any]:
    # Basic validation check
    if not file_paths:
        log.war('no files to process. exiting...')
        return {'status_code': 204, 'message': 'no files to process'}

    # Get file types from all file paths
    file_types = [file_path.split('.')[-1].lower() for file_path in file_paths]

    processors = {
        'csv': CsvFileProcessor(),
        'xlsx': ExcelFileProcessor(),
        'xls': ExcelFileProcessor()
    }

    # Dictionary to store valid data file processors
    valid_file_processors = {}

    # Process each file and check if it is valid
    log.deb('processing data input source files...')
    for file_path, file_type in zip(file_paths, file_types):
        processor = processors[file_type]
        valid_file_processors[file_path] = processor if processor.process_file(log, file_path) else None

    # If we don't have 5 data file processors, then return
    if len(valid_file_processors) < 5:
        log.deb('insufficient number of data files. unable to start etl service')
        return {'status_code': 400, 'message': 'insufficient number of data files'}

    if len(valid_file_processors) > 5:
        log.war('more than 5 data files found in the input source. unable to start etl service')
        return {'status_code': 413, 'message': 'more than 5 oracle processor files found in the input'}

    # We can now send these data file processors to the etl process.
    log.deb('all oracle processor files are valid. handover to etl service...')
    
    

    # When ETL service is done, send the processed content to the output adapter
    s3_output_bucket = S3OutputBucket()

    return {'status_code': 200, 'message': 'all oracle processor files processed'}

