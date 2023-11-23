import os
import sys
import gzip
import json
import shutil
import FastaValidator
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path
from .text import prewords_dict_to_gzjson, temp_jsongz_name, gunzipped_fasta_name


def printer(input_str):
    """
    Prints string with leading green-coloured date and time
    :param input_str: string to be added a prefix
    """
    
    now = datetime.now()
    now_str =  now.strftime("%Y-%m-%d %H:%M:%S")

    print( "\033[92m \033[1m "+now_str+" \033[0m "+input_str )


def test_fasta(file_path):
    """
    Returns empty if file is not fasta
    :param file_path: path to fasta file
    :return: empty if file not fasta
    """
    
    if FastaValidator.fasta_validator(file_path) != 0:
        file_path = None
        print('[ERROR] File not in FASTA format', file=sys.stderr)
        
    return file_path


def is_gz_file(filepath):
    """
    Checks if file is gzipped
    :param filepath: file to be checked
    :return: True if file is gzipped
    """

    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'

    
def gunzip_if_zipped(fasta_download, working_dir):
    """
    If file is gzipped it returns gunzipped file
    :param fasta_download: path to downloaded fasta
    :param working_dir: working directory
    :return: path to non gzipped fasta file
    """
    
    if is_gz_file(fasta_download):

        gunzipped_path = os.path.join(working_dir, gunzipped_fasta_name)
        
        with gzip.open(fasta_download, 'rb') as f_in:
            with open(gunzipped_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        fasta_download = gunzipped_path

    return fasta_download


def get_fileid(url, is_verbose):
    """
    Gets file id given an s3 url
    :param url: s3 path to get fileid from
    :return: the fileid of the genome
    """

    parsed_url = urlparse(url)
    key = Path(parsed_url.path).stem.split(".")[0]

    return key


def dict_to_gzjson(r_dict, working_dir, is_verbose):
    """
    Saves dictionary containing results as gzipped json
    :param r_dict: Dictionary to be recorded as json
    :param working_dir: working directory
    :param is_verbose: True if verbose
    :return: path to gzipped json with the result
    """

    PRE_WORDS = prewords_dict_to_gzjson
    TEMP_JSONGZ_NAME = temp_jsongz_name

    if is_verbose: printer(PRE_WORDS)

    file_path = os.path.join(working_dir, TEMP_JSONGZ_NAME)

    with gzip.open(file_path, 'wt') as f:
        json.dump(r_dict, f)

    return file_path


def get_upload_path(base, fileid, extension):
    """
    Sets string to be used as path for upload
    :param base: the base of the url
    :param fileid: the id of the genome of the analysis
    :param extension: extension of the analysis record
    :return: the url to be used for upload
    """

    return os.path.join(base,fileid[:2],fileid+extension)