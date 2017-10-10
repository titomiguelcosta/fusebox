import boto3
import os

client = boto3.client('ecs')
cluster = os.getenv("AWS_ECS_CLUSTER", "fusebox-cluster")
tasks = client.list_tasks(serviceName=os.getenv("AWS_ECS_SERVICE_NAME", "fusebox-service"), cluster=cluster)

for task in tasks["taskArns"]:
    client.stop_task(task=task, cluster=cluster, reason="deployed new version of the container")
