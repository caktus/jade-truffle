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
        Path("./{{cookiecutter.project_app}}/assets/styles/tailwind_entry.css").unlink()
        shutil.rmtree(Path("./apps/{{cookiecutter.primary_app}}/assets/styles/tailwind"))
    else:
        Path("./{{cookiecutter.project_app}}/assets/styles/sass_entry.scss").unlink()
        shutil.rmtree(Path("./apps/{{cookiecutter.primary_app}}/assets/styles/sass"))

    if "{{cookiecutter.ci_cd}}" == "actions":
        shutil.rmtree(Path("./.circleci"))
    else:
        shutil.rmtree(Path("./.github"))

    if "{{cookiecutter.project_type}}" == "django":
        shutil.rmtree((Path("./apps/search")))


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
        "@tailwindcss/typography",
        "postcss",
        "cssnano",
        "gulp-postcss",
        "postcss-cli",
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

    subprocess.run(['/bin/bash', '-i', '-c', 'export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use'])
    subprocess.run(['/bin/bash', '-i', '-c', 'nvm', 'install-latest-npm'])

    for dep in base_deps:
        subprocess.run(['npm', 'install', '--silent', dep])


def setup_python():
    print("Setting up Python")
    subprocess.run(['make', 'update_requirements'])


def setup_local_py():
    print("Setting up local.py")
    Path("./{{cookiecutter.project_app}}/settings/local.example.py")\
        .rename("./{{cookiecutter.project_app}}/settings/local.py")


def main():
    print("Running post generation tasks.")
    clean_project()
    setup_local_py()
    setup_node()
    setup_python()


if __name__ == "__main__":
    main()
