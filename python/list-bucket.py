# -*- coding: utf-8 -*-
import argparse
import csv
import re
import os
import boto3
import botocore
import sys
import time

current = time.time()

def parse_input(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--dirOrigem', help='bucket que será disponibilizado o csv.',
                        required=True)
    parser.add_argument('-d', '--downloadcsv', help='Nome do csv que será realizado o download.',
                        required=True)
    parser.add_argument('-c', '--csvFileName', help='Nome do arquivo que será realizado o "De Para" com o bucketName.',
                        required=True)
    parser.add_argument('-b', '--bucketName', help='Nome do bucket que será realizado o "De Para".',
                        required=True)
    
    return parser.parse_args()

"""Download do arquivo"""
print("Realizando o download do arquivo .csv")
s3Client = boto3.client('s3')
s3Resource = boto3.resource('s3')
try:
    s3Resource.Bucket('dirOrigem').download_file('downloadCsv', 'csvFileName')
except botocore.exceptions.Client.Error as e:
    if e.response['Error']['Code'] == "404":
        print("O objeto não existe.")
    else:
        raise
print("Download concluido...")

"""Listando o bucket do S3"""
print("Listando o conteudo do Bucket no S3...")
def get_all_s3_keys(bucket):
    s3 = boto3.client('s3')
    key = []
    kwargs = {'Bucket': bucket}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key.append(obj['Key'])
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
    return key

bucket_keys = get_all_s3_keys('bucket-Name-Comparation')
print("...Listagem concluida")

"""Comparando o conteudo do csv com o bucket"""
print("Comparando o csv com o Bucket")
allCSVRows = []
outputFile = open('diff_keys_bucket.txt', 'w')
with open('csvFileName', 'r', newline= '', encoding='utf-8') as csvfile:
    allCSVRows = csv.reader(csvfile, delimiter=';')

    keyscsv = [ re.sub(r'http.*smiles.com.br/',r'',x[3]) for x in allCSVRows]
    keys = list(set(keyscsv))
    
    keys_not_found = list(set(keys) - set(bucket_keys))
    
    for key in keys_not_found:
            print ("Item nao encontrado: {}".format(key), file=outputFile)
outputFile.close()
print("Comparacao finalizado")

end = time.time()
diff = end - current
print(Tempo total da execução) print(diff)
