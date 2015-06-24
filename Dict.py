__author__ = 'leo'

import sys
import re
import linecache
import os
import time
import urllib2
from getpass import getuser
from unicurses import *


user_name = getuser()
cur_dir = os.getcwd()
file_counter = 0
os.chdir('/home/%s/'%user_name)

class GetWords:
    def arg_1(self, file_name):
        try:
            ff = open(file_name, 'r')
        except TypeError:
            print 'File not found.'
            sys.exit(1)
        except IOError:
            print 'File not found.'
            sys.exit(1)
        result = [line for line in ff.readlines()]

        return result


    def clear_nl(self, name):
        file_name = self.arg_1(name)
        result = [string.replace('\n', '') for string in file_name]

        return result


    def clear_blank(self, name):
        file_name = self.clear_nl(name)
        result = [string for string in file_name if not len(string) == 0]

        return result


    def make_lower(self, name):
        file_name = self.clear_blank(name)
        result = [string.lower() for string in file_name]

        return result


    def write(self, name):
        file_name = self.make_lower(name)
        result = []

        for i in range(len(file_name)):
            result.append(file_name[i].replace(' ', '\n'))

        return result


    def regex(self, name):
        file_name = self.write(name)
        result = []

        for word in file_name:
            word1 = " ".join(re.findall("[a-zA-Z]+", word))
            result.append(word1)

        return result


    def split(self, name):
        file_name = self.regex(name)
        result = []

        for string in file_name:
            ff = string.split()
            result.append(ff)

        return result


    def match_the_same(self, name):
        file_name = self.split(name)
        result = []

        print file_name.sort()
        for word in file_name:
            for checker in file_name:
                if word != checker:
                    result.append(word)
                else:
                    continue
        return result


    def get_items(self, name):
        ff = self.split(name)
        result = []

        for line in ff:
            for items in xrange(len(line)):
                result.append(line[items])

        return result

class TermInterface:

    def interface(self):
        runner = True

        while runner is True:
            set_dir = cur_dir + '/Dict'
            os.chdir(set_dir)
            dict_file_name = 'all'
            stdscr = initscr()
            init_pair(1, COLOR_RED, COLOR_BLUE)
            box(stdscr)
            max_y, max_x = getmaxyx(stdscr)

            window_1 = newwin(3, max_x - 2 / 2 - 10, 1, 1)
            wmove(window_1, 1, 1)
            wattron(window_1, color_pair(1))
            waddstr(window_1, 'Dict v0.3 by Fydor Dostoyevski.', attr=A_REVERSE)

            window_2 = newwin(3, 25, max_y-4, 2)
            wmove(window_2, 0, 0)
            waddstr(window_2, '<ESC> for quit.\n', attr=A_REVERSE)

            window_3 = newwin(max_y-10, max_x-4, 4, 2)
            wmove(window_3, 0, 0)

            window_4 = newwin(2, max_x / 2 - 10, max_y - 3, max_x / 2 + 2)
            wmove(window_4, 0, 0)
            waddstr(window_4, 'Get Word: ', attr=A_REVERSE)
            dict_file_name = str(wgetstr(window_4))

            try:
                waddstr(window_3, str(open(cur_dir + '/Dict/%s.dict'%dict_file_name).read()), attr=A_BOLD)
            except IOError:
                pass

            panel = new_panel(window_1)
            panel_2 = new_panel(window_2)
            panel_3 = new_panel(window_3)
            panel_4 = new_panel(window_4)
            waddstr(window_2, '<RETURN> for repeat', attr=A_REVERSE)
            top_panel(panel)
            bottom_panel(panel_2)
            update_panels()
            doupdate()

            key = wgetch(window_4)
            refresh()

            if key == 27:
                endwin()
                runner = False

class Formatting():

    def specify_first_line(self, uf_file, word):
        try:
            uf_file = open(uf_file)
        except TypeError:
            print 'File Error.'
            sys.exit(1)
        counter_start = 0

        for line in uf_file.readlines():
            counter_start += 1
            starting = line.count("Meanings of \"%s\" in Turkish :" % word)
            starting2 = line.count("Meanings of \"%s\" with other terms :" % word)

            if starting == 1 or starting2 == 1:
                starting_line = counter_start

                return starting_line


    def specify_second_line(self, uf_file, word):
        try:
            uf_file = open('%s' % uf_file)
        except TypeError:
            print 'File Error.'
            sys.exit(1)

        return len(uf_file.readlines()) - 1


    def get_lines_between(self, uf_file, new_file_name):
        word = new_file_name
        new_file = open('%s.dict' % new_file_name, 'w')

        global file_counter

        file_counter += 1
        starting_line = self.specify_first_line(uf_file, word)
        ending_line = self.specify_second_line(uf_file, word)

        for line in xrange(starting_line, ending_line):
            new_file.writelines(linecache.getline(uf_file, line))

        return True


class OtherTools:

    def check_not_found(self, uf_file):
        uf = open('%s.uf' % uf_file)
        checking_word = 'Did you mean that?'
        check_list = [line.count(checking_word) for line in uf.readlines()]

        for checker in check_list:
            if checker == 1:
                return True


    def check_connectivity(self, reference):
        try:
            urllib2.urlopen(reference, timeout=2)
            return True
        except urllib2.URLError:
            return False


    def dynamic_prompt(self, line):
        sys.stdout.write("\r\x1b[K" + line.__str__())
        sys.stdout.flush()



def main():
    print('Welcome to HackWords (v0.1) by Fydor Dostoyevski.')
    file_name = raw_input("What's the target file's name: ")

    if os.path.exists('/usr/bin/w3m') is False:
        print 'please install w3m terminal web browser.'
        sys.exit(1)

    if os.path.exists('Dict/') is False:
        try:
            os.mkdir('Dict/')
        except OSError:
            print 'OSError.'
            sys.exit(1)

    if OtherTools().check_connectivity('http://tureng.com') is False:
        print 'No connection. Be sure about internet access.'
        sys.exit(1)
    words = GetWords().get_items(file_name)
    os.chdir('Dict/')
    word_counter = 0

    for word in words:
        word_counter += 1

        if os.path.exists("%s.dict" % word) is True:
            continue

        lenght = len(words)
        percent = float(word_counter) * 100 / float(lenght)
        OtherTools().dynamic_prompt('<%s> dowloading and formatting. %.1f%% is completed.' % (word, percent))
        os.system("wget -q tureng.com/search/%s -O %s.html" % (word, word))
        os.system("w3m -dump %s.html > %s.uf" % (word, word))
        os.system("rm %s.html" % word)

        if OtherTools().check_not_found(word) is True:
            os.system('rm %s.uf' % word)
            continue
        try:
            Formatting().get_lines_between('%s.uf' % word, word)
        except TypeError:
            continue
        os.system("rm %s.uf" % word)
    os.system('find -empty -type f -delete')
    print
    print 'done. [processed %i word, wrote %i new files.]' % (len(words), file_counter)
    time.sleep(2)

if len(sys.argv) <= 1:
    print 'Type [-hw] for hacking words from a txt file in same directory.'
    print "Type [-vw] for a tiny interface for viewing  hacked word's meaning. [Do not use before [-hw] option."
    print "Also, you can use [-hw] [-vw] to together."
    sys.exit(-1)

elif len(sys.argv) > 3:
    print 'too much arguments.'

elif sys.argv[1] == '-hw' and len(sys.argv) <= 2:
    main()

elif sys.argv[1] == '-vw' and len(sys.argv) <= 2:
    TermInterface().interface()

elif sys.argv[1] == '-hw' and sys.argv[2] == '-vw':
    main()
    TermInterface().interface()
else:
    print 'Type [-hw] for hacking words from a txt file in same directory.'
    print "Type [-vw] for a tiny interface for viewing  hacked word's meaning. [Do not use before [-hw] option."
    print "Also, you can use [-hw] [-vw] to together."
    sys.exit(-1)
