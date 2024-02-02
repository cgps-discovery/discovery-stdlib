import os
import boto3
import requests
import botocore
from urllib.parse import urlparse

from .text import prewords_upload_s3, prewords_download_s3_fasta, download_fasta_name, prewords_download_s3_fastq
from .util import printer, test_fasta, gunzip_if_zipped

def get_secrets():
    """
    Retrieves secrets for digital ocean
    :return: key and secret
    """
    
    spaces_key = os.environ['SPACES_KEY']
    spaces_secret = os.environ['SPACES_SECRET']
    
    return (spaces_key, spaces_secret)


def parse_url(url):
    """
    Evaluates an s3 url into the information to communicate with digital ocean
    :param url: s3 path to get information from
    :return: parsed information from s3 link
    """
    
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc.split(".")
    bucket, region = netloc[0], netloc[-3]
    endpoint = ".".join(netloc[1:])
    endpoint = scheme+"://"+endpoint
    
    key = parsed_url.path[1:]
    return region, endpoint, bucket, key


def upload_s3(s3_path,file,content_type,is_verbose):
    """
    Uploads file to s3 bucket
    :param s3_path: url to which the file will be uploaded
    :param file: the path to the file to be uploaded
    :param content_type: the content-type of the file
    :param is_verbose: True if vebose
    """

    PRE_WORDS = prewords_upload_s3

    if is_verbose: printer(PRE_WORDS)

    # Parse url to get secret url
    region, endpoint, bucket, key = parse_url(s3_path) 
    # Get Digital Ocean client
    client = get_do_client(region, endpoint)
    # Arguments for uploading
    extra_args = {'ACL': "private", 'ContentType': content_type}
    # Upload file to private url
    try:
        client.upload_file(file,bucket,key,ExtraArgs=extra_args)
        if is_verbose: printer("Saved to:{}".format(s3_path))
    except Exception as e:
        return e


def download_s3_fastq(s3_path, download_fastq_name, working_dir, is_verbose):
    """
    Downloads gzipped assembly
    :param s3_path: url to file to be downloaded
    :working_dir: directory to save download
    :return: path to downloaded fastq
    """

    PRE_WORDS = prewords_download_s3_fastq

    if is_verbose: printer(PRE_WORDS)
    
    download_path = os.path.join(working_dir, download_fastq_name)

    try:
        os.mkdir(working_dir)
    except Exception as e:
        #printer("Error creating working directory: {}".format(e))
        #raise e
        pass

    # Parse url to get secret url
    region, endpoint, bucket, key = parse_url(s3_path)

    # Get secret url                                                                                                      
    secret_url = get_presigned_url(get_do_client(region, endpoint),bucket,key,'get_object')    

    # Download using secret url
    r = requests.get(secret_url, allow_redirects=True)
    open(download_path, 'wb').write(r.content)
    
    return os.path.join(download_path, working_dir)


def download_s3_fasta(s3_path, working_dir, is_verbose):
    """
    Downloads gzipped assembly
    :param s3_path: url to file to be downloaded
    :working_dir: directory to save download
    :return: path to downloaded fasta
    """

    PRE_WORDS = prewords_download_s3_fasta

    if is_verbose: printer(PRE_WORDS)
    
    download_path = os.path.join(working_dir, download_fasta_name)

    try:
        os.mkdir(working_dir)
    except Exception as e:
        #printer("Error creating working directory: {}".format(e))
        #raise e
        pass

    # Parse url to get secret url
    region, endpoint, bucket, key = parse_url(s3_path)

    # Get secret url                                                                                                      
    secret_url = get_presigned_url(get_do_client(region, endpoint),bucket,key,'get_object')    

    # Download using secret url
    r = requests.get(secret_url, allow_redirects=True)
    open(download_path, 'wb').write(r.content)
    
    return test_fasta( gunzip_if_zipped(download_path, working_dir) )


def get_presigned_url(client,bucket,url, object):
    """
    Gets presigned url of private
    :param client: digital ocean client 
    :param bucket: digital ocean bucket
    :param url: key to the digital ocean item 
    :param object: type of object for the clent method
    :return: The presigned url from private file
    """
    
    url = client.generate_presigned_url(ClientMethod=object,
                                        Params={'Bucket': bucket,
                                                'Key': url},
                                        ExpiresIn=300)
    return url


def get_do_client(r_name, ep_url):
    """
    Retrieves digital ocean client 
    :param r_name: region to access
    :param ep_url: endpoint address
    Return client to get presigned url
    """
    SPACES_KEY, SPACES_SECRET = get_secrets()

    session = boto3.session.Session()
    client = session.client('s3',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                            region_name=r_name,
                            endpoint_url=ep_url,
                            aws_access_key_id=SPACES_KEY,
                            aws_secret_access_key=SPACES_SECRET)
    return client