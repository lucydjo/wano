# Wano Editor

Wano is a web-based text editor inspired by Nano.

## Overview
Wano provides a convenient way to edit text files using a web interface, similar to the popular Nano text editor.

## Requirements
- Python 3.x
- pyngrok
- uuid
- Flask

## Installation
You can install Wano using pip. First, clone the repository:

```bash
git clone https://github.com/lucydjo/wano
cd wano
```

Then, install the package using `pip`:

```bash
pip install .
```

This will install the necessary dependencies and make `wano` command available in your environment.

## Ngrok Configuration
Wano uses Ngrok to expose the local web server to the internet. Before using Wano, set your Ngrok authentication token as an environment variable:

```bash
export NGROK_WANO_KEY=your_ngrok_auth_token
```

You can obtain your Ngrok authentication token from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).

## Usage
To edit a text file with Wano, use the following command:

```bash
wano anyfile.txt
```

This will start the Wano server, open the specified file (`anyfile.txt` in this example) in the web-based editor, and expose it using Ngrok for external access.

After running the `wano` command, you can access the editor by navigating to the provided Ngrok URL in your web browser.

---
