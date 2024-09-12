from app_layer.ports.output_service import OutputService


class S3OutputBucket(OutputService):
    def send(self, log, output_adapter, file_path: str, content: str):
        # Email sending logic goes here
        print(f'sending email with content: {content} for file: {file_path}')
