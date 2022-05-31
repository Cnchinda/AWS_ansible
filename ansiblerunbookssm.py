import boto3
import botocore
import time
from github import github 

ec2client = boto3.resource('ec2')
ssm_client = boto3.client('ssm')
sns_client = boto3.client('sns')
snsarn="arn:aws:sns:us-east-1:180634412322:LambdaSsmAnsible"

username = 'Cnchinda'
token = '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'

login = requests.get('https://github.com/Cnchinda/AWS_ansible.git', auth=(username,token))

def lambda_handler(event=None, context=None):
    #get the instance id from event
    instance_id = event['detail']['instance-id']
    print(f'ec2_instanceID: {instance_id}')
    ec2instance = ec2client.Instance(instance_id)
    #Iterate over all tag values to get the tag value from key SSMAnsiblePlaybookName which should contain the playbookname
    #playbook = [tags['Value'] for tags in ec2instance.tags if tags['Key'] == 'SSMAnsiblePlaybookName']
    #Covert playbook into a string datatype
    #playbook =' '.join(map(str, playbook))
    #Check to see if playbook tag exist, if not tag it'll
    playbook = install_apache.yml
    if len(playbook) == 0:
        print(f'No SSMAnsiblePlaybookName Tag found on instance {instance_id}')
        return
    else: 
        #sleep 60 seconds. This allows for ec2 instance to be in appropriate state to accept a RunCommand
        time.sleep(60)
        #provides3 uri where the playbook is stored 
        playbook_url = https://github.com/Cnchinda/AWS_ansible.git/{playbook}" 
        params={
                'playbookurl':[playbook_url],
                'extravars':['SSM=True'],
                'timeoutSeconds' : ["120"]
            }
        ssm_response = ssm_client.send_command(
            InstanceIds = [ instance_id ],
            DocumentName = 'AWS-RunAnsiblePlaybook',
            Parameters = params
        )
        #sleep 60 seconds. This will allow SSM RunCommand to initiate and register a response
        time.sleep(60)
        command_id = ssm_response['Command']['CommandId']
        command_invocation_result = ssm_client.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
        ssm_cmd_status = command_invocation_result['Status']
        if ssm_cmd_status == 'Success':
            print(f"Ansible Playbook Applied successfuly on {instance_id}") 
            sns_client.publish(
                TargetArn=snsarn,
                Message=f"Ansible Playbook Applied successfuly on {instance_id}"
            )
        else:
            print(f"Ansible Playbook Apply Failed on {instance_id}") 
            sns_client.publish(
                TargetArn=snsarn,
                Message=f"Ansible Playbook Apply Failed on {instance_id}"
            )


