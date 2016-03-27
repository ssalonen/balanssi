from __future__ import absolute_import
import pandas as pd
from rest_pandas import PandasView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from balanssi.models import Transaction
from balanssi.serializers import TransactionSerializer
from categories.models import Category


def _construct_inequality_queryset_kwargs(field, req_dict):
    kw = {}
    for op in 'gt', 'gte', 'lt', 'lte':
        k = '{field}__{op}'.format(**locals())
        v = req_dict.get(k)
        if v is not None:
            v = float(v)
            kw[k] = v
            print op
    return kw

class TransactionsView(PandasView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def filter_queryset(self, qs):
        print 'filter'
        req = self.request
        kk = _construct_inequality_queryset_kwargs('amount', req.GET)
        if kk:
            qs = qs.filter(**kk)
            print kk
        return qs

    def transform_dataframe(self, df):
        #print 'dtypes', df.dtypes
        req = self.request

        # hack, query category names
        cat_defined = ~df['category'].isnull().values
        cat_ids = list(df['category'].iloc[cat_defined])
        categories = Category.objects.in_bulk(cat_ids)
        df['category'] = [str(categories[k]) if not pd.isnull(k) else 'N/A'
                            for k in df['category']]


        groupby_key = req.GET.get('groupby')
        #print 'groupby:', groupby_key
        if not groupby_key:
            return df
        groupby_op = req.GET.get('groupby_op', 'sum')
        #print 'groupby op:', groupby_op
        if not groupby_op:
            return df

        cols = req.GET.get('cols', 'amount')
        cols = cols.split(',')


        grouped = df.groupby(groupby_key)[cols]

        str2op = {'sum': grouped.sum, 'mean': grouped.mean,
                  'min' : grouped.min, 'max': grouped.max}
        return str2op[groupby_op]()


def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def vis(request):
    return TemplateResponse(request, 'test.html')
