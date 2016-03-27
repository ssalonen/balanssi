#import pandas as pd
from django.db import models

#def equal_or_both_null(o1, o2):
#    return (pd.isnull(o1) and pd.isnull(o2)) or (o1 == o2)

# Create your models here.
class Transaction(models.Model):
    registry_date = models.DateField('Kirjauspaiva')
    value_date = models.DateField('Arvopaiva')
    pay_date = models.DateField('Maksupaiva')
    amount = models.FloatField('Maara')
    party = models.CharField(max_length=50)
    account_number = models.CharField(max_length=34)
    action = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    category = models.ForeignKey('categories.Category', blank=True, null=True)

    def get_similar_kw(self):
        """Return dict representing this Transaction. Categories are not included. TODO: Use with get_or_create?"""
        return dict(registry_date=self.registry_date,
                      value_date=self.value_date,
                      pay_date=self.pay_date,
                      amount=self.amount,
                      party=self.party,
                      account_number=self.account_number,
                      action=self.action,
                      reference=self.reference,
                      message=self.message,
                      category=self.category)
#    def sameas(self, other):
#        """Whether two transactions are representing the same transaction event. Tags are ignored."""
#        # we do not want to override == operator
#        return (equal_or_both_null(self.registry_date, other.registry_date) and
#                equal_or_both_null(self.value_date, other.value_date) and
#                equal_or_both_null(self.pay_date, other.pay_date) and
#                np.allclose(self.amount, other.amount) and
#                equal_or_both_null(self.party, other.party) and
#                equal_or_both_null(self.account_number, other.account_number) and
#                equal_or_both_null(self.action, other.action) and
#                equal_or_both_null(self.reference, other.reference) and
#                equal_or_both_null(self.message, other.message))

    def __unicode__(self):
        return (u'Transaction(party={self.party}, '
                    'amount={self.amount}, '
                    'message={self.message}, '
                    'pay_date={self.pay_date}, '
                    'category={self.category})'.format(self=self))


