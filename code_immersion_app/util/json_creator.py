from bs4 import BeautifulSoup
import json

examples = {}
examples_path = '/home/michael/projects/cppbyexample.com'

levels = ['beginner', 'intermediate', 'advanced']
examples['levels'] = {}

for level in levels:

    # get list of functions at this difficulty
    with open(examples_path + '/tags/' + level + '.html') as f:
        lines = f.readlines()

    lessons = {}
    line_count = 0
    for line in lines:
        line_count = line_count+1
        if line_count < 230:
            continue

        if line_count > 394:
            break

        if line[-5:-1] == '</a>':
            filename = line.split('"')[1]
            lessons[line_count] = filename



    examples['levels'][level] = {}
    for filename in lessons.values():

        with open(examples_path + filename) as example:
            content = example.read()


            soup = BeautifulSoup( content )
            try:
                cleaned_filename = filename.split('.')[0]
                cleaned_filename = cleaned_filename.split('/')[1]
                examples['levels'][level][cleaned_filename] = soup.pre.get_text()
            except:
                if filename == '/what_is_std.html':
                    continue
                raise Exception('pre tag not found')

    '''
    pre_found = False
    num_line = 0
    for line in content:
        num_line = num_line + 1
        
        if not pre_found and line[:5] != '<pre>':
            continue
        else:
            pre_found = True
            lo = num_line

        if line[:6] == '</pre>':
            hi = num_line

            soup = BeautifulSoup( content )
            examples[filename] = soup.get_text()

            break
            '''
with open('lessons.json', 'w') as outfile:
    json.dump(examples, outfile)




