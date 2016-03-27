import os
from .models import Transaction
from .util import save_transactions_if_new
from .parsers import transactions_from_nordea_csv
from .taggers import DEFAULT_TAGGER, PartyBasedTagger
from .taggers import __file__ as taggers_path

from categories.models import Category

taggers_path = os.path.dirname(taggers_path)


from django.db import transaction


#@transaction.commit_on_success() # see http://stackoverflow.com/questions/20039250/django-1-6-transactionmanagementerror-database-doesnt-behave-properly-when-aut
def load_data(fname):
    transactions = transactions_from_nordea_csv(fname)
    fpath = os.path.join(taggers_path,
                'category_mapping.csv')
    tagger = PartyBasedTagger.from_csv(fpath)
    cat_name_to_obj = {None: None}
    #DEFAULT_TAGGER.register_tagger(tagger)
    for t in transactions:
        cat_name = tagger.get_category(t)
        print t

        if cat_name in cat_name_to_obj:
            cat = cat_name_to_obj[cat_name]
        else:
            try:
                cat = Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                raise ValueError('Category "{}" does not exist'.format(cat_name))

        if cat:
            print '   --> tagged', cat
            t.category = cat
    print ''
    print ''
    print ''
    print 'Untagged:'
    for t in transactions:
        if t.category:
            continue
        print t

    new_transactions = save_transactions_if_new(transactions)
    print 'saved', str(len(new_transactions)), 'transactions'


#@transaction.commit_on_success() # see http://stackoverflow.com/questions/20039250/django-1-6-transactionmanagementerror-database-doesnt-behave-properly-when-aut
def delete_all_transactions():
    for t in Transaction.objects.all():
        t.delete()