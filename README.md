![Build status](https://img.shields.io/github/workflow/status/appcove/developer-software/Build%20the%20sources/master?style=for-the-badge)
![Licence](https://img.shields.io/github/license/appcove/developer-software?style=for-the-badge)
# Appcove Developer Software
This custom Debian PPA is used by AppCove to build and share all the in-house built power tools
--

## Installation

Install needed programs
``` bash
sudo apt install -y curl gpg
```

Download of the key and `source.list`
``` bash
curl -sLO https://appcove.github.io/developer-software/ubuntu/dists/jammy/main/binary-amd64/ads-release_1.0.0custom22.04_amd64.deb
sudo dpkg -i ads-release_1.0.0custom22.04_amd64.deb
sudo apt update
```
❗**Log out and log back in for systemwide changes to be applied**, then try to install one of our tools: `sudo apt install git-excess`


Install everything: 
```
sudo apt install ads-git-excess ads-fd ads-pastel ads-bat
```
### List of available Packages after installation

``` bash
sudo apt list "ads-*"
```
Should output
- ads-release - This package installs the needed files for the PPA to work correctly
- [ads-git-excess](https://github.com/appcove/git-excess)
- [ads-pastel](https://github.com/sharkdp/pastel)
- [ads-fd](https://github.com/sharkdp/fd)
- [ads-bat](https://github.com/sharkdp/bat)
- [ads-procs](https://github.com/dalance/procs) - Replacement for `ps` written in Rust.
- [ads-grex](https://github.com/pemistahl/grex) - An intuitive regex generator meant to create expression based on user's input
- [ads-broot](https://github.com/Canop/broot) - Navigate directories and list content in a tree, with a lot of additional features
- [ads-exa](https://github.com/ogham/exa) - Modern replacement for the venerable file-listing command-line program ls
- [ads-sd](https://github.com/chmln/sd) - An intuitive find & replace CLI.
