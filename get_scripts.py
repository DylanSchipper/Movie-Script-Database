import sources
import json
import time
import multiprocessing
import os

DIR = os.path.join("scripts", "temp")

if not os.path.exists(DIR):
    os.makedirs(DIR)

def main():
    with open('sources.json', 'r') as f:
        data = json.load(f)
    
    processes = []
    starttime = time.time()

    for source, included in data.items():
        if included == "true":
            # print("Fetching scripts from %s" % (source))
            # sources.get_scripts(source=source)
            # print()
            p = multiprocessing.Process(target=sources.get_scripts, args=(source,))
            processes.append(p)
            p.start()

    for process in processes:
        process.join()

    print()    
    print('Time taken = {} seconds'.format(time.time() - starttime))

if __name__ == '__main__':
    main()
