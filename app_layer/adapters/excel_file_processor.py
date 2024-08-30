# adapters/excel_file_processor.py

import os

from app_layer.ports.file_processor import FileProcessor


class ExcelFileProcessor(FileProcessor):
    def process_file(self, log, file_path: str):
        log.deb(f'processing excel file: {file_path}...')
        is_valid = os.path.basename(file_path).startswith('ActualsDBT')
        log.deb(f'processing excel file: {file_path} - valid[{is_valid}]')
        return is_valid

    def send_to_output(self, log, output_adapter, file_path: str, content: str):
        output_adapter.send(file_path, content)
