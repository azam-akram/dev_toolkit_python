import boto3
import json

class PauseResumeOrchService:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.sqs_client = boto3.client('sqs')

    def get_orch_service_functions_by_pattern(self, pattern):
        try:
            paginator = self.lambda_client.get_paginator('list_functions')
            response_iterator = paginator.paginate()
            
            matching_functions = []
            for response in response_iterator:
                functions = response.get('Functions', [])
                for function in functions:
                    function_name = function.get('FunctionName', '')
                    if pattern in function_name:
                        matching_functions.append(function_name)

            return matching_functions
        except Exception as e:
            print(f"An error occurred while retrieving lambda functions: {e}")
            return []

    def get_source_sqs_for_orch_service(self, lambda_function_name):
        try:
            response = self.lambda_client.list_event_source_mappings(FunctionName=lambda_function_name)

            sqs_queues = []
            for mapping in response['EventSourceMappings']:
                if mapping['EventSourceArn'].startswith('arn:aws:sqs'):
                    arn_parts = mapping['EventSourceArn'].split(':')
                    sqs_queue_name = arn_parts[-1]
                    sqs_queues.append(sqs_queue_name)

            return sqs_queues
        except Exception as e:
            print(f"An error occurred while retrieving list of event source mappings: {e}")
            return []

    def get_sqs_queue_arn(self, queue_name):
        try:
            response = self.sqs_client.get_queue_attributes(
                QueueUrl=queue_name,
                AttributeNames=['QueueArn']
            )
            return response['Attributes']['QueueArn']
        except Exception as e:
            print(f"An error occurred while retrieving sqs queue urls: {e}")
            return ""

    def find_sqs_trigger_uuid(self, lambda_function_name, sqs_queue_arn):
        try:
            response = self.lambda_client.list_event_source_mappings(FunctionName=lambda_function_name)
        
            for mapping in response['EventSourceMappings']:
                if mapping.get('EventSourceArn') == sqs_queue_arn:
                    return mapping['UUID']
        
            return None
        except Exception as e:
            print(f"An error occurred while retrieving sqs queue utrigger uuid: {e}")
            return None

    def enable_disable_lambda_sqs_trigger(self, lambda_function_name, sqs_queue_name, enable_trigger):
        try:
            sqs_queue_arn = self.get_sqs_queue_arn(sqs_queue_name)
            trigger_uuid = self.find_sqs_trigger_uuid(lambda_function_name, sqs_queue_arn)

            if trigger_uuid:
                self.lambda_client.update_event_source_mapping(
                    UUID=trigger_uuid,
                    Enabled=enable_trigger
                )
                action = "enabled" if enable_trigger else "disabled"
                print(f"SQS trigger {action} for Lambda function '{lambda_function_name}'.")
            else:
                print(f"No event source mapping found for Lambda function '{lambda_function_name}' and SQS queue '{sqs_queue_name}'.")
        except Exception as e:
            print(f"An error occurred while enabling/disabling SQS trigger: {e}")


if __name__ == "__main__":
    # Caution: Control Enabling and Disabling Orchestration Service Trigger by this flag. Use it with care.
    enable_trigger = True

    action = "Enabling" if enable_trigger else "Disabling"
    print(f"{action} Orchestration Service Lambda Functions")

    pRService = PauseResumeOrchService()
    och_service_lambda_functions = pRService.get_orch_service_functions_by_pattern('my-test-service')
    print(f"Matching Lambda functions: {json.dumps(och_service_lambda_functions, indent=4)}")
    
    for i in range(len(och_service_lambda_functions)):
        sqs_queues = pRService.get_source_sqs_for_orch_service(och_service_lambda_functions[i])

        if len(sqs_queues) == 0:
            print(f"No SQS queue associated, skipping pausing orch service : {och_service_lambda_functions[i]}")
            continue

        print(f"{action} event source mapping from SQS queues : {sqs_queues[0]} to Test Service Lambda: {och_service_lambda_functions[i]}")
        
        # All above are read actions - Following line is deliberately disable to avoid unwanted write actions.
        # Uncomment following line if you want to enable or disable orchestration service triggers from SQS
        #pRService.enable_disable_lambda_sqs_trigger(och_service_lambda_functions[i], sqs_queues[0], enable_trigger)
