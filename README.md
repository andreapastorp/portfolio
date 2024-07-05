# Portfolio
Just a repo for my portfolio.

Jugo was created by [@maarten990](https://github.com/maarten990).

# Jugo; the juiciest portfolio generator.

Jugo generates portfolios!

## Project layout
- `public` is the main folder containing both the templates and the generated HTML
- `public/templates` contains the jinja templates that will be rendered
- `public/templates/projects` contains the jinja templates for each project page; each of them
   should define variables called `title` and `image` to be used to generate the overview on the
   frontpage.
- `public/static` contains the static files (css, images, etc)
- `public/html` contains the generated output, including the static files copied into it. This
   folder is self-contained and can be deployed to a host like Firebase.

## Usage
Basically just run `python jugo.py`; see `python jugo.py --help` for additional options.
Python requirements are specified in `requirements.txt` and can be installed from there
(`pip install -r requirements.txt`).

# License
Source code is licensed under [MIT license](https://opensource.org/license/mit).
Content of the site is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). 
