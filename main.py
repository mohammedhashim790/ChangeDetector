from time import sleep

import requests
from mac_notifications import client
import os


def notify(icloud_id: str, message: str, title: str = ""):
    if icloud_id == "":
        raise Exception("icloud_id cannot be empty")
    if message == "":
        raise Exception("message cannot be empty")

    if title == "":
        title = "Website Update"

    notification_script = f"osascript send.applescript {icloud_id} \"{message}\""

    client.create_notification(
        title=title,
        subtitle=message,
    )
    os.system(notification_script)


if __name__ == "__main__":

    # Provide URL of website here.
    url = "{url}"

    # Keywords to search on the website
    keys = []

    firstHtmlText = ""

    sent = False

    durationRelax = 5

    if firstHtmlText == "":
        firstHtmlText = requests.get(url).text.lower()

    print("Sending Request")
    while True:
        try:
            text = requests.get(url).text.lower()
        except Exception as e:
            print(f"Exception {e}")

        if all(map(lambda x: x.lower() in text, keys)) or firstHtmlText != text:
            print("\n\n ******* Website Updated ******* \n\n")
            sent = True
            notify()
        else:
            print("\rNo Changes in Website", end="")

        sleep(durationRelax) if not sent else sleep(durationRelax * 5)
