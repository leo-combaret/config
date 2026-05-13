# Installation
The easiest way to install Zellij is through a package for your OS .
If one is not available for your OS, you can download a prebuilt binary or even try Zellij without installing .
If you have Cargo installed, you can download the latest release using cargo binstall .
Otherwise, you can compile and install it with Cargo .
## Rust - Cargo
For instructions on how to install Cargo see here .
Once installed run:
```
cargo install --locked zellij
```
If experiencing errors, if installed through rustup, please try running:
```
rustup update
```
## Cargo - binstall
For smaller machines like laptops, you might want to just install the binary instead of compiling everything.
The easiest way if cargo is present, is to install with the binstall cargo extension :
```
cargo binstall zellij
```
## Binary Download
Pre-built binaries are available each release for Linux, macOS, and Windows on the release page .
### Linux / macOS
Once downloaded, untar the file:
```
tar -xvf zellij*.tar.gz
```
check for the execution bit:
```
chmod +x zellij
```
and then execute Zellij:
```
./zellij
```
Include the directory Zellij is in, in your PATH Variable if you wish to be able to execute it anywhere.
'Or'
move Zellij to a directory already included in your [$PATH] Variable.
### Windows
Download the Windows binary from the release page , extract it, and run zellij.exe from a terminal (e.g., PowerShell or Windows Terminal).
## Compiling Zellij From Source
Instructions on how to compile Zellij from source can be found here .
## Third party repositories
Zellij is packaged in some third part repositories. Please keep in mind that they are not directly affiliated with zellij maintainers:
More information about third party installation can be found here .