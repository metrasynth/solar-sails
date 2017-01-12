from collections import defaultdict

from sails.ui import App


class CCMappings(object):

    def __init__(self):
        self.reload()

    def reload(self):
        App.settings.beginGroup('midi')
        try:
            source = App.settings.value('cc_mappings') or ''
        finally:
            App.settings.endGroup()
        self.cc_aliases = defaultdict(set)
        self.alias_ccs = defaultdict(set)
        for line in source.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split('=', 1)
            if len(parts) != 2:
                continue
            parts = [p.strip() for p in parts]
            cc, alias = parts
            try:
                cc = int(cc)
            except ValueError:
                continue
            self.cc_aliases[cc].add(alias)
            self.alias_ccs[alias].add(cc)

    @property
    def options(self):
        return [''] + list(sorted(self.alias_ccs))


cc_mappings = CCMappings()
