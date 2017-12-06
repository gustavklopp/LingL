# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Lwtgeneral(models.Model):
    lwtkey = models.CharField(db_column='LWTKey', primary_key=True, max_length=40)  # Field name made lowercase.
    lwtvalue = models.CharField(db_column='LWTValue', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = '_lwtgeneral'


class Archivedtexts(models.Model):
    atid = models.AutoField(db_column='AtID', primary_key=True)  # Field name made lowercase.
    atlgid = models.IntegerField(db_column='AtLgID')  # Field name made lowercase.
    attitle = models.CharField(db_column='AtTitle', max_length=200)  # Field name made lowercase.
    attext = models.TextField(db_column='AtText')  # Field name made lowercase.
    atannotatedtext = models.TextField(db_column='AtAnnotatedText')  # Field name made lowercase.
    ataudiouri = models.CharField(db_column='AtAudioURI', max_length=200, blank=True, null=True)  # Field name made lowercase.
    atsourceuri = models.CharField(db_column='AtSourceURI', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'archivedtexts'


class Archtexttags(models.Model):
    agatid = models.IntegerField(db_column='AgAtID', primary_key=True)  # Field name made lowercase.
    agt2id = models.IntegerField(db_column='AgT2ID')  # Field name made lowercase.

    class Meta:
        db_table = 'archtexttags'
        unique_together = (('agatid', 'agt2id'),)


class Languages(models.Model):
    lgid = models.AutoField(db_column='LgID', primary_key=True)  # Field name made lowercase.
    lgname = models.CharField(db_column='LgName', unique=True, max_length=40)  # Field name made lowercase.
    lgdict1uri = models.CharField(db_column='LgDict1URI', max_length=200)  # Field name made lowercase.
    lgdict2uri = models.CharField(db_column='LgDict2URI', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lggoogletranslateuri = models.CharField(db_column='LgGoogleTranslateURI', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lgexporttemplate = models.CharField(db_column='LgExportTemplate', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    lgtextsize = models.IntegerField(db_column='LgTextSize')  # Field name made lowercase.
    lgcharactersubstitutions = models.CharField(db_column='LgCharacterSubstitutions', max_length=500)  # Field name made lowercase.
    lgregexpsplitsentences = models.CharField(db_column='LgRegexpSplitSentences', max_length=500)  # Field name made lowercase.
    lgexceptionssplitsentences = models.CharField(db_column='LgExceptionsSplitSentences', max_length=500)  # Field name made lowercase.
    lgregexpwordcharacters = models.CharField(db_column='LgRegexpWordCharacters', max_length=500)  # Field name made lowercase.
    lgremovespaces = models.IntegerField(db_column='LgRemoveSpaces')  # Field name made lowercase.
    lgspliteachchar = models.IntegerField(db_column='LgSplitEachChar')  # Field name made lowercase.
    lgrighttoleft = models.IntegerField(db_column='LgRightToLeft')  # Field name made lowercase.

    class Meta:
        db_table = 'languages'


class Sentences(models.Model):
    seid = models.AutoField(db_column='SeID', primary_key=True)  # Field name made lowercase.
    selgid = models.IntegerField(db_column='SeLgID')  # Field name made lowercase.
    setxid = models.IntegerField(db_column='SeTxID')  # Field name made lowercase.
    seorder = models.IntegerField(db_column='SeOrder')  # Field name made lowercase.
    setext = models.TextField(db_column='SeText', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'sentences'


class Settings(models.Model):
    """ different custom settings are stored like that: setting Key : setting value
        Warning with stvalue! It's a CharField. Don't forget to do int(stvalue) if you put int inside (like 'currentlanguage' """
    stkey = models.CharField(db_column='StKey', primary_key=True, max_length=40)  # Field name made lowercase.
    stvalue = models.CharField(db_column='StValue', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'settings'


class Tags(models.Model):
    tgid = models.AutoField(db_column='TgID', primary_key=True)  # Field name made lowercase.
    tgtext = models.CharField(db_column='TgText', unique=True, max_length=20)  # Field name made lowercase.
    tgcomment = models.CharField(db_column='TgComment', max_length=200)  # Field name made lowercase.

    class Meta:
        db_table = 'tags'


class Tags2(models.Model):
    t2id = models.AutoField(db_column='T2ID', primary_key=True)  # Field name made lowercase.
    t2text = models.CharField(db_column='T2Text', unique=True, max_length=20)  # Field name made lowercase.
    t2comment = models.CharField(db_column='T2Comment', max_length=200)  # Field name made lowercase.

    class Meta:
        db_table = 'tags2'


class Textitems(models.Model):
    tiid = models.AutoField(db_column='TiID', primary_key=True)  # Field name made lowercase.
    tilgid = models.IntegerField(db_column='TiLgID')  # Field name made lowercase.
    titxid = models.IntegerField(db_column='TiTxID')  # Field name made lowercase.
    tiseid = models.IntegerField(db_column='TiSeID')  # Field name made lowercase.
    tiorder = models.IntegerField(db_column='TiOrder')  # Field name made lowercase.
    tiwordcount = models.IntegerField(db_column='TiWordCount')  # Field name made lowercase.
    titext = models.CharField(db_column='TiText', max_length=250)  # Field name made lowercase.
    titextlc = models.CharField(db_column='TiTextLC', max_length=250)  # Field name made lowercase.
    tiisnotword = models.IntegerField(db_column='TiIsNotWord')  # Field name made lowercase.

    class Meta:
        db_table = 'textitems'


class Texts(models.Model):
    txid = models.AutoField(db_column='TxID', primary_key=True)  # Field name made lowercase.
    txlgid = models.IntegerField(db_column='TxLgID')  # Field name made lowercase.
    txtitle = models.CharField(db_column='TxTitle', max_length=200)  # Field name made lowercase.
    txtext = models.TextField(db_column='TxText')  # Field name made lowercase.
    txannotatedtext = models.TextField(db_column='TxAnnotatedText')  # Field name made lowercase.
    txaudiouri = models.CharField(db_column='TxAudioURI', max_length=200, blank=True, null=True)  # Field name made lowercase.
    txsourceuri = models.CharField(db_column='TxSourceURI', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'texts'


class Texttags(models.Model):
    tttxid = models.IntegerField(db_column='TtTxID', primary_key=True)  # Field name made lowercase.
    ttt2id = models.IntegerField(db_column='TtT2ID')  # Field name made lowercase.

    class Meta:
        db_table = 'texttags'
        unique_together = (('tttxid', 'ttt2id'),)


class Words(models.Model):
    ''' wostatus  1 =>  "Learning",
                 2 =>  "Learning",
                 3 => "Learning",
                 4 => "Learning",
                 5 => "Learned",
                99 => "Well Known",
                98 => "Ignored", 
    '''
    woid = models.AutoField(db_column='WoID', primary_key=True)  # Field name made lowercase.
    wolgid = models.IntegerField(db_column='WoLgID')  # Field name made lowercase.
    wotext = models.CharField(db_column='WoText', max_length=250)  # Field name made lowercase.
    wotextlc = models.CharField(db_column='WoTextLC', max_length=250)  # Field name made lowercase.
    wostatus = models.IntegerField(db_column='WoStatus')  # Field name made lowercase.
    wotranslation = models.CharField(db_column='WoTranslation', max_length=500)  # Field name made lowercase.
    woromanization = models.CharField(db_column='WoRomanization', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wosentence = models.CharField(db_column='WoSentence', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    wocreated = models.DateTimeField(db_column='WoCreated')  # Field name made lowercase.
    wostatuschanged = models.DateTimeField(db_column='WoStatusChanged')  # Field name made lowercase.
    wotodayscore = models.FloatField(db_column='WoTodayScore')  # Field name made lowercase.
    wotomorrowscore = models.FloatField(db_column='WoTomorrowScore')  # Field name made lowercase.
    worandom = models.FloatField(db_column='WoRandom')  # Field name made lowercase.

    class Meta:
        db_table = 'words'
        unique_together = (('wolgid', 'wotextlc'),)


class Wordtags(models.Model):
    wtwoid = models.IntegerField(db_column='WtWoID', primary_key=True)  # Field name made lowercase.
    wttgid = models.IntegerField(db_column='WtTgID')  # Field name made lowercase.

    class Meta:
        db_table = 'wordtags'
        unique_together = (('wtwoid', 'wttgid'),)
