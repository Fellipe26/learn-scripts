# -*- coding: utf-8 -*-

import argparse
import boto3

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clusterName', help='Nome do Cluster',
                        required=True)
    parser.add_argument('--taskDefinition', help='Nome da Task Definition',
                        required=True)

    return parser.parse_args()

def run_task(clusterName, taskDefinition):
    client = boto3.client('ecs')
    response = client.run_task(
        cluster=clusterName,
        taskDefinition=taskDefinition,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-f62cafaf',
                    'subnet-b7adc0c0'
                ],
                'assignPublicIp': 'DISABLED',
            }
        }
    )
    return str(response)

args = parse_input()
resp = run_task(args.clusterName, args.taskDefinition)
print ("Fim da execução do job")
