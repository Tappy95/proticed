import time
from decimal import Decimal

a = {}
category_id = 'aaaa'
site = 'us'
update_time = time.time()
b = a.setdefault((category_id, site, update_time),
                                             [0, 0, 0, Decimal('0.00'), Decimal('0.00'), Decimal('0.00')])
print(b)
b[0] = 1
print(a)