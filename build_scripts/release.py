import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "release"
VERSION = "1.0.0"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = "https://github.com/appcove/developer-software"
DESCRIPTION = "This package install the key inside the client and add files to path"

UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]


if __name__ == '__main__':

    BUILD_FOLDER = f"temp/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    # add path to bins
    Path(f'{BUILD_FOLDER}/etc/profile.d').mkdir(parents=True, exist_ok=True)
    with open(f'{BUILD_FOLDER}/etc/profile.d/10-ads-release.sh', "w") as release_file:
        release_file.write("export PATH=$PATH:/opt/ads/bin")

    # add key and list file and create a new path
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
    with open(f'{BUILD_FOLDER}/DEBIAN/postinst', "w") as release_file:
        release_file.write("""
curl -s --compressed "https://appcove.github.io/developer-software/ubuntu/KEY.gpg" | sudo gpg --dearmor -o /usr/share/keyrings/appcove-developer-software.gpg
sudo curl -s --compressed -o /etc/apt/sources.list.d/appcove-developer-software.list "https://appcove.github.io/developer-software/ubuntu/dists/jammy/appcove-developer-software.list""")

    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(BUILD_FOLDER, f"asd-{PACKAGE}", VERSION, UBUNTU_VERSION,
                       MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION)
    create_deb_package(f"{BUILD_FOLDER}")