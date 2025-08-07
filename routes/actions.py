from flask import Blueprint, render_template, session, request, flash
import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Boto3 clients
ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')

# Flask Blueprint
actions_bp = Blueprint('actions', __name__, url_prefix='/actions')

@actions_bp.route('/', methods=['GET', 'POST'])
def instance_actions():
    instance_id = session.get('instance_id')

    if not instance_id:
        flash("❌ Instance ID not found in session.", "error")
        return render_template('actions.html', instance_id=None)

    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'Disassociate Public IP':
                disassociate_public_ip(instance_id)
            elif action == 'Detach from Load Balancer':
                detach_from_load_balancer(instance_id)
            elif action == 'Modify SG to Quarantine':
                apply_quarantine_sg(instance_id)
            elif action == 'Create Forensic AMI':
                create_forensic_ami(instance_id)
            elif action == 'Move to Quarantine Subnet':
                move_to_quarantine_subnet(instance_id)

            flash(f"✅ Action '{action}' completed for instance {instance_id}", "success")

        except Exception as e:
            flash(f"❌ Error performing '{action}': {str(e)}", "error")

    return render_template('actions.html', instance_id=instance_id)


# ---------- Helper Functions ----------

def disassociate_public_ip(instance_id):
    # Elastic IP disassociation
    addresses = ec2.describe_addresses(Filters=[
        {'Name': 'instance-id', 'Values': [instance_id]}
    ])
    for addr in addresses.get('Addresses', []):
        assoc_id = addr.get('AssociationId')
        if assoc_id:
            ec2.disassociate_address(AssociationId=assoc_id)

    # Stop, modify, and restart instance to clear auto-assigned IP
    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    eni_id = instance['NetworkInterfaces'][0]['NetworkInterfaceId']

    ec2.stop_instances(InstanceIds=[instance_id])
    ec2.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])

    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        SourceDestCheck={'Value': False}
    )

    ec2.modify_network_interface_attribute(
        NetworkInterfaceId=eni_id,
        Attachment={
            'AttachmentId': instance['NetworkInterfaces'][0]['Attachment']['AttachmentId'],
            'DeleteOnTermination': True
        }
    )

    ec2.start_instances(InstanceIds=[instance_id])


def detach_from_load_balancer(instance_id):
    # NOTE: Replace with real logic to look up target groups dynamically
    # Example (static TargetGroupArn):
    target_group_arn = 'arn:aws:elasticloadbalancing:region:account-id:targetgroup/your-tg/abc123'

    targets = elbv2.describe_target_health(TargetGroupArn=target_group_arn)
    for tg in targets['TargetHealthDescriptions']:
        if tg['Target']['Id'] == instance_id:
            elbv2.deregister_targets(
                TargetGroupArn=target_group_arn,
                Targets=[{'Id': instance_id}]
            )


def apply_quarantine_sg(instance_id):
    quarantine_sg_id = 'sg-xxxxxxxxxxxxxxxxx'  # Replace with your quarantine SG ID
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[quarantine_sg_id]
    )


def create_forensic_ami(instance_id):
    ec2.create_image(
        InstanceId=instance_id,
        Name=f"Forensic-AMI-{instance_id}",
        NoReboot=True
    )


def move_to_quarantine_subnet(instance_id):
    new_subnet_id = 'subnet-xxxxxxxxxxxxxxx'  # Replace with your quarantine subnet ID

    ec2.stop_instances(InstanceIds=[instance_id])
    ec2.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])

    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    eni_id = instance['NetworkInterfaces'][0]['NetworkInterfaceId']
    attachment_id = instance['NetworkInterfaces'][0]['Attachment']['AttachmentId']

    ec2.detach_network_interface(AttachmentId=attachment_id, Force=True)
    ec2.delete_network_interface(NetworkInterfaceId=eni_id)

    new_eni = ec2.create_network_interface(
        SubnetId=new_subnet_id,
        Groups=[sg['GroupId'] for sg in instance['SecurityGroups']]
    )

    ec2.attach_network_interface(
        NetworkInterfaceId=new_eni['NetworkInterface']['NetworkInterfaceId'],
        InstanceId=instance_id,
        DeviceIndex=0
    )

    ec2.start_instances(InstanceIds=[instance_id])
