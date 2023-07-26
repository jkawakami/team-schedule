import re

txt = "Jacksonville0-0"
x = re.search('\d{1,3}-\d{1,3}', txt)
print(x)
print(x.start())
print(txt)
