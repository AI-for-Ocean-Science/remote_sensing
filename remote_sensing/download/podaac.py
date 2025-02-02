""" Methods for downloading data from the PO.DAAC archive. 

Makes use of code taken from the podaac_data_downloader package script,
aka subscriber.podaac_data_downloader

"""

import os

from datetime import datetime, timedelta, timezone

from subscriber.podaac_data_downloader import main
from subscriber import podaac_access as pa

from urllib.error import HTTPError

from IPython import embed

page_size = 2000
provider = 'POCLOUD'

if os.getenv('OS_RS') is not None:
    podaac_path = os.path.join(os.getenv('OS_RS'), 'PODAAC')
else:
    podaac_path = os.path.join('./', 'PODAAC')

def grab_file_list(collection:str, verbose:bool=True,
               time_range:tuple=None,
               bbox:str=None):
    
    # Authenicate with Earthdata Login
    pa.setup_earthdata_login_auth(pa.edl)
    token = pa.get_token(pa.token_url)

    # Colleection ID
    collection_id = pa.get_cmr_collection_id(
        collection_short_name=collection,
        provider=provider,
        token=token,
        verbose=verbose)


    # Times
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if time_range is None:
        start_date_time = datetime.now(timezone.utc) - timedelta(weeks=1)
        start_date_time = start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date_time = now
    else:
        start_date_time, end_date_time = time_range

    temporal_range = pa.get_temporal_range(
        start_date_time, end_date_time, now)
    params = [
            ('page_size', page_size),
            ('sort_key', "-start_date"),
            ('provider', provider),
            ('ShortName', collection),
            ('temporal', temporal_range),
            ('token', token),
        ]
    if bbox is not None:
        params.append(('bounding_box', bbox))

    # If 401 is raised, refresh token and try one more time
    try:
        results = pa.get_search_results(params, verbose)
    except HTTPError as e:
        if e.code == 401:
            token = pa.refresh_token(token)
            # Updated: This is not always a dictionary...
            # in fact, here it's always a list of tuples
            for  i, p in enumerate(params) :
                if p[1] == "token":
                    params[i] = ("token", token)
            results = pa.get_search_results(params, verbose)
        else:
            raise e

    # Downloads
    downloads_all = []
    downloads_data = [[u['URL'] for u in r['umm']['RelatedUrls'] if
                       u['Type'] == "GET DATA" and ('Subtype' not in u or u['Subtype'] != "OPENDAP DATA")] for r in
                      results['items']]
    downloads_metadata = [[u['URL'] for u in r['umm']['RelatedUrls'] if u['Type'] == "EXTENDED METADATA"] for r in
                          results['items']]

    for f in downloads_data:
        downloads_all.append(f)
    for f in downloads_metadata:
        downloads_all.append(f)

    downloads = [item for sublist in downloads_all for item in sublist]

    # filter list based on extension
    filtered_downloads = []
    for f in downloads:
        for extension in pa.extensions:
            if pa.search_extension(extension, f):
                filtered_downloads.append(f)

    downloads = filtered_downloads
    checksums = pa.extract_checksums(results['items'])

    # Return
    return downloads, checksums


def download_files(file_list:list, 
                   download_dir:str=None, 
                   clobber:bool=False,
                   verbose:bool=True):
    """ Download files from the PO.DAAC archive.

    Parameters
    -----------
    file_list : list
        List of files to download.
    download_dir : str, optional
        Directory to download files to. Default is the podaac_path
        A sub-directory is created for each collection.
    clobber : bool, optional
        Overwrite existing files. Default is False.
    verbose : bool, optional
        Print verbose output. Default is True.

    Returns
    --------
    None

    """
    # Authenicate with Earthdata Login
    pa.setup_earthdata_login_auth(pa.edl)
    token = pa.get_token(pa.token_url)

    if download_dir is None:
        download_dir = podaac_path
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    # Loop on files
    success_cnt = failure_cnt = skip_cnt = 0
    for f in file_list:

        # Parse filename
        fparse = f.split('/')

        # Collection
        collection = fparse[-2]

        full_path = os.path.join(download_dir, collection)
        if not os.path.isdir(full_path):
            print(f'Creating directory: {full_path}')
            os.makedirs(full_path)

        # Filename
        filename = fparse[-1]


        # Download

        try:
            # -d flag, args.outputDirectory
            output_path = os.path.join(full_path, filename)
            
            # decide if we should actually download this file (e.g. we may already have the latest version)
            if os.path.isfile(output_path) and not clobber:# and pa.checksum_does_match(output_path, checksums)):
                print(f'File exists: {filename}\nUse clobber=True to overwrite')
                skip_cnt += 1
                continue

            pa.download_file(f,output_path)
            success_cnt = success_cnt + 1

            # Success
            print(f'File downloaded: {output_path}')

        except Exception:
            print(f'File failed to download: {filename}.') 
            failure_cnt = failure_cnt + 1