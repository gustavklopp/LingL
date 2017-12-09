# -*- coding: utf-8 -*-
from django import get_version, forms
from django.forms import Widget
from django import utils
import copy
import json
from django.forms.utils import flatatt


class SplitJSONWidget(forms.Widget):

    def __init__(self, attrs=None, newline='<br/>\n', sep='__', debug=False):
        self.newline = newline
        self.separator = sep
        self.debug = debug
        Widget.__init__(self, attrs)

    def _as_text_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, extra_attrs={'type':'text',
                                             'name':"%s" % (key)})
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        return u""" <label for="%s">%s:</label>
        <input%s />""" % (attrs['id'], key, flatatt(attrs))

    def _to_build(self, name, json_obj):
        inputs = []
        for el in json_obj:
            k = list(el.keys())[0]
            v = list(el.values())[0]
            inputs.append(self._as_text_field(name, k, v))
        return inputs

    def _prepare_as_ul(self, l):
        ul = '<ul>'
        for el in l:
            ul += '<li>%s</li>' % el
        return ul

    def _to_pack_up(self, root_node, raw_data):

        copy_raw_data = copy.deepcopy(raw_data)
        result = []

        def _to_parse_key(k, v):
            if k.find(self.separator) != -1:
                apx, _, nk = k.rpartition(self.separator)
                try:
                    # parse list
                    int(nk)
                    l = []
                    obj = {}
                    index = None
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            head, _, t = key.rpartition(self.separator)
                            _, _, index = head.rpartition(self.separator)
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                try:
                                    int(t)
                                    l.append(val)
                                except ValueError:
                                    if index in obj:
                                        obj[index].update({t: val})
                                    else:
                                        obj[index] = {t: val}
                                del copy_raw_data[key]
                        if obj:
                            for i in obj:
                                l.append(obj[i])
                    l.append(v)
                    return _to_parse_key(apx, l)
                except ValueError:
                    # parse dict
                    d = {}
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            _, _, t = key.rpartition(self.separator)
                            try:
                                int(t)
                                continue
                            except ValueError:
                                pass
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                d.update({t: val})
                                del copy_raw_data[key]
                    v = {nk: v}
                    if d:
                        v.update(d)
                    return _to_parse_key(apx, v)
            else:
                return v

        for k, v in raw_data.iteritems():
            if k in copy_raw_data:
                # to transform value from list to string
                v = v[0] if isinstance(v, list) and len(v) is 1 else v
                if k.find(self.separator) != -1:
                    d = _to_parse_key(k, v)
                    # set type result
                    if not len(result):
                        result = type(d)()
                    try:
                        result.extend(d)
                    except:
                        result.update(d)
        return result

#     def value_from_datadict(self, data, files, name):
#         data_copy = copy.deepcopy(data)
#         result = self._to_pack_up(name, data_copy)
#         return json.dumps(result)

    def render(self, name, value, attrs=None):
        try:
            value = json.loads(value)
        except (TypeError, KeyError):
            pass
        inputs = self._to_build(name, value or {})
        result = self._prepare_as_ul(inputs)
        if self.debug:
            # render json as well
            source_data = u'<hr/>Source data: <br/>%s<hr/>' % str(value)
            result = '%s%s' % (result, source_data)
        return utils.safestring.mark_safe(result)
