import xml.etree.cElementTree as element_tree
from xml.dom import minidom
import json


with open('inverted_index.json') as inputfile:
    data = json.load(inputfile)

root = element_tree.Element("inverted_index")
		    
for lemma in data:
    xml_lemma = element_tree.SubElement(root,"lemma",name = lemma)
    for article in data[lemma]:
        for article_single in article:
            element_tree.SubElement(xml_lemma,"document",id = article_single, weight = str(article[article_single]))

tree = element_tree.ElementTree(root)

xmlstr = minidom.parseString(element_tree.tostring(root)).toprettyxml(indent="   ")
with open("inverted_index.xml", "w") as outputfile:
    outputfile.write(xmlstr)

