import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from layer.service import process_data_input_source_files

app_name = "fat"
region_name = 'us-west-1'


@csrf_exempt
def sns_notification(request):
    if request.method == 'POST':
        message = json.loads(request.body.decode('utf-8'))
        sns_message_type = request.META.get('HTTP_X_AMZ_SNS_MESSAGE_TYPE')

        if sns_message_type == 'SubscriptionConfirmation':
            # Handle subscription confirmation
            confirm_url = message['SubscribeURL']
            # Fetch the URL to confirm the subscription
            requests.get(confirm_url)
            return JsonResponse({'status': 'subscription confirmed'})

        elif sns_message_type == 'Notification':
            # Process the S3 event notification
            s3_info = json.loads(message['Message'])

            # Parse the S3 event notification
            buckets = {}
            for record in s3_info['Records']:
                bucket_name = record['s3']['bucket']['name']
                file_key = record['s3']['object']['key']
                file_name = file_key.split('/')[-1]  # Get the file name from the key
                file_type = file_name.split('.')[-1].lower()  # Get the file type

                # Store the file information in the buckets dictionary
                if bucket_name not in buckets:
                    buckets[bucket_name] = {}
                buckets[bucket_name][file_name] = file_type

            # Process the data input source files
            result = process_data_input_source_files(buckets)

            # Return the result
            return JsonResponse(result)

    return JsonResponse({'status': 'not allowed'}, status=405)
