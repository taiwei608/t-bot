# -*- coding: utf8 -*-
import requests
import chardet
from xml.etree.ElementTree import ElementTree
import urllib
NS = {"ns" : "urn:cwb:gov:tw:cwbcommon:0.1"}
def get(city):

	KeyFile = open("CWBtoken", "r")
	Token = KeyFile.read().strip()
	print Token
	URL = "http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey=" + Token
	print URL
	print "download weather xml file"
	xmlfile = urllib.URLopener()
	xmlfile.retrieve(URL, "xmlfile.xml")

	print "parse data"
	tree = ElementTree()
	tree.parse("xmlfile.xml")
	
	if '台' in city:
		city = city.replace("台", "臺")

	city = city.decode("utf-8") 
	'''
	print city
	print type(city)
	print cityEncoded
	print type(cityEncoded)
	if(cityEncoded == u"高雄市"):
		print "success"
	else:
		print "fail"
	'''
	'''
	if '台' in city:
		city = city.replace("台", "臺")
	print city
	city = unicode(city, errors='ignore')
	print city
	print type(city)
	'''
	for location in tree.find("ns:dataset", NS).findall("ns:location", NS):
		locationName = location.find("ns:locationName", NS).text
		test = u"臺北市"
		if locationName == city:
			weatherInfo = dict()
			weatherElements = location.findall("ns:weatherElement", NS) 
			#print locationName
			for weatherElement in weatherElements:
				elementName = weatherElement.find("ns:elementName", NS).text
				for time in weatherElement.findall("ns:time", NS):
					startTime = time.find("ns:startTime", NS).text
					endTime = time.find("ns:endTime", NS).text
					parameterName = time.find("ns:parameter", NS).find("ns:parameterName", NS).text

					if elementName == u"MaxT":
						parameterName = parameterName + "C ~ "
					elif elementName == u"MinT":
						parameterName = parameterName + "C "
					elif elementName == u"PoP":
						parameterName = parameterName + "%"
					else:
						parameterName = parameterName + " "

					startTime = startTime.split("+")
					endTime = endTime.split("+")
					weatherKey = startTime[0] + " ~ " + endTime[0] + " "

					if(weatherKey in weatherInfo):
						weatherInfo.update({weatherKey:weatherInfo[weatherKey] + parameterName})
					else:
						weatherInfo.update({weatherKey:parameterName})

					#print startTime + "~" + endTime + " " + elementName + " " + parameterName 
					#print weatherInfo[startTime + endTime]
		
			returnStr = ""
			if(len(weatherInfo)):
				for date, info in sorted(weatherInfo.items()):
					returnStr += date + "\n" + info + "\n"
			locationCity = "[%s]\n" % locationName
			returnStr = locationCity + returnStr
			print returnStr
			return returnStr
	return "無法查無資訊"

