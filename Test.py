import requests
from bs4 import BeautifulSoup
from bs4 import  NavigableString
from bs4 import  Tag
import re
# Tag("sada").f

html = '''
<li>
<span class="sprite safghanistan" title="Afghanistan"></span> <a href="afghanistan-1.html">Afghanistan</a>
</li>
<li>
<span class="sprite salbania_section" title="Albania"></span> <a href="albania_section-1.html">Albania</a>
<ul>
<li>
<span class="sprite salbanie" title="Albania"></span> <a href="albanie-1.html">Albania</a>
</li>
<li>
<span class="sprite sshkroder_city" title="City of Shkodër"></span> <a href="shkroder_city-1.html">Shkodër, <em>City of</em></a>
</li>
</ul>
</li>
<li>
<span class="sprite salgerie" title="Algeria"></span> <a href="algerie-1.html">Algeria</a>
</li>

'''
soup = BeautifulSoup(html,  'html.parser')

list_of_li = soup.findChildren("li", recursive=False)
# print(list_of_li)



print("#############################")
# print(list_of_li[0])
a = list_of_li[0].find_all(re.compile('<span.+' ))
print(str(list_of_li[0]))
a = re.findall('title="(.+)".+href="(.+)"', str(list_of_li[0]), flags=re.M|re.I|re.DOTALL)
print(a)
print("#############################")
print(list_of_li[1])
# a = list_of_li[1].find_all(re.compile('.+title="(.+)".+href="(.+)"', flags=re.M|re.I|re.DOTALL))
a = re.findall('title="(.+)".+href="(.+)"', str(list_of_li[1]), flags=re.I)
print(a)


# print("#############################")
# a = list_of_li[0].findChildren("li")
# print(a)
# print("#############################")
# a = list_of_li[1].findChildren("li")
# print(a)


# print(soup.findChildren("li", recursive=False))


# print(help(soup))
# print(help(soup.find))
# print(help(soup.findAll))

# print(soup.find_all("ul"))
# print(tag.get())