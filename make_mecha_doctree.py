import os

# modules to ignore in the api doc
ignore_modules = [
    "aeon.dj_pipeline",
    "aeon.qc.video",
]


def make_mecha_doctree():
    """
    Create a doctree of all modules in aeon_mecha/aeon.
    """
    doctree = ""
    api_path = os.path.join(".", "aeon_mecha", "aeon")
    for root, dirs, files in os.walk(api_path):
        # remove leading "./"
        root = root[2:]
        for file in sorted(files):
            if file.endswith(".py") and not file.startswith("_"):
                # convert file path to module name
                full = os.path.join(root, file)
                full = full[:-3].replace(os.sep, ".")
                full = (".").join(full.split(".")[1:])
                ignore = False
                for ignore_module in ignore_modules:
                    if full.startswith(ignore_module):
                        ignore = True
                        break
                if not ignore:
                    doctree += f"    {full}\n"

    # get the api doc header
    with open("src/_templates/api_mecha_head.rst", "r") as f:
        api_head = f.read()

    # write file for api doc with header + doctree
    output_dir = "./src/reference/api"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "mecha.rst"), "w") as f:
        f.write("..\n  This file is auto-generated.\n\n")
        f.write(api_head)
        f.write(doctree)


if __name__ == "__main__":
    make_mecha_doctree()
