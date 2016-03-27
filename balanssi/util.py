from balanssi.models import Transaction

def save_transactions_if_new(transactions):
    """Save transactions if they are "new" (determined by get_similar_kw). Created transactions are returned."""
    def yield_new():
        for t in transactions:
            kw = t.get_similar_kw()
            obj, created = Transaction.objects.get_or_create(**kw)
            if created:
                yield obj
    
    return list(yield_new())