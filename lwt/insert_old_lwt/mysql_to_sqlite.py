#!/usr/bin/env python


# Convert a mysql dump into a sqlite-compatible format.
# I wrote this for just one script... no guarantees that it will work with others...

import re
import sys

def mysql_to_sqlite(content):


    ############### Change in syntax: ##################################
    print("..Change in syntax ..")
    # int(...) by integer:
    COMMAND_RE = re.compile(r'int\(\d+\)', re.I | re.M | re.S)

    content = COMMAND_RE.sub('integer', content)

    # AUTO_INCREMENT by AUTOINCREMENT:
    COMMAND_RE = re.compile(r'AUTO_INCREMENT', re.I | re.M | re.S)

    content = COMMAND_RE.sub('', content)


    ############# unused commands ########################################
    print("..replacing unused commands/statements ..")

    # KEY ... is not used in Sqlite3:
    # UNIQUE KEY neither
    # ENGINE=MyISAM ... DEFAULT CHARSET=UTF8 neither
    # CHARACTER SET utf8 COLLATE utf8_bin neither


    # COMMAND_RE = re.compile(r'(^(SET|LOCK|UNLOCK).*?;$)|((,\s*?)?^\s*?(KEY).*?$)|(COLLATE utf8_unicode_ci)', re.I | re.M | re.S)
    COMMAND_RE = re.compile(r''' ,\s+KEY.*?[`\)]\)
                               | ,\s+UNIQUE\sKEY.*?[`\)]\)
                               | ENGINE.*?utf8
                               | CHARACTER.*?bin
                               ''', re.M | re.S | re.X )

    content = COMMAND_RE.sub('', content)


    # COMMAND_RE = re.compile(r'^(SET).*?;\n$', re.I | re.M | re.S)
    """
    COMMAND_RE = re.compile(r"\\'", re.I | re.M | re.S) # "\'" => "''"
    content = COMMAND_RE.sub("''", content)
    """
    content = content.replace( r"\'", "''" )
 
    COMMAND_RE = re.compile(r"COMMENT\s+.*?(,?)$", re.M | re.S) # "\'" => "''"
    content = COMMAND_RE.sub(r"\1", content)
 
    # table constraints
    # TCONS_RE = re.compile(r'\)(\s*(CHARSET|DEFAULT|ENGINE)(=.*?)?\s*)+;', re.M | re.S)
    # content = TCONS_RE.sub(');', content)
 
 
    ######################## insert multiple values ##########################
    print("..editing multiple value replacement ..")
    # the most tricky / dangerous part (may fail; simple "state machine" parser will be the way to go)
    INSERTVALS_RE = re.compile(r'^(INSERT INTO.*?VALUES)\s*\((.*?)\);$', re.M | re.S)
    INSERTVALS_SPLIT_RE = re.compile(r'\)\s*,\s*\(', re.I | re.M | re.S)
 
    def insertvals_replacer(match):
        insert, values = match.groups()
        replacement = []
        for vals in INSERTVALS_SPLIT_RE.split(values):
            replacement.append( '%s (%s);' % (insert, vals) )
        return '\n'.join( replacement )
 
    content = INSERTVALS_RE.sub(insertvals_replacer, content)
 
    print("..writing output ..")

    return content

if __name__ == '__main__':
#     content = '''
#    CREATE TABLE `words` (  
#     `WoID` int(11) unsigned NOT NULL AUTO_INCREMENT,  
#      `WoLgID` int(11) unsigned NOT NULL, 
#      KEY `WoTranslation` (`WoTranslation`(333)), 
#      KEY `WoCreated` (`WoCreated`),  
#      KEY `WoRandom` (`WoRandom`) ) 
#      ENGINE=MyISAM AUTO_INCREMENT=592 DEFAULT CHARSET=utf8;
# '''  
#     print(mysql_to_sqlite(content))
    with open('lwt-backup-2017-10-06-08-45-34.sql',encoding="utf8") as fin:
        content = fin.read()
        content = mysql_to_sqlite(content)
        with open('converted_sqlite3_python.sql', 'w',encoding="utf8") as fout:
            fout.write(content)


