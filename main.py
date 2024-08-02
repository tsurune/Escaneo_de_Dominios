import requests
import argparse
from urllib.parse import urljoin


def read_dictionary(url):
    """Reads the dictionary from the given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text.splitlines()


def scan_directories(domain, dictionary):
    """Scans the domain for directories listed in the dictionary."""
    found_directories = []
    for directory in dictionary:
        url = urljoin(domain, directory)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Found: {url}")
                found_directories.append(url)
            else:
                print(f"Not found: {url} (Status code: {response.status_code})")
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
    return found_directories


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory scanner for a given domain.")
    parser.add_argument("domain", help="The domain to scan (e.g., https://example.com)")
    args = parser.parse_args()

    dictionary_url = "https://raw.githubusercontent.com/hackingyseguridad/diccionarios/master/diccionario.txt"

    print(f"Reading dictionary from {dictionary_url}")
    dictionary = read_dictionary(dictionary_url)

    print(f"Scanning directories on {args.domain}")
    found_directories = scan_directories(args.domain, dictionary)

    print("Scan complete.")
    print(f"Found directories: {found_directories}")
