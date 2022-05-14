from plistlib import InvalidFileException
import requests
import argparse
import os
import time


def get_args():
    """Requests the CSV file location from the user.
        Returns:
                arguments: User response in the form of an argparse arguments object.
    """
    def is_path(given_path: str):
        if(os.path.exists(given_path) and os.path.isfile(given_path)):
            if (given_path[-3:] == "csv"):
                return given_path
            else:
                print("Argument must be a CSV file")
                raise InvalidFileException(given_path)
        else:
            print("Argument must be a file path")
            raise NotADirectoryError(given_path)

    parser = argparse.ArgumentParser(
        description="Upload csv to cloud.")
    parser.add_argument("path", type=is_path, help="Path to ECG CSV")
    parser.add_argument("key", type=str, help="GCP Key")
    args = parser.parse_args()
    return args


def send_file(csv: str, key: str):
    """Converts the dataframe of an ECG CSV into a model friendly format.
        Args:
                csv (str): Path to the ECG CSV.
    """
    url = "https://storage.googleapis.com/upload/storage/v1/b/PROJECT_DATA/o?uploadType=media&name=ECG_DATA.csv"
    headers = {
        "Authorization": "Bearer " + key,

    }
    print("Preparing CSV")
    payload = open(csv, 'rb')
    print("Uploading")
    post_request = requests.post(headers=headers, url=url, data=payload)
    print("Finished")
    print(post_request.status_code)
    print(post_request.content)


if __name__ == "__main__":
    arguments = get_args()
    curTime = time.time()
    send_file(arguments.path, arguments.key)
    print("TIME: "+str(time.time() - curTime))
