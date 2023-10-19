# Lautaro Daniel Villarreal Culic'
# https://lautarovculic.com


# require: pip install requests
# require: pip install argparse
# require: pip install time
# require: pip install concurrent.features
# require: pip install alive-progress
# require: pip install colorama

import requests
import argparse
import concurrent.futures
import time
from colorama import init, Fore
from alive_progress import alive_bar

print("#################################")
print(f"####### {Fore.RED}Lautaro V. Culic'{Fore.RESET} #######")
print(f"############# {Fore.RED}zDirb{Fore.RESET} #############")
print(f"### {Fore.RED}https://lautarovculic.com{Fore.RESET} ###")
print("#################################")

def enumerate_directory(url, extension, bar):
    url_with_extension = url + extension
    response = requests.get(url_with_extension)
    if response.status_code != 404:
        print(f"HTTP Status {Fore.GREEN}{response.status_code}{Fore.RESET} - {Fore.LIGHTGREEN_EX}{url_with_extension}{Fore.RESET}")
    bar()

def add_protocol(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

def get_valid_url(prompt):
    while True:
        url = input(prompt).strip()
        if not url:
            print(f"{Fore.RED}URL cannot be empty{Fore.RESET}. Please provide a valid URL.")
        else:
            return add_protocol(url)

def get_wordlist():
    while True:
        wordlist_file = input(f"{Fore.RED}Enter the path to the wordlist file: {Fore.RESET}")
        try:
            with open(wordlist_file, "r", encoding="ISO-8859-1") as file:
                wordlist = file.readlines()
                if not wordlist:
                    print(f"{Fore.RED}Wordlist file is empty{Fore.RESET}. Please provide a valid wordlist.")
                else:
                    return wordlist
        except FileNotFoundError:
            print(f"File not found: {Fore.RED}{wordlist_file}{Fore.RESET}. Please provide a valid wordlist file.")

def enumerate_directories(url, history, wordlist, extension):
    total_words = len(wordlist)
    print(f"Total words in the wordlist: {Fore.RED}{total_words}{Fore.RESET}")

    while True:
        print(f"Enumerating directories for: {Fore.RED}{url}{Fore.RESET}")

        start_time = time.time()

        with alive_bar(total_words, title="Enumerating directories", bar="classic", spinner="classic") as bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(enumerate_directory, f"{url}/{line.strip()}", extension, bar): line for line in wordlist}
                concurrent.futures.wait(futures)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Enumeration completed in {Fore.RED}{elapsed_time:.2f} seconds.{Fore.RESET}")
        print(f"Total words enumerated:{Fore.RED}{total_words}{Fore.RESET}")
        exit()

def enumerate_subdomains(url, history, wordlist):
    total_words = len(wordlist)
    print(f"Total subdomains in the wordlist: {Fore.RED}{total_words}{Fore.RESET}")

    start_time = time.time()

    with alive_bar(total_words, title="Enumerating subdomains", bar="classic", spinner="classic") as bar:
        for line in wordlist:
            subdomain = line.strip()
            if subdomain and len(subdomain) <= 63: 
                subdomain_url = f"http://{subdomain}.{url.split('//')[-1]}"
                try:
                    response = requests.get(subdomain_url)
                    if response.status_code != 404:
                        print(f"Subdomain {Fore.GREEN}found{Fore.RESET} - {Fore.LIGHTGREEN_EX}{subdomain_url}{Fore.RESET}")
                except requests.exceptions.RequestException:
                    pass
            bar()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Enumeration completed in {Fore.RED}{elapsed_time:.2f} seconds.{Fore.RESET}")
    print(f"Total words enumerated: {Fore.RED}{total_words}{Fore.RESET}")
    exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to start enumeration (Example: -u https://lautarovculic.com)")
    parser.add_argument("-w", "--wordlist", help="Wordlist file path (Example: -w common.txt)")
    parser.add_argument("-e", "--extension", default="", help="Extension to add to the URLs (Example: -e .php)")
    parser.add_argument("-s", "--subdomains", action="store_true", help="Enumerate subdomains (Example: -s)")
    args = parser.parse_args()

    if args.url:
        start_url = add_protocol(args.url)
    else:
        start_url = get_valid_url(f"{Fore.RED}Enter the URL to start enumeration:{Fore.RESET} ")

    if args.wordlist:
        try:
            with open(args.wordlist, "r", encoding="ISO-8859-1") as wordlist_file:
                wordlist = wordlist_file.readlines()
                if not wordlist:
                    print(f"Wordlist file is {Fore.RED}empty{Fore.RESET}. Please provide a valid wordlist.")
                    wordlist = get_wordlist()
        except FileNotFoundError:
            print(f"File {Fore.RED}not found{Fore.RESET}: {args.wordlist}. Please provide a valid wordlist file.")
            wordlist = get_wordlist()
    else:
        wordlist = get_wordlist()

    history = []

    if args.subdomains:
        enumerate_subdomains(start_url, history, wordlist)
    else:
        enumerate_directories(start_url, history, wordlist, args.extension)
