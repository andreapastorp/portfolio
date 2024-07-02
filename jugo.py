"""
Jugo; the juiciest portfolio generator.
"""

import argparse
from dataclasses import dataclass
from functools import partial
import http.server
from pathlib import Path
import shutil
import socketserver

from jinja2 import FileSystemLoader, Environment

MAIN_PAGES = ["index.html", "about.html"]


@dataclass
class Project:
    """
    Representation of a single project, including it's path on disk and the image/title to be used
    on the main page.
    """

    path: Path
    image_path: str
    title: str


def get_projects(jinja_env: Environment, template_folder: Path) -> list[Project]:
    """
    Return a list of projects to be linked on the main page.

    Args:
        jinja_env: A jinja environment set to the same folder as `template_folder`
        template_folder: The base folder containing all templates

    Returns:
        A list of `Project` objects containing the project path and additional metadata.
    """
    projects = []

    for file in (template_folder / "projects").glob("*.html"):
        template_path = file.relative_to(template_folder)
        template = jinja_env.get_template(str(template_path))

        if not hasattr(template.module, "title"):
            raise ValueError(f"{template_path} does not have a title defined")
        if not hasattr(template.module, "image"):
            raise ValueError(f"{template_path} does not have an image defined")

        projects.append(
            Project(
                path=template_path,
                image_path=template.module.image,
                title=template.module.title,
            )
        )

    return projects


def ensure_projects_folders_exist(output_folder, projects: list[Project]) -> None:
    """
    Ensure that the required folder structure exists for each project.
    """
    for project in projects:
        (output_folder / project.path.parent).mkdir(parents=True, exist_ok=True)


def render_file(jinja_env: Environment, write_path: Path, template_path: Path, **kwargs) -> None:
    """
    Render a single template at `template_path` to `write_path`.
    Remaining keyword arguments are passed to jinja as variables.
    """
    with write_path.open("w") as f:
        f.write(jinja_env.get_template(str(template_path)).render(**kwargs))


def render_portfolio(jinja_env: Environment, output_folder: Path, projects: list[Project]) -> None:
    """
    Render the portfolio into `output_folder` using a given jinja environment and list of projects.
    """
    ensure_projects_folders_exist(output_folder, projects)
    for project in projects:
        render_file(jinja_env, output_folder / project.path, project.path)

    for page in MAIN_PAGES:
        render_file(jinja_env, output_folder / page, Path(page), projects=projects)


def copy_static_files(folder: Path, output_folder: Path, static_folder: str = "static") -> None:
    """
    Copy the folder with static files into the generated html folder.
    """
    shutil.copytree(folder / static_folder, output_folder / static_folder, dirs_exist_ok=True)


def generate(folder: Path) -> None:
    """
    Generate the project under `folder`.
    """
    template_folder = folder / "templates"
    output_folder = folder / "html"
    env = Environment(loader=FileSystemLoader(template_folder))

    projects = get_projects(env, template_folder)
    render_portfolio(env, output_folder, projects)
    copy_static_files(folder, output_folder)


def serve(folder: Path, port: int) -> None:
    """
    Spin up an http server to locally host the website.
    """
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=folder / "html")
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"http://localhost:{port}")
        httpd.serve_forever()


def main() -> None:
    """
    Main entrypoint.
    """
    parser = argparse.ArgumentParser(prog="Jugo", description=__doc__)
    parser.add_argument("--folder", "-f", help="The public folder", default="public")
    parser.add_argument(
        "--port", "-p", help="Port to use if --serve is passed", type=int, default=8000
    )
    parser.add_argument(
        "--serve", help="Spin up a simple webserver after generating", action="store_true"
    )
    args = parser.parse_args()

    folder = Path(args.folder)
    generate(folder)
    if args.serve:
        serve(folder, args.port)


if __name__ == "__main__":
    main()
