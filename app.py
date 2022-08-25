import base64
import json
import os
import re
import subprocess
from pprint import pprint


def handler(event, context):
    print("Event:")
    pprint(event)
    print("Context:")
    pprint(context)
    if "test" in event:
        return "hello world"
    with open("text.star", "r") as infile:
        template_file = infile.readlines()
    default_replace_dict = {
        "MESSAGE_TEXT": "template message",
        "HEX_COLOR": "ad97ef"
    }
    given_replace_dict = {}
    if "isBase64Encoded" in event:
        decoded = base64.b64decode(event.get("body", ""))
        given_replace_dict = json.loads(decoded).get("replacements", {})
    else:
        given_replace_dict = event.get("replacements", {})
    replace_dict = {**default_replace_dict, **given_replace_dict}
    output_file = re.sub(r"<(\w+?)>",
                         lambda match: replace_dict[match.group(1)],
                         ''.join(template_file))
    with open("/tmp/rendered.star", "w+") as outfile:
        outfile.write(output_file)
    subprocess.run(
        ["pixlet", "render", "/tmp/rendered.star", "-o", "/tmp/out.webp"])
    tidbyt_device_id = os.environ.get("TIDBYT_DEVICE_ID")
    tidbyt_api_token = os.environ.get("TIDBYT_API_TOKEN")
    push_subprocess = subprocess.run([
        "pixlet", "push", tidbyt_device_id, "/tmp/out.webp", "-t",
        tidbyt_api_token
    ])

    response = {"status": "failed"}
    if push_subprocess.returncode == 0:
        response["status"] = "success"

    return response
