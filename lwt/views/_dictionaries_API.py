""" Helper functions. Guided by the 'utilities.inc.php' file in lwt
    a collection of helper functions. """
from django.utils.translation import ugettext as _
from django.templatetags.static import static # to use the 'static' tag as in the templates
# second party
import re
import html # use to scrap the dictionary
# third party
from bs4 import BeautifulSoup #use to scrap
from urllib import parse # set the encoding for the URL
from urllib.parse import urljoin, urlparse
# local

''' helper function: when saving a webpage, we clean it:'
    remove all the scripts, convert the relative links to absolute
    and get only finally the <body>, <link> and <style>
    @url    the url of the original webpage
    @soup   the Beautifulsoup
    @return the html string
'''
def _clean_soup_Webpage(soup, url):
    for scr in soup.select('script'):
        scr.extract()
    
    # We'll keep only <link>, <style> and <body>
    links = soup.findAll('link')
    link_str = ''
    parsed_uri = urlparse(url)
    url_maindomain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    for link in links:
        absolute_url = urljoin(url_maindomain, link['href'])
        link['href'] = absolute_url
        str_link = str(link)
        link_str += str_link
    lingl_style = '<link rel="stylesheet" type="text/css" href="'+static('lwt/css/styles.css')+'">'
    styles = soup.findAll('style')
    style_str = ''
    for style in styles:
        str_style = str(style)
        style_str += str_style
    body = soup.find('body')
    body_str = str(body)
    html = link_str + style_str + lingl_style + body_str
    return html

''' Helper func for dictwebpage (and _pons_API()
    allows to clean the webpage to get only the useful content:
    for ex: remove banner, <script> etc... 
    It's also where we get only the interested content inside the body'''
def _clean_soup(soup, url=None):
    # Remove all <script></script>
    link_scr = ''
    for scr in soup.select('script'):
        str_scr = str(scr)
        # further editing to keep some scripts:
        # default: keep nothing. Write here script link we DO want
        if 'youdao' in url and 'result-min.js' in str_scr:
            link_scr += str_scr
            continue
        scr.extract()
    # We'll keep only <link> and <body>
    links = soup.findAll('link')
    link_str = ''
    for link in links:
        # further editing of <link> or some API (css file messsing up with my own style)
        # default: Keep everything. Write here link Link we DO NOT want
        str_link = str(link)
        # bootstrap style loaded by pons.com are messing up with my own style
        if 'pons' in url  and 'bootstrap_dict_catalogue' in str_link:
            continue
        if 'dict.cc' in url and 'dict.cc/inc/dict.css' in str_link:
            continue
        # for Wordreference.com, the style is inline in fact, in a <style> tag
        if 'wiktionary' in url and 'rel="stylesheet"' in str_link:
            continue
        if 'naver' in url and 'rel="stylesheet"' in str_link:
            continue
        link_str += str_link
    body = soup.find('body')
    # further editing of the <body> for some API
    if 'pons' in url: # Case of a PONS.com website, some div can be removed
        body_pageheader = body.select_one('#page-header')
        if body_pageheader:
            body_pageheader.extract()
        body_containercontent = body.select_one('#container-content')
        if body_containercontent:
            body.select_one('.searchbar-tabs').extract()
        if result_section_nav := body.select_one('#result-section__nav'):
            result_section_nav.extract()
        if result_section_header := body.find_all('h3', {'class':'result-section__header'}):
            [r.extract() for r in result_section_header]
    if 'dict.cc' in url:
        pass
    if 'wordref' in url:
        if full_header := body.find('header', {'class':'full-header'}):
            full_header.extract()
            body.find('div', {'id':'ad1'}).extract()
            body.find('div', {'id':'search'}).extract()
    if 'wiktionary' in url:
        div_mwbody = body.find('div', {'class':'mw-body'})
        body = div_mwbody
    if 'youdao' in url:
        div_results = body.find('div', {'id':'results'})
        body = div_results
    if 'naver' in url:
        div_container = body.find('div', {'id':'container'})
        body = div_container
    body_str = str(body)
    html = link_scr + link_str + body_str 
    return html

'''Helper for all the APIs. Allow to make a word clickable (or using shortcut):
   the word is automatically then put inside the top left Translation box'''
def __convert_clickable_word(current_tag, idx_item):
    trans_item = current_tag.get_text().strip()
    new_tag = '''
        <{current_tag}><span  title="Copy" class="hover_pointer" onclick="addTranslation('{trans_item}');">
            <img src="{button_png}" alt="Copy" />&nbsp;<span id="trans_item_{idx_item}">{trans_item}</span>&nbsp;<span class="text-muted" 
            title="{keyboard_shortcut}">[{idx_item}]</span>
        </span></{current_tag}>'''.format(trans_item=trans_item, 
                                          button_png=static('lwt/img/icn/tick-button.png'), 
                                          idx_item=idx_item, 
                                          keyboard_shortcut=_('keyboard shortcut'),
                                          current_tag=current_tag.name)
    tag_soup = BeautifulSoup(new_tag, 'html.parser').find(current_tag.name)
    current_tag.replace_with(tag_soup)

def _google_API(content):
    raw_data = content.read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = None
    else:
        result = html.unescape(re_result[0])
    return [result]
    

def _pons_API(content, url):
    from django.utils.translation import get_language_info

    soup = BeautifulSoup(content, 'html.parser')
    # Sometimes Pons displays the targeted language in the second block, sometimes in the second...
    pattern = r'(?<=en\.pons\.com/translate/)\w+(?=-)'
    origin_lang = re.search(pattern, url).group().lower()

    divs_lang = soup.find_all('div', {'class':'lang'})
    div_targets = []
    for div_lang in divs_lang:
        # we must determine what is the origin language for each block
        div_lang_origin = div_lang['id']
        is_origin_lang_first = origin_lang == get_language_info(div_lang_origin)['name'].lower()
        if is_origin_lang_first:
            div_targets.extend(div_lang.find_all('div', {'class': 'target'}))
        else:
            div_targets.extend(div_lang.find_all('div', {'class': 'source'}))
            
    for idx, div_target in enumerate(div_targets):
        trans_item = div_target.get_text().strip()
        new_tag = '<span  title="{0}" class="hover_pointer" onclick="addTranslation(\'{1}\');">'
        new_tag += '<img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;'
        new_tag += '<span class="text-muted" title="{4}">[{3}]</span> </span>'
        new_tag = new_tag.format(_('Copy this translation'), trans_item, static('lwt/img/icn/tick-button.png'), 
                                idx+1, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('span')
        div_target.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _dictcc_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    idx_item = 0
    for row in rows:
        if not row.has_attr('id'):
            continue
        idx_item += 1
        td = row.find_all('td')[1]
        trans_item = td.get_text().strip()
        new_tag = '''
            <td><span  title="Copy" class="hover_pointer" onclick="addTranslation('{0}');">
                <img src="{1}" alt="Copy" />&nbsp;<span id="trans_item_{2}">{0}</span>&nbsp;<span class="text-muted" 
                title="{3}">[{2}]</span>
            </span></td>'''.format(trans_item, static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('td')
        td.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wordref_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    td_towrds = soup.find_all('td',{'class':'ToWrd'})
    idx_item = 0
    for td_towrd in td_towrds:
        if td_towrd.get_text() == 'Englisch':
            continue
        idx_item += 1
        spans = td_towrd.find_all('span')
        for span in spans:
            if span.has_attr('title'):
                continue
            span.extract()
        trans_item = td_towrd.get_text().strip()
        new_tag = '''
            <td class="ToWrd"><span  title="{0}" class="hover_pointer" onclick="addTranslation('{1}');">
                <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                title="{4}">[{3}]</span>
            </span></td>'''.format(_('Copy this translation'), trans_item, 
                                   static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('td')
        td_towrd.replace_with(tag_soup)
    span_romans = soup.find_all('span',{'class':'roman'})
    for span_roman in span_romans:
        idx_item += 1
        spans = span_roman.find_all('span')
        for span in spans:
            if span.has_attr('title'):
                continue
            span.extract()
        trans_item = span_roman.get_text().strip()
        new_tag = '''
            <span  title="{0}" class="roman hover_pointer" onclick="addTranslation('{1}');">
                <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                title="{4}">[{3}]</span>
            </span>'''.format(_('Copy this translation'), trans_item, 
                              static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('span')
        span_roman.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wiki_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    ols = soup.find_all('ol')
    idx_item = 0
    for ol in ols:
        for li in ol.find_all('li'):
            idx_item += 1
            to_be_added_str = ''
            span_hqtoggle = li.find('span', {'class':'HQToggle'})
            if span_hqtoggle:
                to_be_added_str += str(span_hqtoggle)
                span_hqtoggle.extract()
            dl = li.find('dl')
            if dl:
                to_be_added_str += str(dl)
                dl.extract()
            trans_item = li.get_text().strip()
            new_tag = '''
                <li><span  title="{0}" class="roman hover_pointer" onclick="addTranslation('{1}');">
                    <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                    title="{4}">[{3}]</span>
                </span>{5}</li>'''.format(_('Copy this translation'), trans_item, 
                                            static('lwt/img/icn/tick-button.png'), idx_item,
                                           _('keyboard shortcut'), to_be_added_str)
            tag_soup = BeautifulSoup(new_tag, 'html.parser').find('li')
            li.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wiki_API_redirect(error, finalurl, word_escaped):
    soup = BeautifulSoup(error, 'html.parser')
    didyoumean = soup.find('span', {'id':'did-you-mean'})
    if didyoumean:
        didyoumean_a = didyoumean.find('a') # --> '/wiki/thisotherspelledword'
        didyoumean_word = didyoumean_a['href'].split('/')[-1]
        didyoumean_word_escaped = parse.quote(didyoumean_word)
        finalurl = finalurl.replace(word_escaped, didyoumean_word_escaped)
    return finalurl

def _youdao_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    div_trans_container = soup.find('div', {'class':'trans-container'})
    lis = div_trans_container.find_all('li')
    idx_item = 0
    for li in lis:
        idx_item += 1
        __convert_clickable_word(li, idx_item)
    div_twebtrans = soup.find('div', {'id':'webTransToggle'})
    titles = div_twebtrans.find_all('div', {'class':'title'})
    for title in titles:
        idx_item += 1
        span = title.find('span')
        if not span: continue
        __convert_clickable_word(span, idx_item)
    html = _clean_soup(soup, url)
    return html

def _naver_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    with open('test.html','w') as test:
        test.write(str(soup))
    div_searchPage_entry = soup.find('div', {'id':'searchPage_entry'})
    ps = div_searchPage_entry.find_all('p', {'class':'mean'})
    idx_item = 0
    for p in ps:
        idx_item += 1
        __convert_clickable_word(p, idx_item)
    div_searchPage_mean = soup.find('div', {'id':'searchPage_mean'})
    div_origins = div_searchPage_mean.find_all('div', {'class':'origin'})
    for div_origin in div_origins:
        a_link = div_origin.find('a', {'class':'link'})
        idx_item += 1
        __convert_clickable_word(a_link, idx_item)
    html = _clean_soup(soup, url)
    return html
