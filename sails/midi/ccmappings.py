from collections import defaultdict

from sails.ui import App


class CCMappings(object):
    def __init__(self):
        self.cc_aliases = defaultdict(set)
        self.alias_ccs = defaultdict(set)
        self.reload()

    def reload(self):
        App.settings.beginGroup("midi")
        try:
            source = App.settings.value("cc_mappings") or ""
        finally:
            App.settings.endGroup()
        self.cc_aliases.clear()
        self.alias_ccs.clear()
        for line in source.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("=", 1)
            if len(parts) != 2:
                continue
            parts = [p.strip() for p in parts]
            cc, alias = parts
            try:
                channel, cc = cc.split()
                channel = int(channel) - 1
                cc = int(cc)
            except ValueError:
                continue
            self.cc_aliases[(channel, cc)].add(alias)
            self.alias_ccs[alias].add((channel, cc))

    @property
    def options(self):
        return [""] + list(sorted(self.alias_ccs))


cc_mappings = CCMappings()
