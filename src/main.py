import os
import shutil

from markdown import markdown_to_html_node


def main():
    proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(proj_dir, "static")
    public_dir = os.path.join(proj_dir, "public")
    print("Copying static files...")
    copy_directory(static_dir, public_dir)
    print("Static files copied.")
    generate_pages_recursive(
        os.path.join(proj_dir, "content"),
        os.path.join(proj_dir, "template.html"),
        os.path.join(public_dir),
    )


def copy_directory(src_dir: str, dest_dir: str):
    if not os.path.exists(src_dir):
        raise ValueError(f"Path not found: {src_dir}")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    children = os.listdir(src_dir)
    for child in children:
        src_child = os.path.join(src_dir, child)
        dest_child = os.path.join(dest_dir, child)
        if os.path.isfile(src_child):
            print(f"{src_child} -> {dest_child}")
            shutil.copy(src_child, dest_child)
        else:
            copy_directory(src_child, dest_child)


def extract_title(markdown):
    title_lines = list(filter(lambda line: line.startswith("# "),
                              markdown.split("\n")))
    if len(title_lines) == 0:
        raise ValueError("No level one heading found in {}".format(markdown))
    if len(title_lines) > 1:
        raise ValueError(
            "More than one level one heading found in {}".format(markdown))
    return title_lines[0].lstrip("# ")


def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    children = os.listdir(content_dir_path)
    for child in children:
        content_child = os.path.join(content_dir_path, child)
        dest_child = os.path.join(dest_dir_path, child)
        if os.path.isfile(content_child) and content_child.endswith(".md"):
            generate_page(content_child,
                          template_path,
                          dest_child.replace(".md", ".html"))
        else:
            generate_pages_recursive(content_child, template_path, dest_child)


def generate_page(from_path, template_path, dest_path):
    print("Generating page from {} to {} using {}".format(
        from_path, dest_path, template_path))
    markdown_file = open(from_path)
    template_file = open(template_path)
    markdown = markdown_file.read()
    template = template_file.read()
    content = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    to_write = template.replace("{{ Title }}", title)
    to_write = to_write.replace("{{ Content }}", content.to_html())
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(to_write)
    dest_file.close()
    markdown_file.close()
    template_file.close()


if __name__ == "__main__":
    main()
