# coding: utf-8
import numpy as np
import pandas as pd
import dateutil

_csv_header_to_field = {u'Kirjauspäivä':'registry_date',
	u'Arvopäivä':'value_date',
	u'Maksupäivä':'pay_date',
	u'Määrä':'amount',
	u'Saaja/Maksaja':'party',
	u'Tilinumero':'account_number',
	u'Tapahtuma':'action',
	u'Viite':'reference',
	u'Viesti':'message'}


def dataframe_from_nordea_csv(fname):
	d = pd.read_csv(fname,
			sep='\t', skiprows=1, encoding='utf-8',
			decimal=',')
	d = d.dropna(subset=[d.columns[0]])


	# Parse dates (three first columns). Interpret as UTC dates
	for iCol in range(3):
		d.iloc[:, iCol] = d.iloc[:, iCol].map(lambda s: dateutil.parser.parse(s, dayfirst=1).date())

	# Remove obsolete columns and rename to fields
	d = d[_csv_header_to_field.keys()].rename(columns=_csv_header_to_field)

	# strip() string columns
	for field in ['party', 'account_number', 'action', 'reference', 'message']:
		d[field] = d[field].str.strip()
		# Normalize NaNs etc to empty string
		if not np.issubdtype(d[field].dtype, float):
			d[field].fillna('', inplace=True)

	return d

def dataframe_to_transactions(df):
	from models import Transaction
	transactions = [Transaction(**dict(row.iteritems()))
                        for _, row in df.iterrows()]
	return transactions

def transactions_from_nordea_csv(fname):
	"""Construct list of Transaction models from a CSV file"""
	d = dataframe_from_nordea_csv(fname)
	transactions = dataframe_to_transactions(d)
	return transactions
