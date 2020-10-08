from datetime import datetime
from urllib.parse import quote

from numpy import unicode

# a = "1期"
# b = '1\u671f'
# c = a.encode("raw_unicode_escape", "utf-8").decode()
# print(a)
# print(b)
# print(c)
# print(type(b))
# print(quote(a))
# print(quote(b))
# print(quote(c))
a = datetime.now().strftime("%Y-%m-%d")
print(a)


