import pandas as pd
import re
from itertools import izip

class Tagger(object):

    def get_category(self, transaction):
        """Return Category representing the transaction.
        Return None to continue categorization."""
        pass

class EnsebleTagger(object):

    def __init__(self):
        self._registry = []

    def get_category(self, transaction):
        for tagger in self._registry:
            cat = tagger.tag(transaction)
            if cat is not None:
                return cat
        return None

    def register_tagger(self, tagger):
        if tagger in self._registry:
            raise ValueError('Tagger already registered!')

        self._registry.append(tagger)

    def unregister_tagger(self, tagger):
        self._registry.remove(tagger)


class PartyBasedTagger(object):

    def __init__(self, patterns, categories, expr, flags=re.IGNORECASE|re.UNICODE):
        self.patterns = [re.compile(unicode(p).strip(), flags=flags|re.UNICODE) for p in patterns]
        self.categories = categories
        self.expr = expr

    @classmethod
    def from_csv(cls, fname, flags=re.IGNORECASE|re.UNICODE):
        f = pd.DataFrame.from_csv(fname, sep='\t', index_col=False, encoding='utf-8')
        party_patterns = f['party_regex']
        cat = f['category']
        expr = f['expr'].str.strip().fillna('')
        return cls(party_patterns, cat, expr, flags)

    def get_category(self, transaction):
        for pat, cat, expr in izip(self.patterns, self.categories, self.expr):
            if (pat.search(transaction.party) and
               (not expr or bool(eval(expr, {'t': transaction})))):
                return cat
        return None




DEFAULT_TAGGER = EnsebleTagger()
DEFAULT_TAGGER.register_tagger(PartyBasedTagger([], [], []))