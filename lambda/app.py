import base64
import json
import os
import subprocess
import urllib.parse
from json.decoder import JSONDecodeError
from pprint import pprint


def build_pixlet_sender(tidbyt_device_id, tidbyt_api_token):

    def pixlet_send(image_filename):
        push_subprocess = subprocess.run([
            "pixlet", "push", tidbyt_device_id, image_filename, "-t",
            tidbyt_api_token
        ])
        response = {"status": "failed"}
        if push_subprocess.returncode == 0:
            response["status"] = "success"

        return response

    return pixlet_send


def load_message_template():
    with open("text.star", "r") as infile:
        template_file = infile.readlines()

    return template_file


def send_specific_image(image_label):
    fixed_images_dict = {"nyan_cat": "nyan_cat.webp"}
    image_to_push = fixed_images_dict.get(image_label, "nyan_cat.webp")

    tidbyt_device_id = os.environ.get("TIDBYT_DEVICE_ID")
    tidbyt_api_token = os.environ.get("TIDBYT_API_TOKEN")
    push_subprocess = subprocess.run([
        "pixlet", "push", tidbyt_device_id, image_to_push, "-t",
        tidbyt_api_token
    ])

    response = {"status": "failed"}
    if push_subprocess.returncode == 0:
        response["status"] = "success"

    return response


def send_message(message_content):
    # default values to prevent failed executions
    default_replace_dict = {
        "MESSAGE_TEXT": "template message",
        "HEX_COLOR": "ad97ef",
        "SCROLL_SPEED": "100",
        "FONT": "6x13"
    }

    # resolve given values with defaults, preferring given values
    replacements_dict = {**default_replace_dict, **message_content}

    # replace variables in template
    output_file = ''.join(load_message_template()).format(**replacements_dict)

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


def handle_actions(body_content):
    if "image" in body_content:
        return send_specific_image(body_content.get("image"))
    if "message" in body_content:
        return send_message(body_content.get("message"))


def handler(event, context):
    # log the Lambda event and context
    print("Event:")
    pprint(event)
    print("Context:")
    pprint(context)

    # shortuct for testing so we don't go through the whole rendering process
    if "test" in event:
        return "hello world"

    if event.get("isBase64Encoded", False):
        decoded = base64.b64decode(event.get("body", ""))
        return handle_actions(decoded)
    else:
        return handle_actions(event.get("body", {}))
