'''
Operations on saved Compoundwords:
- Delete GOSW for saved compound word (they haven't been defined in fact).
- and update field 'wordinside_oder_NK' for them
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


compoundwords = Words.objects.filter(Q(owner_id=2)&Q(status__gt=0)&\
                                     Q(isCompoundword=True)&Q(isnotword=True))

for cowo in compoundwords:
    wordinside_order = json.loads(cowo.wordinside_order)
    wordinside_order_NK = []
    for wordinside in wordinside_order:
        word = Words.objects.get(id=wordinside)
        wordinside_order_NK.append([word.wordtext, word.language.natural_key()])
    cowo.wordinside_order_NK = json.dumps(wordinside_order_NK)
    # delete GOSW
    GOSW = Grouper_of_same_words.objects.filter(grouper_of_same_words_for_this_word=cowo).first()
    if GOSW:
        GOSW.delete()
    cowo.grouper_of_same_words = None
    cowo.save()

