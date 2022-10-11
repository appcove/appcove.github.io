from functools import cache
import requests
import json
import re
from pathlib import Path
import subprocess
import ubuntu_folder
from common import install_rust
import yaml
import shutil
import glob

# def get_latest_version_and_deb_file(git_repo_url: str):

#     package_creator_and_name = re.search(
#         "https://github.com/([^\n]+)", git_repo_url)
#     package_creator_and_name = package_creator_and_name.group(1)

#     package_latest_asset = f"https://api.github.com/repos/{package_creator_and_name}/releases/latest"

#     package_name = re.search(
#         "https://api.github.com/repos/.*/([^\n]+)/releases/latest", package_latest_asset)

#     package_name = package_name.group(1)
#     latest_version_info = requests.get(package_latest_asset).json()

#     ubuntu_deb_assets = [asset["browser_download_url"]
#                          for asset in latest_version_info["assets"] if re.match(f"{package_name}_.*_amd64.deb",  asset["name"])]

#     print("xxx")
#     if len(ubuntu_deb_assets):
#         package_version = re.search(
#             "https://github.com/.*/.*/releases/download/v([^\n]+)/.*", ubuntu_deb_assets[0])

#         package_version = package_version.group(1)
#         print("io sono")
#         return (package_name, ubuntu_deb_assets[0])
#     else:
#         raise RuntimeError(
#             f'could not get asset download link from {git_repo_url} ')


if __name__ == "__main__":

    install_rust()

    with open("included_tools.json", "r") as config_file:
        config_json = json.load(config_file)
        # precompiled_tools_urls = config_json["precompiled_tools"]
        to_compile_tools = config_json["to_be_compiled_tools"]

    Path(f'temp').mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["git", "checkout", "remotes/origin/website", "--", "cache.yaml"])
    try:
        with open(r'cache.yaml') as cache_file:
            cached_submodules_hashes = yaml.full_load(cache_file)
            print(cached_submodules_hashes)
    except FileNotFoundError:
        cached_submodules_hashes = {}

    # run custom scripts
    for tool_name in to_compile_tools:
        current_submodule_hash = subprocess.run(
            ["git", "submodule", "status", f"sources/{tool_name}"], capture_output=True).stdout
        try:
            current_submodule_hash = str(
                current_submodule_hash.decode("utf-8")).split()[0]
        except IndexError:
            current_submodule_hash = ""

        if cached_submodules_hashes.get(tool_name) == current_submodule_hash and current_submodule_hash != "":
            print(f"{tool_name} from cache")
            cache_build_deb = subprocess.run(
                f"git checkout remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 -- $(git ls-tree --name-only -r remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 | egrep -e '^.*{tool_name}.*.deb$')", shell=True, capture_output=True).stdout
            cache_build_deb = str(cache_build_deb)
            for deb_file in glob.glob(r'*.deb'):
                shutil.move(deb_file, "temp")
        else:
            subprocess.check_output(
                ["python3", f"build_scripts/{tool_name}.py"])
            cached_submodules_hashes[tool_name] = str(current_submodule_hash)

    with open(r'cache.yaml', 'w+', encoding='utf8') as cache_file:
        yaml.dump(cached_submodules_hashes, cache_file)

    ubuntu_folder.init_ubuntu_folder()

    # idea for future
    # download precompiled tools' debs
    # for tool_url in precompiled_tools_urls:
    #     (package_name, deb_download_url) = get_latest_version_and_deb_file(tool_url)
    #     print((package_name, deb_download_url))
    #     response = requests.get(deb_download_url)
    #     open(f"temp/{package_name}.deb", "wb+").write(response.content)


# https://raw.githubusercontent.com/appcove/developer-software/website/cache.yaml
# https://raw.githubusercontent.com/appcove/developer-software/website/ubuntu/dists/jammy/main/binary-amd64/
