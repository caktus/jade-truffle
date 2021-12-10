import subprocess
import shutil
from pathlib import Path


def clean_project():
    if "{{cookiecutter.testing_type}}" == "django":
        print("REMOVE: pytest.ini")
        Path(Path().cwd(), "pytest.ini").unlink()

    if "{{cookiecutter.css_style}}" == "sass":
        Path("./tailwind.config.js").unlink()
        Path("./postcss.config.js").unlink()

    if "{{cookiecutter.ci_cd}}" == "actions":
        shutil.rmtree(Path("./.circleci"))
    else:
        shutil.rmtree(Path("./.github"))


def setup_node():
    print("Setting up Node")
    base_deps = [
        "@babel/core",
        "@babel/preset-env",
        "@sentry/webpack-plugin",
        "babel-loader",
        "fs-jetpack",
        "jquery",
        "autoprefixer",
        "gulp",
        "gulp-rename",
        "prettier",
        "webpack",
        "webpack-bundle-tracker",
        "webpack-merge",
        "webpack-cli",
        "webpack-stream"
    ]

    tailwind_deps = [
        "tailwindcss",
        "@tailwindcss/forms",
        "@tailwindcss/typography",
        "postcss",
        "postcss-import",
        "postcss-preset-env",
    ]

    sass_deps = [
        "sass",
        "gulp-sass"
    ]

    if "{{cookiecutter.css_style}}" == "tailwind":
        base_deps += tailwind_deps
    else:
        base_deps += sass_deps

    subprocess.run(['/bin/bash', '-i', '-c', 'nvm use'])

    for dep in base_deps:
        subprocess.run(['npm', 'install', '--silent', dep])


def setup_python():
    print("Setting up Python")
    subprocess.run(['make', 'update_requirements'])


def setup_local_py():
    print("Setting up local.py")
    Path("./{{cookiecutter.project_slug}}/settings/local.example.py")\
        .rename("./{{cookiecutter.project_slug}}/settings/local.py")


def main():
    print("Running post generation tasks.")
    clean_project()
    setup_local_py()
    setup_node()
    setup_python()


if __name__ == "__main__":
    main()
