# zDirb

A Python script for enumerating directories and counting words in files with progress tracking.

## Table of Contents

- [Description](#description)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Customization](#customization)


## Description

This Python script allows you to enumerate directories based on a provided URL and count the words in files located in those directories using a wordlist. It includes progress tracking with an interactive progress bar.

## Prerequisites

- Python 3.x
- Required libraries:
    - `requests`
    - `alive-progress`

You can install the required libraries using `pip`. For example:

```bash
pip install requests
pip install alive-progress
```

## Usage

1 - Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/directory-enumeration-tool.git
```
2 - Navigate to the project directory:
```bash
cd directory-enumeration-tool
```
3 - Run the script with the following command:
```bash
python3 directory_enumerator.py -u <start_url> -w <wordlist_file>
```
If you don't provide the -u or -w arguments, the script will prompt you to enter the URL and wordlist file paths.

The script will automatically add "http://" or "https://" to the URL if missing.

## Customization

You can customize the script as needed. For example, you can modify the code to change the number of concurrent threads or customize the progress bar appearance.
### NOTE
If you increase the number of threads, it may skip directories or it may be enumerated multiple times. A range of 5 to 15 is recommended.
