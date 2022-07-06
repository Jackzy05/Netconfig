# Netconfig
Netconfig is a collection of tools for my CLI to configure my network fast and simple. Some examples of its usage are on the picture below.

## Usage
- `netconfig block eth_addr`
- `netconfig unblock eth_addr`
- `netconfig list`
- `netconfig help`

  block         Blocks internet traffic to specified MAC address.
  unblock       Unblocks internet traffic to specified MAC address.
  list          Displays current network entries in verbose mode.  All invalid
                entries and entries on the loop-back interface will be shown.
  help     	Displays the help section.
  eth_addr      Specifies a physical address.

Example:
  -> netconfig block 1C:15:1F:0C:40:27    .... Blocks internet traffic.
  -> netconfig unblock 1C:15:1F:0C:40:27  .... Unblocks internet traffic.
  -> netconfig list                       .... Displays network entries.
  -> netconfig help                       .... Displays the help section.

<img src="netconfig.png">

## Installation
If you'd like to setup netconfig for your local machine you can follow these steps:

1. Install [Python](https://www.python.org/downloads/) including the `pip` package manager. Make sure to check the "Add to PATH" checkbox as well.
2. Install all needed modules -> `pip install bs4`, `pip install requests` and others if needed.
3. Add the python extension (.PY) to the [PATHTEXT](https://www.msftnext.com/what-is-the-pathext-environment-variable-in-windows-10/) in the system environment variables
4. Add the `config.json` file to [path](https://www.maketecheasier.com/what-is-the-windows-path/).
5. Get your default gateway IP from the CLI using the `ipconfig` command. Paste that IP into your browser and explore API endpoints using [devtools](https://developer.chrome.com/docs/extensions/reference/devtools_network/).
6. Change the default gateway as well as the endpoints located in `netconfig.py`.
