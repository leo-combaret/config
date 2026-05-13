# REPL
## Getting started
Zed's built-in REPL uses Jupyter kernels so you can run code interactively in regular editor files.
## Installation
Zed supports running code in multiple languages. To get started, you need to install a kernel for the language you want to use.
Currently supported languages:
- Python (ipykernel)
- TypeScript (Deno)
- R (Ark)
- R (Xeus)
- Julia
- Scala (Almond)
Once installed, you can start using the REPL in the respective language files, or other places those languages are supported, such as Markdown. If you recently added the kernels, run the repl: refresh kernelspecs command to make them available in the editor.
## Using the REPL
To start the REPL, open a file with the language you want to use and use the repl: run command (defaults to ctrl-shift-enter on macOS) to run a block, selection, or line. You can also click on the REPL icon in the toolbar.
The repl: run command will be executed on your selection(s), and the result will be displayed below the selection.
Outputs can be cleared with the repl: clear outputs command, or from the REPL menu in the toolbar.
### Cell mode
Zed supports notebooks as scripts using the # %% cell separator in Python and // %% in TypeScript. This allows you to write code in a single file and run it as if it were a notebook, cell by cell.
The repl: run command will run each block of code between the # %% markers as a separate cell.
```
# %% Cell 1
import time
import numpy as np

# %% Cell 2
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
```
## Language specific instructions
### Python
#### Global environment
On macOS, your system Python will not work. Either set up pyenv or use a virtual environment.
To setup your current Python to have an available kernel, run:
```
pip install ipykernel
python -m ipykernel install --user
```
#### Conda Environment
```
source activate myenv
conda install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```
#### Virtualenv with pip
```
source activate myenv
pip install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```
### R (Ark Kernel)
Install Ark by downloading the release for your operating system. For example, for macOS just unpack ark binary and put it into /usr/local/bin . Then run:
```
ark --install
```
### R (Xeus Kernel)
- Install Xeus-R
- Install the R Extension for Zed (search for R in Zed Extensions)
### TypeScript: Deno
- Install Deno and then install the Deno jupyter kernel:
```
deno jupyter --install
```
### Julia
- Download and install Julia from the official website .
- Install the Julia Extension for Zed (search for Julia in Zed Extensions)
### Scala
- Install Scala with cs setup (Coursier): brew install coursier/formulas/coursier && cs setup
- REPL (Almond) setup instructions : brew install --cask temurin (Eclipse foundation official OpenJDK binaries) brew install coursier/formulas/coursier && cs setup coursier launch --use-bootstrap almond -- --install
## Changing which kernel is used per language
Zed automatically detects available kernels and organizes them in the kernel picker:
- Recommended : The Python environment matching your active toolchain (if detected)
- Python Environments : Virtual environments (venv, virtualenv, Poetry, Pipenv, Conda, uv, etc.)
- Jupyter Kernels : Installed Jupyter kernelspecs
- Remote Servers : Connected remote Jupyter servers
### Installing ipykernel
Python environments appear in the picker even if ipykernel is not installed. Environments missing ipykernel are dimmed and labeled "ipykernel not installed." When you select one, Zed automatically runs pip install ipykernel in that environment and activates it once installation completes.
### How Zed Recommends Kernels
When you run code, Zed selects a kernel automatically:
1. Active toolchain match : If a Python environment matches your active toolchain and has ipykernel, Zed uses it
2. First available Python env : Otherwise, the first Python environment with ipykernel
3. Language-based fallback : If no Python envs are ready, Zed picks a Jupyter kernel matching the code block's language
You can override this by explicitly selecting a kernel from the picker.
### Setting Default Kernels
To configure a different default kernel for a language, you can assign a kernel for any supported language in your settings.json :
```
{
  "jupyter": {
    "kernel_selections": {
      "python": "conda-env",
      "typescript": "deno",
      "javascript": "deno",
      "r": "ark"
    }
  }
}
```
## Interactive Input
When code execution requires user input (such as Python's input() function), the REPL displays an input prompt below the cell output.
Type your response in the text field and press Enter to submit. The kernel receives your input and continues execution.
For password inputs, characters appear masked with asterisks for security.
If execution is interrupted while an input prompt is active, the prompt automatically clears when the kernel returns to idle state.
## Debugging Kernelspecs
Available kernels are shown via the repl: sessions command. To refresh the kernels you can run, use the repl: refresh kernelspecs command.
If you have jupyter installed, you can run jupyter kernelspec list to see the available kernels.
```
$ jupyter kernelspec list
Available kernels:
  ark                   /Users/z/Library/Jupyter/kernels/ark
  conda-base            /Users/z/Library/Jupyter/kernels/conda-base
  deno                  /Users/z/Library/Jupyter/kernels/deno
  python-chatlab-dev    /Users/z/Library/Jupyter/kernels/python-chatlab-dev
  python3               /Users/z/Library/Jupyter/kernels/python3
  ruby                  /Users/z/Library/Jupyter/kernels/ruby
  rust                  /Users/z/Library/Jupyter/kernels/rust
```
> Note: Zed makes best effort usage of
> sys.prefix
> and
> CONDA_PREFIX
> to find kernels in Python environments. If you want explicitly control run
> python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
> to install the kernel directly while in the environment.