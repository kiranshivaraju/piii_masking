# import boto3
# from pii_masker import PIIMasker
# from main import combined_names, organizations, locations

# def process_and_upload_files(s3_client, source_bucket, source_folder, target_folder):
#     # List all files in the source folder
#     objects = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=source_folder)

#     if 'Contents' in objects:
#         for obj in objects['Contents']:
#             file_key = obj['Key']
#             # Check if the object is a file and not just a folder name
#             if file_key.endswith('/'):
#                 continue
            
#             # Get the file content
#             file_obj = s3_client.get_object(Bucket=source_bucket, Key=file_key)
#             file_content = file_obj['Body'].read().decode('utf-8')

#             # Define new file name and path
#             new_file_name = file_key.split('/')[-1].replace('.txt', '_pii.txt')
#             new_file_key = f"{target_folder}/{new_file_name}"

#             masker = PIIMasker()
#             masker.set_fake_names(combined_names)
#             masker.set_fake_orgs(organizations)
#             masker.set_fake_locations(locations)
#             masked_text = masker.mask_all_pii(file_content)
#             # print(masked_text)
#             # print("**************")
#             # print("Mapping:", masker.get_mapping())

#             # Upload the file to the new location with the new name
#             s3_client.put_object(Bucket=source_bucket, Key=new_file_key, Body=masked_text)

#             print(f"File {file_key} processed and uploaded as {new_file_key}")

# def main():
#     # Define your bucket and folders
#     source_bucket = 'mai-support-test'
#     source_folder = 'processed_data_4kTextfiles/'
#     target_folder = 'pii4k'

#     # Initialize S3 client
#     s3_client = boto3.client('s3')

#     # Process and upload files
#     process_and_upload_files(s3_client, source_bucket, source_folder, target_folder)

# if __name__ == "__main__":
#     main()

import boto3
from pii_masker import PIIMasker
from main import combined_names, organizations, locations

def list_all_objects(s3_client, bucket, prefix):
    all_objects = []

    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' in response:
        all_objects.extend(response['Contents'])

    while response.get('IsTruncated', False):
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=response['NextContinuationToken'])
        if 'Contents' in response:
            all_objects.extend(response['Contents'])

    return all_objects

def process_and_upload_files(s3_client, source_bucket, source_folder, target_folder):
    # List all files in the source folder
    objects = list_all_objects(s3_client, source_bucket, source_folder)

    for obj in objects:
        file_key = obj['Key']
        # Check if the object is a file and not just a folder name
        if file_key.endswith('/'):
            continue
        
        # Get the file content
        file_obj = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        file_content = file_obj['Body'].read().decode('utf-8')

        # Define new file name and path
        new_file_name = file_key.split('/')[-1].replace('.txt', '_pii.txt')
        new_file_key = f"{target_folder}/{new_file_name}"

        masker = PIIMasker()
        masker.set_fake_names(combined_names)
        masker.set_fake_orgs(organizations)
        masker.set_fake_locations(locations)
        masked_text = masker.mask_all_pii(file_content)

        # Upload the file to the new location with the new name
        s3_client.put_object(Bucket=source_bucket, Key=new_file_key, Body=masked_text)

        print(f"File {file_key} processed and uploaded as {new_file_key}")

def main():
    # Define your bucket and folders
    source_bucket = 'insert_bucket_name_here'
    source_folder = 'insert_folder_name_here'
    target_folder = 'insert_folder_name_here'

    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Process and upload files
    process_and_upload_files(s3_client, source_bucket, source_folder, target_folder)

if __name__ == "__main__":
    main()

