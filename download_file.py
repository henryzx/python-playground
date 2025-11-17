import requests
import mimetypes
import os

def download_file(url, local_filename=None):
    """
    Downloads a file from a given URL and saves it locally.

    Args:
        url (str): The URL of the file to download.
        local_filename (str, optional): The name to save the file as. 
                                        If None, it tries to infer the filename from the URL.
    """
    
    # 1. Determine the local filename
    if local_filename is None:
        # Tries to get the filename from the URL path
        local_filename = url.split('/')[-1]
    
    print(f"Attempting to download file from: {url}")
    print(f"Saving as: {local_filename}")

    # 2. Start the request stream
    try:
        mime_type = ""
        # Use stream=True to download in chunks
        with requests.get(url, stream=True) as r:
            # Check for successful response
            r.raise_for_status() 
            mime_type = r.headers['Content-Type'].split(';')[0]
            # 3. Write content in chunks
            with open(local_filename, 'wb') as f:
                # 8192 bytes (8KB) is a common chunk size
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # 4. Verify and adjust file extension if necessary
        extension = mimetypes.guess_extension(mime_type, strict=False)
        if extension and not local_filename.endswith(extension):
            os.rename(local_filename, local_filename + extension)
        print(f"\n✅ Download successful! File saved to: {os.path.abspath(local_filename)}")
        return True

    except Exception as e:
        print(f"\n❌ An error occurred during download: {e}")
        return False
