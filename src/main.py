from copy_static import copy_directory
from generate_page import generate_pages_recursive


def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
