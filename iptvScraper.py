from bs4 import BeautifulSoup
import requests

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

def getWebSite(url):
	r = requests.get(url)
	return r.text

def getIptvs(webSite):
	text = BeautifulSoup(webSite, 'html.parser').body.text
	splittedText = text.split('#EXTINF:-1,')
	splittedText.pop(0) # b'#EXTM3U
	splittedText.pop()

	return removeEndComma(splittedText)

def removeEndComma(list):
	iptvs = []
	for element in list:
		iptvs.append(element.replace('\n', ',')[:-1])

	return iptvs

def printList(list):
	for element in list:
		print(element.encode('utf-8'))

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
	return reparsed.toprettyxml(indent="  ").encode('utf-8')

def writeIntoFile(fileName, content):
	f = open(fileName, 'wb')
	f.write(content)
	f.close()

url = 'http://iptv.filmover.com/iptv-italian-and-french-playlist/'
webSite = getWebSite(url)
iptvs =  getIptvs(webSite)
printList(iptvs)
f4mContent = generateF4m(iptvs)
#print(f4mContent)
writeIntoFile('result.xml', f4mContent)
