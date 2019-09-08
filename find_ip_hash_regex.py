import re

text = "hjdh hdfh j 8 98  90 m hj87  123.2.2.3 kjdkf  2.4.5.6.7.8"

print(re.search(r"([0-9]{1,}\.){3}[0-9]{1,}", text)[0])

text= "the md5 is ee7052756112a78d0040ffcf85ba9d26 righ ee7052756112a78d0040ffcf85ba9d26 t?"

print(re.findall(r"[0-9a-fA-F]{32}", text))