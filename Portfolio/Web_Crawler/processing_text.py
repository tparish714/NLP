# Tera Parish       txp200011
# Bridgette Bryant  bmb180001

import os
import string
import re


def process_text(repo):
    count = 0
    for filename in os.listdir(repo):
        with open(os.path.join(repo, filename), 'r') as f:
            count += 1
            # remove new line
            raw = f.read().replace('\n', ' ')
            # remove multiple spaces
            raw = re.sub("\s\s+", " ", raw)
            raw = raw.replace('&nbsp;', ' ')
            # create a new file to write to for each file read in
            path= repo + '_out'
            if not os.path.exists(path):
                os.makedirs(path)
            # output file name
            out = repo + str(count) + '.txt'
            with open(os.path.join(path, out), 'w', encoding='utf-8') as file:
                # write to file
                file.write(raw)
                # close the file
                file.close()


if __name__ == '__main__':
    # clean up text files
    process_text('dem_urls')
    process_text('rep_urls')
    process_text('int_urls')