import sources
import json
import time
import multiprocessing
import os
import logging
from urllib.error import HTTPError

# Configure logging
logging.basicConfig(filename="script_fetcher.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DIR = os.path.join("scripts", "temp")

if not os.path.exists(DIR):
    os.makedirs(DIR)

def fetch_script_with_error_handling(source):
    try:
        # Attempt to fetch the script
        sources.get_scripts(source)
    except HTTPError as e:
        if e.code == 404:
            logging.error(f"HTTP 404: Script not found at {source}")
        else:
            logging.error(f"HTTP Error {e.code}: {source}")
    except Exception as e:
        logging.error(f"An error occurred while fetching {source}: {e}")

def main():
    with open('sources.json', 'r') as f:
        data = json.load(f)
    
    processes = []
    starttime = time.time()

    for source, included in data.items():
        if included == "true":
            # Instead of directly calling sources.get_scripts, call the new fetch function
            p = multiprocessing.Process(target=fetch_script_with_error_handling, args=(source,))
            processes.append(p)
            p.start()

    for process in processes:
        process.join()

    print()    
    print('Time taken = {} seconds'.format(time.time() - starttime))

if __name__ == '__main__':
    main()