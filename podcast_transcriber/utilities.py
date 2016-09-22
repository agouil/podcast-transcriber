import os
import shutil
import tempfile
import urllib2


TEMP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')


def check_env_vars():
    """
    Checks if all necessary ENV variables are set. If not, prints
    an error message.
    """

    if 'GOOGLE_API_KEY' not in os.environ:
        print "Google API key is missing.\n" \
            + "To add run `export GOOGLE_API_KEY=<your-api-key>"
        return False
    return True


def cleanup():
    shutil.rmtree(TEMP_DIR)


def create_ancillary_folders():
    if not os.path.exists(OUTPUT_DIR):
        print "Output directory absent. Creating output directory..."
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(TEMP_DIR):
        print "Creating tmp directory..."
        os.makedirs(TEMP_DIR)


def create_temporary_folder():
    """
    Creates a temporary directory to store all the intermediate files.
    """

    dirpath = tempfile.mkdtemp(dir=TEMP_DIR)
    print "Created tmp dir at ", dirpath
    return dirpath


def create_temporary_file_name(directory, suffix):
    """
    Creates a temporary file name.

    Params:
        directory (string): The directory of the temp file
        suffix (string): The temp file name
    """

    return os.path.join(directory, suffix)


def write_output_file(filename, contents):
    """
    Writes an output file to the directory defined by OUTPUT_DIR variable.

    Params:
        filename (string): The output file name
        contents (string): The contents of the file
    """

    with open(os.path.join(OUTPUT_DIR, filename + '.txt'), 'w') as output_file:
        output_file.write(contents)


def download_remote_file(url, dest):
    """
    Downloads a remote file to the specified location.

    Params:
        url  (string): The url of the remote file
        dest (string): The download destination
    """

    remote_file = urllib2.urlopen(url)
    meta_info = remote_file.info()
    file_size = int(meta_info.getheaders("Content-Length")[0])

    print "Downloading: %s" % url.split('/')[-1]

    file_size_dl = 0
    block_sz = 8192

    with open(dest, 'wb') as local_file:
        while True:
            buf = remote_file.read(block_sz)
            if not buf:
                break

            file_size_dl += len(buf)
            local_file.write(buf)

            status = r"Progress: %d / %d    [%3.2f%%]" % (
                file_size_dl, file_size, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,
    print "\nFile downloaded to: %s" % dest
