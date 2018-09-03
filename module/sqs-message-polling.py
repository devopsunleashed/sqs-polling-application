import boto3
import time

# Create boto3 SQS client
sqs = boto3.client('sqs')

queue_url = 'SQS QUEUE URL HERE'

# The duration (in seconds) that the received messages are hidden from subsequent retrieve requests after being
# retrieved by a ReceiveMessage request.
visibility_timeout = 30

# The duration (in seconds) for which the call waits for a message to arrive in the queue before returning.
# If a message is available, the call returns sooner than WaitTimeSeconds.
# If no messages are available and the wait time expires, the call returns successfully with an empty list of messages.
wait_time_seconds = 20

# The maximum number of messages to return. Amazon SQS never returns more messages than this value
# (however, fewer messages might be returned). Valid values are 1 to 10. Default is 1.
max_number_of_messages = 1

# Delete received message from queue
def removeMessageFromQueue(receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle)
    print('Deleted message from queue: %s' % receipt_handle)

while 1:
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=max_number_of_messages,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=visibility_timeout,
        WaitTimeSeconds=wait_time_seconds
    )

    if 'Messages' in response:
        message=response['Messages'][0]
        receipt_handle=message['ReceiptHandle']
        print(message)

        # This is where we would do some file processing and other tasks
        time.sleep(20)

        # If processing is good, we could remove the message from the queue, else skip removal
        removeMessageFromQueue(receipt_handle)
    else:
        print("No messages on the queue to process")
