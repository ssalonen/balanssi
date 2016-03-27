# coding=utf-8

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date

import pandas as pd
import numpy as np
from pkg_resources import resource_filename #@UnresolvedImport #pylint: disable=E0611
from django.test import TestCase

from balanssi.parsers import dataframe_from_nordea_csv


class TestNordeaParser(TestCase):
    
    def test_nordea_dataframe(self):
        fname = resource_filename(__name__, 'test_dump_nordea.csv')
        self.assert_(fname)

        df = dataframe_from_nordea_csv(fname)

        expected_registry_dates = np.r_[[date(2013, 1, 2)]*2,
                               [date(2013, 1, 3)]*2,
                               [date(2013, 1, 4)]*3,
                               [date(2013, 1, 7)]*2,
                               [date(2013, 1, 8)]].tolist()

        expected_value_dates = expected_registry_dates
        expected_pay_dates = expected_registry_dates
        expected_amounts = [-27, -27.3, 146.05, -36.26,
                            -34.40, -41, -97.01, -19.6,
                            -55.2, -63.30]
        expected_parties = ['AS OY PIENIKATU 2',
                            'Puoti Oy',
                            'Matti Nieminen',
                            'CITYMARKET HELSINKI',
                            'Grillikioski Medzan',
                            'Vinoteca Oy',
                            u'SÄHKÖINFO OY',
                            '4 VUODENAIKAA',
                            'ABC VIINIKKA',
                            'K SUPERMARKET RUOKANI']
        expected_account_numbers = np.r_[['123456-999888'],
                                    ['']*5,
                                    ['12000-88888'],
                                    ['']*3]

        self.assertSequenceEqual(list(df.registry_date), expected_registry_dates)
        self.assertSequenceEqual(list(df.value_date), expected_value_dates)
        self.assertSequenceEqual(list(df.pay_date), expected_pay_dates)
        self.assertTrue(np.allclose(df.amount, expected_amounts))
        self.assertSequenceEqual(list(df.party), expected_parties)
        
        expected_account_numbers_nonull = pd.Series(expected_account_numbers).dropna()
        self.assertSequenceEqual(list(df.account_number.dropna()), 
                                    list(expected_account_numbers_nonull))
        self.assertSequenceEqual(list(df.account_number.isnull()), 
                                    list(pd.Series(expected_account_numbers).isnull()))


        # TODO: test other fields