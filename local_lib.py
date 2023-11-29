import sys
import os

from .util import get_fileid, sha1sum, printer, test_fasta
from .do_lib import download_s3_fasta
from .text import prewords_save_fasta, download_fasta_name

def stdin_to_fasta(working_dir,is_verbose):
    """
    Takes text passed in as stdin and saves it to file
    :param working_dir: working directory
    :param is_verbose: True if verbose
    :return: path to saved file
    """
    
    PRE_WORDS = prewords_save_fasta

    if is_verbose: printer(PRE_WORDS)

    save_path = os.path.join( working_dir, download_fasta_name )

    try:
        os.mkdir(working_dir)
    except Exception as e:
        pass

    fasta = open(save_path, "w")

    for line in sys.stdin:
        fasta.write(line)
    
    return test_fasta( save_path )


def evaluate_fasta_input (fasta_s3_path,working_dir,is_verbose):
    """
    Evaluates if the fasta_s3_path is given. If given then download fasta from s3,
    otherwise save stdin to file
    :param fasta_s3_path: provided path to s3 fasta
    :param working_dir: working directory
    :return: id of file to be evaluated and path to fasta file 
    """
    
    if fasta_s3_path is None:
        fasta_path = stdin_to_fasta(working_dir,is_verbose)
        fileid = sha1sum(fasta_path)
    else:
        fileid = get_fileid(fasta_s3_path, is_verbose)
        fasta_path = download_s3_fasta(fasta_s3_path, working_dir, is_verbose)
    
    return (fileid, fasta_path)