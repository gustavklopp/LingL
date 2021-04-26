""" Helper functions. Guided by the 'utilities.inc.php' file in lwt
    a collection of helper functions. """
from django.contrib import messages
from django.db import transaction
from django.utils.translation import ugettext as _
# second party
import re #it's standard in python
import json  #it's standard in python
import urllib #it's standard in python
# local
from lwt.models import *


def processSessParam(reqkey, sesskey, default, isnum, request):
    """ Fetch the key in the GET/POST method (reqkey), else in the COOKIE (sesskey), else get the default:
    for ex.: to display the right page number (for ex. in edit_textget_textssort_selectoptions):
    $currentpage = processSessParam("page","currenttextpage",'1',1); """
    result = ''
    if request.GET[reqkey] or request.POST[reqkey]:
        # the GET/POST var has been set:
        reqdata = request.GET[reqkey] if request.GET[reqkey] else request.POST[reqkey]
        request.session[sesskey] = reqdata  # put the result into COOKIE
        result = reqdata  # and return also the result

    elif request.session[sesskey]:
        result = request.session[sesskey]

    else:
        result = default

    result = int(result) if isnum else result


def validateLang(currentlang):
    """ Does the language with this ID 'currentlang' exists in db? """
    if currentlang != '':
        if not Languages.objects.get(id=int(currentlang)):
            currentlang = ''
    return currentlang


def validateTextTag(currenttag, currentlang):
    """ Is the tag is used in the texts? Return '' if not """
    if currenttag != '' and currenttag != -1:
        if currentlang != '' and currentlang != -1:
            t = Texts.objects.filter(txlg__id=currentlang).values_list(
                'texttags', flat=True).distinct()
        else:
            # get the list of the distict tags used in the texts
            t = Texts.objects.values_list('texttags', flat=True).distinct()
        r = Texttags.objects.filter(id__in=t).count()
        currenttag = '' if r == 0 else currenttag
    return currenttag

def splitCheckText(text,noinsert=0):
    ''' Used to split the text into sentences.
        noinsert = -1     => Check, return protocol
        noinsert = -2     => Only return sentence list
        else:
                        => Split: insert sentences/textitems entries in DB '''

    r = ''
    removeSpaces = text.txlg.lgremovespaces # Used for Chinese,Jap where the white spaces are not used.
    splitEachChar = text.txlg.lgspliteachchar
    splitSentence = text.txlg.lgregexpsplitsentences
    noSentenceEnd = text.txlg.lgexceptionssplitsentences
    termchar = text.txlg.lgregexpwordcharacters
    replace = text.txlg.lgcharactersubstitutions.split("|") # some weird apostrophes are listed, triple dots etc.
    rtlScript = text.txlg.lgrighttoleft
    ######## PRE-PROCESSING ##############################################################################
    t = text.txtext.strip()
    if splitEachChar: # do we make each character a word? (used in Chinese,Jap)
        t = re.sub(r'([^\s])', r'\1 ', t) # 'this is a text.'=> ''t h i t  i t  a  t e x t . '

    t = re.sub(r'\s{2,}', r' ', t) # 'big  space.little space.' => 'big space.little space.'
    if noinsert == -1:
        r += '<div style="margin-right:50px;"><h4>Text</h4><p '
        r += 'dir="rtl"' if rtlScript else ''
        r += '>' + t + '</p>'

    t = t.replace('{', '[')  # because of sent. spc. char. Is it useful??
    t = t.replace('}', ']')                              # is it useful??
    for value in replace: # Using lgcharactersubstitutions: change weird apostrophes, triple dots etc
        fromto = value.strip().split("=")
        if len(fromto) >= 2:
            t = t.replace(fromto[0].strip(), fromto[1].strip())
        t = t.strip()

    if noSentenceEnd != '': # 'M.John' must not be cut into 2 sentences. replace it with an 'hyphenation point'
        t = re.sub(r'(' + noSentenceEnd + ')\s', r'\1‧', t)
        t = re.sub(r'([' + splitSentence + '¶])\s', r"\1\n", t) # end of paragraph are replaced by \n
        t = re.sub(r" ¶\n", r"\n¶\n", t)
        t = re.sub(r'‧', r' ', t) # but if there't already the 'hyphenation point', change it by space.
    ############ ACTUAL PROCESSING ############################################################################
    if t == '': # No text, so...
        textLines = [t]
    else:
        t = t.split("\n") # line return are used to split (ln were place at the position of splitsentence the step before)
        l = len(t)

        for i in range(l):  #  loop over each sentences in the text
            t[i] = t[i].strip()
            if t[i] != '':
                pos = splitSentence.find(t[i]) # identify the splitter used in the sentence (? or ! or . or ;)
                while pos != -1: # Not sure what it't doing? Removing weird sentences with only one dot inside??
                    t[i-1] += " " + t[i]
                    for j in range(i + 1, l):
                        t[j-1] = t[j]
                    t.pop()
                    l = len(t)
                    pos = splitSentence.find(t[i])

        textLines = [line.strip() for line in t if line.strip()] 

        ###############################
        # Only return sentence list
        if noinsert == -2:
            return textLines

        sentWords = {}
        ################################
        # Check, return protocol
        if noinsert == -1: # TODO: the split text which return only stats.
            wordList = {}
            wordSeps = []
            r += "<h4>Sentences</h4><ol>"
            for sentID,sentTxt in enumerate(textLines):
                r += "<li "
                r += 'dir="rtl"' if rtlScript else ''
                r += ">" + sentTxt + "</li>"
                sentWords[sentID] = re.split(r'([^'+termchar+']{1,})', sentTxt)
                l = len(sentWords[sentID])
                for i in sentWords[sentID]:
                    word = word.lower()
                    if word != '':
                        if i % 2 == 0:
                            if word in wordList:
                                wordList[word ][0] += 1
                                wordList[word ][1].append(sentID)
                            else:
                                wordList[word ] = [1, [sentID]]
                        else:
                            ww = remove_spaces(word , removeSpaces)
                            if ww in wordSeps:
                                wordSeps[ww] += 1
                            else:
                                wordSeps[ww] = 1

            r += "</ol><h4>Word List <span class=\"red2\">(red = already saved)</span></h4><ul>"
            wordList.sort()
            anz = 0
            for key, value in wordList.items():
                trans = Words.objects.filter(wolg__id=text.txlg.lid).values_list(
                    'wotranslation', flat=True).get(wotextlc=key)
                if not isset(trans):
                    trans = ""
                if trans == "*":
                    trans = ""
                if trans != "":
                    r += "<li "
                    r += 'dir="rtl"' if rtlScript else ''
                    r += "><span class=\"red2\">[" + key + "] — " + \
                        value[0] + " - " + repl_tab_nl(trans) + "</span></li>"
                else:
                    r += "<li "
                    r += 'dir="rtl"' if rtlScript else ''
                    r += ">[" + key + "] — " + value[0] + "</li>"
                anz += 1

            r += "</ul><p>TOTAL: " + anz + "</p><h4>Non-Word List</h4><ul>"
            if '' in wordSeps:
                del wordSeps['']
            wordSeps.sort()
            anz = 0
            for key, value in wordSeps:
                r += "<li>[" + key.replace(" ", "<span class=\"backgray\">&nbsp;</span>") + \
                    "] — " + value + "</li>"
                anz += 1

            r += "</ul><p>TOTAL: " + anz + "</p></div>"
            return r
    ################################################
    # Split: insert sentences/textitems entries in DB
    for sentID,sentTxt in enumerate(textLines): # Loop on each sentence
        with transaction.atomic(): # allow bulk transaction
            newsentence = Sentences.objects.create(selg=text.txlg,setx=text,seorder=sentID+1,setext=sentTxt) # create each sentence
            sentList = re.split(r'([^'+termchar+']+)', sentTxt) # ['This',' ','is',' ','good','.',' ']
            sentList = [i for i in sentList if i] # remove the empty item created by re.split
            lastitem = sentList.pop() # Special case: it's the delimiter: th e'.' at the end of the sentence for ex.
            for wordidx,word in enumerate(sentList): # creating textitsm (i.e fragment of sentence with 9 words inside)
                tiwordcount = 0
                textitemList = [] # => ['this','this is','this is good']
                if word != ' ': # ex: ['this',' ','good'] don't create textitem beginning with ' '
                    if tiwordcount == 9: # the textitem max length is 9 of wordcount
                        continue
                    for idx in range(wordidx,len(sentList)):
                        titext = ''.join(sentList[wordidx:idx+1]) # 'this',' ','is' => 'this is'
                        if titext[-1] != ' ': # don't insert in db 'this ' or 'this is ' but 'this' and 'this is'
                            textitemList.append(titext)
                            tiwordcount += 1
                            # Create the textitem. tiorder is 1-based, not 0-based
                            Textitems.objects.create(tilg=text.txlg, tise=newsentence,titx=text,tiorder=(wordidx+1), \
                                            tiwordcount=tiwordcount, titext=remove_spaces(titext,removeSpaces), \
                                            titextlc=remove_spaces(titext.lower(),removeSpaces), tiisnotword=False)
                else: # what't the need to insert that in db?? 'this',' ','is' => the ' ' is inserted into db.
                    tiwordcount += 1
                    Textitems.objects.create(tilg=text.txlg, tise=newsentence,titx=text,tiorder=(wordidx+1), \
                                    tiwordcount=tiwordcount, titext=' ', titextlc=' ', tiisnotword=True)
            # Special case: it's the delimiter: th e'.' at the end of the sentence for ex.
            Textitems.objects.create(tilg=text.txlg, tise=newsentence,titx=text,tiorder=(wordidx+2), \
                            tiwordcount=tiwordcount, titext=lastitem, titextlc=lastitem, tiisnotword=True)
            

def remove_spaces(s,remove):
    ''' some cleaning for the splitting in textitems function '''
    if remove:
        return re.sub(r'\s{1,}', r'', s)  
    else:
        return s

def repl_tab_nl(s):
    ''' some other cleaning for the splitting in textitems function '''
    s = re.sub(r'[\r\n\t]', r' ', s)
    s = re.sub(r'\r\n', r' ', s)
    s = re.sub(r'\s', r' ', s)
    s = re.sub(r'\s{2,}', r' ', s)
    return s.strip()

def isset(variable):
    ''' original php function converted in python ''' 
    return variable in locals() or variable in globals()

def annotation_to_json(ann):
    ''' Converts the field in text, txannotatedtx to json format
    to be readable inside the javascript part in text_read '''
    if ann == '':
        return "{}"
    arr = {}
    items = re.split(r'[\n]', ann)
    for item in items:
        vals = re.split(r'[\t]', item)
        if len(vals) > 3 and vals[0] >= 0 and vals[2] > 0:
            arr[vals[0]-1] = [vals[1],vals[2],vals[3]]
    return json.dump(arr)

def makeStatusClassFilter(status):
    ''' don't know what it's doing...'''
    if status == '':
        return ''
    ls = [1,2,3,4,5,98,99]
    if status == 599:
        makeStatusClassFilterHelper(5,ls)
        makeStatusClassFilterHelper(99,ls)
    elif status < 6 or status > 97:
        makeStatusClassFilterHelper(status,ls)
    else:
        start = int(status) / 10
        end = status - start*10
        for i in range(start,end):
            makeStatusClassFilterHelper(i,ls)
    r = ''
    for v in ls:
        if v != -1:
            r += ':not(.status'+v+')'
    return r


def makeStatusClassFilterHelper(status,ls):
    ''' don't know what it's doing...'''
    try:
        pos = ls.index(status)
        ls[pos] = -1
    except ValueError: # not found
        pass

def strToClassName(mystring):
    ''' escapes everything to "Â¤xx" but not 0-9, a-z, A-Z, and unicode >= (hex 00A5, dec 165) '''
    ''' What's the need of this???...'''
    l = len(mystring)
    r = ''
    for i in range(l):
        c = mystring[i:i+1]
        o = ord(c)
        if o < 48 or (o > 57 and o < 65) or (o > 90 and o < 97) or (o > 122 and o < 165):
            r += 'Â¤'+strToHex(c)
        else: 
            r += c
    return r

def strToHex(mystring):
    ''' What's the need of this???...'''
    myhex=''
    for c in mystring:
        h = hex(ord(c))
        if len(h) == 1: 
            myhex += "0"+h
        else:
            myhex += h
    return myhex.upper()

def get_statuses():
    ''' CONSTANTS (I know, it's not me...) used inside text_read when displaying the tooltip '''
    statuses = { 1 : {"abbr" :   "1", "name" : _("Learning")},
                 2 : {"abbr" :   "2", "name" : _("Learning")},
                 3 : {"abbr" :   "3", "name" : _("Learning")},
                 4 : {"abbr" :   "4", "name" : _("Learning")},
                 5 : {"abbr" :   "5", "name" : _("Learned")},
                99 : {"abbr" : "WKn", "name" : _("Well Known")},
                98 : {"abbr" : "Ign", "name" : _("Ignored")}, }
    return statuses

def createTheDictLink(u,t): 
    ''' 
    - called by view dictwebpage to create the dict link in text_read bottomright 
    - called by pgm.js:  make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder)
    createTheDictLink(wblink1,txt,'Dict1','Lookup Term: ') + =>http://127.0.0.1/trans.php?x=2&i=http%3A//www.wordreference.com/enfr/%23%23%23&t=This  
    createTheDictLink(wblink2,txt,'Dict2','') +
    createTheDictLink(wblink3,txt,'GTr','') + ...'''
    # Case 1: url without any ###: append UTF-8-term
    # Case 2: url with 1 ###: substitute UTF-8-term
    # Case 3: url with 2 ###enc###: substitute enc-encoded-term
    url = u.strip()
    trm = t.strip()
    pos = url.upper().find('###')
    if pos > 0: # ### found
        pos2 = url.upper().rfind('###')
        if (pos2-pos-3) > 1:   # 2 ### found
            enc = url[(pos+3):pos2].strip()
            r = url[:pos]
            r += urllib.parse.quote_plus(trm.decode(enc).encode('UTF-8'))
            if (pos2+3) < len(url):
                r += url[(pos2+3):]
        elif pos == pos2: # 1 ### found
            replac = '+' if trm == '' else urllib.parse.quote_plus(trm)
            r = url.replace("###", replac)
    else:  # no ### found
        r = urllib.parse.quote_plus(trm)
    return r


# def texttodocount2(text):
#     ''' Update the number of word to do and Display the "I KNOW ALL" button (if it's still useful) '''
#     c = textwordcount(text) - textworkcount(text)
#     if c > 0: 
#         return '<span title="To Do" class="status0">&nbsp;' + str(c)+'&nbsp;</span>&nbsp;&nbsp;&nbsp;<input type="button" onclick="iknowall(' +text+');" value=" I KNOW ALL " />'
#     else
#         return '<span title="To Do" class="status0">&nbsp;' + str(c)+'&nbsp;</span>'
# }
