from bs4 import BeautifulSoup
import requests

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

def getWebSite(url):
	r = requests.get(url)
	return r.text

def getIptvs(webSite):
	soup = BeautifulSoup(webSite, 'html.parser').body.find_all('p')[2].encode("ascii")
	pTagRemoved = str(soup).replace("<p>", "")
	pTagRemoved = pTagRemoved.replace("</p>", "")
	brTagReplaced = pTagRemoved.replace("<br/>\\n", ",")
	splitted = brTagReplaced.split('#EXTINF:-1,')
	splitted.pop(0) # b'#EXTM3U

	return removeEndComma(splitted)

def removeEndComma(list):
	iptvs = []
	for element in list:
		iptvs.append(element[:-1])
	return iptvs

def generateF4m(iptvs):
	streamingInfos = Element('streamingInfos')

	for iptv in iptvs:
		data = iptv.split(',')
		item = SubElement(streamingInfos, 'item')
		title = SubElement(item, 'title')
		title.text = data[0]

		link = SubElement(item, 'link')
		link.text = "plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url=" + data[1]

		thumbnail = SubElement(item, 'thumbnail')
		thumbnail.text = "imagehere"

	return prettify(streamingInfos)

def prettify(elem):
	"""Return a pretty-printed XML string for the Element.
	"""
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def writeIntoFile(fileName, content):
	f = open(fileName, 'w')
	f.write(content)
	f.close()

url = 'http://iptv.filmover.com/european-iptv-playlist-29-09-2016/'
webSite = getWebSite(url)
iptvs =  getIptvs(webSite)
f4mContent = generateF4m(iptvs)
writeIntoFile('result.xml', f4mContent)
