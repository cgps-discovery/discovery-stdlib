import time

"""
Text to be printed in the upload process
"""
prewords_upload_s3 = "Uploading results to digital ocean"

"""
Text to be printed in the fastq download process
"""
prewords_download_s3_fasta = "Downloading FASTA assembly"

"""
Text to be printed in the fastq download process
"""
prewords_download_s3_fastq = "Downloading FASTQ"

"""
Text to be printed in the process of saving results to file
"""
prewords_dict_to_gzjson = "Saving results"

"""
Text to be printed in the process of saving results to file
"""
prewords_save_fasta = "Saving stdin fasta to file"

"""
Extension of jsongz file
"""
jsongz_extension = ".json.gz"

"""
Temporary name of file with resuts in json.gz format
"""
temp_jsongz_name = str(time.time_ns())+"result"+jsongz_extension

"""
Name of file if fasta is gzipped
"""
gunzipped_fasta_name = str(time.time_ns())+"sequence.fasta"

"""
Name of downloaded fasta file
"""
download_fasta_name = str(time.time_ns())+"sequence.fa"