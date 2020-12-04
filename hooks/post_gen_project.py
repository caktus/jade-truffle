from pathlib import Path


def check_testing_type():
    if "{{cookiecutter.testing_type}}" == "django":
        print("REMOVE: pytest.ini")
        Path(Path().cwd(), "pytest.ini").unlink()


def main():
    print("Cleaning up project.")
    check_testing_type()


if __name__ == "__main__":
    main()
