from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import boto3
from botocore.exceptions import BotoCoreError, ClientError

input_bp = Blueprint('input', __name__, url_prefix='/input')

def get_all_instance_ids():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_instances()
        instance_list = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                name = next(
                    (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'),
                    'Unnamed' 
                )
                instance_list.append({
                    'InstanceId': instance_id,
                    'Name': name,
                    'State': state
                })

        return instance_list

    except (BotoCoreError, ClientError) as e:
        print(f"Error retrieving EC2 instances: {e}")
        return None

@input_bp.route('/', methods=['GET', 'POST'])
def input_form():
    if request.method == 'POST':
        selected_instance = request.form.get('instance_id')
        if not selected_instance:
            flash("Please select an instance", "error")
            return redirect(url_for('input.input_form'))

        # Store selected instance in session
        session['instance_id'] = selected_instance

        # Redirect to action handler
        return redirect(url_for('actions.instance_actions'))

    # Load instance options for dropdown
    instance_data = get_all_instance_ids()
    if instance_data is None:
        flash("❌ Error retrieving EC2 instances. Check AWS credentials or permissions.", "error")
        instance_data = []

    return render_template('input.html', instances=instance_data)
