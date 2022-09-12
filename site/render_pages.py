import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_file(jinja_env, template_name, output_file_name, output_file_path):
    template = jinja_env.get_template(template_name)
    render = template.render()
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    with open(f"{output_file_path}/{output_file_name}", "w+") as outfile:
        outfile.write(render)


def main():
    this_file_path = Path(__file__).parent.resolve()
    env = Environment(loader=FileSystemLoader(f"{this_file_path}/templates/"),
                      autoescape=select_autoescape())

    render_path = f"{this_file_path}/rendered/"

    files_to_render = [
        {
            "template_name": "base.html",
            "output_file_name": "index.html",
            "output_file_path": render_path
        },
        {
            "template_name": "message.html",
            "output_file_name": "index.html",
            "output_file_path": f"{render_path}/tidbyt"
        },
    ]

    for file in files_to_render:
        render_file(env, **file)


if __name__ == "__main__":
    main()
