import random
import os
import linecache
import re

def corpus_text(language, nb_of_lines):
    ''' Use for Testing '''
    ''' generator of a set of (nb_of_lines) sentences in the language chosen,
    from a random text (inside 'lwt/corpus/(language))'''

    nb_of_lines -= 1 # because the first line is not counted in our loop
    # choose a file:
    corpus_loc = os.path.join('lwt','corpus', language)
    all_texts = os.listdir(corpus_loc)
    title = random.choice(all_texts)
    fullpath_text = os.path.join('lwt','corpus',language,title)

    # choose a position in the text:
    with open(fullpath_text, encoding='utf8') as f:
        # get the numbr of lines:
        lines_total = sum(1 for line in f)
    lines = []
    
    temp_nb_of_lines = nb_of_lines

    while True:
        random_pos = random.randrange(lines_total)
        line = linecache.getline(fullpath_text, random_pos) 
        if re.search(r'.*[^\W\d_].*', line): # first line must contain at least one letter
            lines.append(line) # get the first line
            i = 1
            while nb_of_lines != 0 and (random_pos + (temp_nb_of_lines - nb_of_lines) + i) < lines_total:
                # loop until we get our number of lines desired or reach the end of file
                line = linecache.getline(fullpath_text, random_pos + (temp_nb_of_lines - nb_of_lines) + i)
                if line.strip() != '':
                    lines.append(line)
                    nb_of_lines -= 1
                else:
                    i += 1
            text = ''.join(lines)
            break
    return title, text


if __name__ == '__main__':
    print(corpus_text('English', 4))
    