import locale
from datetime import datetime
import time


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

a = datetime.now().strftime('%d %B %Y')

b = datetime.now()

c = datetime.now().hour

d = datetime.now().minute

print(c, d)