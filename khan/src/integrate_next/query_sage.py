import os
import requests
import pandas as pd
from sage_data_client import query

cookie = input("Please enter your authentication cookie: ")

start_time = "2024-06-09T15:00:00Z"
end_time = "2024-06-11T02:00:00.000Z"

filter_criteria = {
    "plugin": "registry.sagecontinuum.org/theone/imagesampler:0.3.0.*",
    "vsn": "W015"
}

df = query(start=start_time, end=end_time, filter=filter_criteria)

output_folder = "/home/"
for image_url in df.iloc[:, 2]:
    if 'top' in image_url.rsplit('/', 3)[1]:
        image_name = image_url.rsplit('/', 1)[-1]
        image_path = os.path.join(output_folder, image_name)
        response = requests.get(image_url, headers={"Cookie": f"auth_sagecontinuum_org_sessionid={cookie}"})
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
                print(f"Downloaded: {image_path}")
        else:
            print(f"Failed to download: {image_url}")
