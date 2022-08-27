import base64
import json
import os
import subprocess
import urllib.parse
from json.decoder import JSONDecodeError
from pprint import pprint


def handler(event, context):
    # log the Lambda event and context
    print("Event:")
    pprint(event)
    print("Context:")
    pprint(context)

    # shortuct for testing so we don't go through the whole rendering process
    if "test" in event:
        return "hello world"

    # load in the template
    with open("text.star", "r") as infile:
        template_file = infile.readlines()

    # default values to prevent failed executions
    default_replace_dict = {
        "MESSAGE_TEXT": "template message",
        "HEX_COLOR": "ad97ef",
        "SCROLL_SPEED": "100",
        "FONT": "6x13"
    }

    # handle case where data gets delivered directly
    # or is base64 encoded from API-Gateway endpoint
    given_replace_dict = {}
    if event.get("isBase64Encoded", False):
        decoded = base64.b64decode(event.get("body", ""))
        try:
            given_replace_dict = json.loads(decoded).get("replacements", {})
        except JSONDecodeError:
            form_data_parsed = {
                k: v[0]
                for k, v in urllib.parse.parse_qs(decoded.decode(
                    'utf-8')).items()
            }
            if "HEX_COLOR" in form_data_parsed:
                form_data_parsed["HEX_COLOR"] = form_data_parsed[
                    "HEX_COLOR"].replace("#", "")
            given_replace_dict = form_data_parsed

    else:
        given_replace_dict = event.get("replacements", {})

    # resolve given values with defaults, preferring given values
    replace_dict = {**default_replace_dict, **given_replace_dict}

    # replace variables in template
    output_file = ''.join(template_file).format(**replace_dict)

    # write the rendered template
    with open("/tmp/rendered.star", "w+") as outfile:
        outfile.write(output_file)

    # render the template
    subprocess.run(
        ["pixlet", "render", "/tmp/rendered.star", "-o", "/tmp/out.webp"])

    # push rendered image to device
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
