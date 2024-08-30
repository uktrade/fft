import boto3
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .layer.service import process_data_input_source_files
from .log import LogService, LogLevel
from .serializers import S3EventSerializer
from transaction.serializers import TransactionSerializer
from django.db import transaction as db_transaction

app_name = "fat"
log = LogService().build(app_name, LogLevel.DEBUG)

# SSM client
ssm_client = boto3.client('ssm', region_name='us-west-1')

@api_view(['POST'])
def s3_event(request):
    serializer = S3EventSerializer(data=request.data)
    if serializer.is_valid():
        bucket = serializer.validated_data['bucket']
        key = serializer.validated_data['key']

        # Get all objects from S3 bucket
        s3 = boto3.client('s3', region_name='us-west-1')
        objects = s3.list_objects_v2(Bucket=bucket)
        if not objects.get('Contents'):
            log.deb(f'no objects found in bucket: {bucket}. will not proceed')
            return

        log.deb(f'objects found in bucket: {bucket}. processing...')

        # Get all file paths
        file_paths = [obj['Key'] for obj in objects['Contents']]

        # Process the oracle input source files
        result = process_data_input_source_files(log, ssm_client, file_paths)

    return


# External API endpoint
# ---------------------
# To allow data workspace to contact fft for data

@api_view(['GET'])
@db_transaction.atomic
def get_latest(request):
    if request.method == 'GET':
        # Below is an example of how to use the TransactionSerializer, not the actual implementation
        # of the get_latest function.
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)