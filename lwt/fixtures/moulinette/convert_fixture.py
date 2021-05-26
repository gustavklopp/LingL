'''
with data from LWT: saved words can be duplicate (i.e they have same wordtext but have
a different Grouper_of_same_word: Fix this.
Also, compound words need to have their wordtext has: 'firstelement+secondelement'
'''
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), 'LingL'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LingL.settings")
import django
from django.conf import settings
django.setup()

from django.db.models import Q
from django.db.models.functions import Lower
import json
from lwt.models import Words, Grouper_of_same_words
import re


savedwords = Words.objects.filter(Q(owner_id=2)&Q(status__gt=0)).\
                annotate(wordtext_lc=Lower('wordtext')).order_by('language','wordtext_lc')
wordtext = ''
gosw = None
word = None
word_naturalkey = ''
for wo in savedwords:
    # it's a new distinct word
    if wo.wordtext_lc != wordtext: 
        word = wo
        wordtext = wo.wordtext_lc
        gosw = wo.grouper_of_same_words
        if wo.isnotword: # it's a compound word
            wtx = wo.wordtext
            match = re.search(r'\{.+\}', wtx)
            if match:
                wtx = match.group()
                wtx = wtx[1:-1]
                wtx_split = wtx.split(' ')
                if len(wtx_split) == 1:
                    wtx_split = wtx.split('\'')
                    if len(wtx_split) == 1:
                        wtx_split = list(wtx)
                wtx = '+'.join(wtx_split)
                wo.wordtext = wtx
                word_alternative_naturalkey = [wtx, wo.language.natural_key()]
        else:
            word_alternative_naturalkey = [wo.wordtext, wo.language.natural_key()]
        wo.grouper_of_same_words.id_string = json.dumps(word_alternative_naturalkey)
        wo.grouper_of_same_words.save()

    # word has already been seen before
    else: 
        wo.grouper_of_same_words = gosw
#         Grouper_of_same_words.objects.get(id=wo.id).delete()
    wo.save()
        



        
    
