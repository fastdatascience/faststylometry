with open("src/faststylometry/__init__.py", "r", encoding="utf-8") as f:
    text = f.read()

import re

init_py_lines = text.split("\n")
for idx, line in list(enumerate(init_py_lines)):
    if "__version__" in line:
        old_version = re.sub(r'.+= "|"', "", line)
        version_bits = old_version.split(".")
        old_version_regex = r"\.".join(version_bits)
        version_bits[-1] = str(int(version_bits[-1]) + 1)
        new_version = ".".join(version_bits)
        init_py_lines[idx] = re.sub(old_version, new_version, line)

        print("Old version", old_version)
        print("New version", new_version)

with open("CITATION.cff", "r", encoding="utf-8") as f:
    text = f.read()

citation_lines = text.split("\n")
for idx, line in list(enumerate(citation_lines)):
    if line.startswith("version:"):
        citation_lines[idx] = re.sub(old_version_regex, new_version, line)

with open("pyproject.toml", "r", encoding="utf-8") as f:
    text = f.read()

pyproject_lines = text.split("\n")
for idx, line in list(enumerate(pyproject_lines)):
    if line.startswith("version"):
        pyproject_lines[idx] = re.sub(old_version_regex, new_version, line)

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

readme_lines = text.split("\n")
for idx, line in list(enumerate(readme_lines)):
    if "Version " in line:
        readme_lines[idx] = re.sub("Version " + old_version_regex, "Version " + new_version, line)

with open("src/faststylometry/__init__.py", "w", encoding="utf-8") as f:
    f.write("\n".join(init_py_lines))

with open("CITATION.cff", "w", encoding="utf-8") as f:
    f.write("\n".join(citation_lines))

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(readme_lines))

with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write("\n".join(pyproject_lines))

import os
os.system(f'git add src/faststylometry/__init__.py CITATION.cff README.md pyproject.toml && git commit -m "Update version to {new_version}"')
