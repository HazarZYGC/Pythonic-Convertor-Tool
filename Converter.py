import csv
from xml.etree.ElementTree import Element, SubElement,tostring
import xml.dom.minidom
import xml.etree.ElementTree as ET
import json



SOURCE_FILE = ''
DESTINATION_FILE = ''
CONVERTION = ''
dictList = []
#CSV

#read csv
def readCSV():
    with open('DEPARTMENTS.csv', 'r', encoding="utf8") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=";")
        for row in csvreader:
            dictList.append(dict(row))


def CSVtoXML():
    readCSV()
    cursor = 0
    Root = Element('departments')
    while cursor<len(dictList)-1:
        currentUni = dictList[cursor+1]['ÜNİVERSİTE']
        University = SubElement(Root, 'university', name=currentUni, uType=dictList[cursor]['ÜNİVERSİTE_TÜRÜ'])
        cond = (x for x in dictList if x['ÜNİVERSİTE'] == currentUni)
        for new in cond:
            Item = SubElement(University, 'item', id=new['PROGRAM_KODU'], faculty=new['FAKÜLTE'])
            Name = SubElement(Item, 'name')
            Name.text = new['PROGRAM']
            if new['DİL'] == '':
                if new['ÖĞRENİM_TÜRÜ']=='' : Name.set('lang','tr');Name.set('second','No')
                else: Name.set('lang','tr');Name.set('second','Yes')
            else:
                if new['ÖĞRENİM_TÜRÜ'] == '' : Name.set('lang','en');Name.set('second','No')
                else : Name.set('lang','en');Name.set('second','Yes')
            Period = SubElement(Item, 'period');Period.text = new['ÖĞRENİM_SÜRESİ']
            Quota = SubElement(Item, 'quota');Quota.text = new['KONTENJAN']
            if new['OKUL_BİRİNCİSİ_KONTENJANI'] == '': Quota.set('spec','0')
            else : Quota.set('spec',new['OKUL_BİRİNCİSİ_KONTENJANI'])
            Field = SubElement(Item, 'field');Field.text = new['PUAN_TÜRÜ']
            if new['GEÇEN_YIL_MİN_PUAN'] == '':
                Lastscore = SubElement(Item, 'last_min_score');Lastscore.text = '0'
                if new['GEÇEN_YIL_MİN_SIRALAMA']=='' : Lastscore.set('order','0')
                else: Name.set('lang',new['GEÇEN_YIL_MİN_SIRALAMA'])
            else:
                Lastscore = SubElement(Item, 'last_min_score');Lastscore.text = new['GEÇEN_YIL_MİN_PUAN']
                if new['GEÇEN_YIL_MİN_SIRALAMA']=='' : Lastscore.set('order','0')
                else: Lastscore.set('order',new['GEÇEN_YIL_MİN_SIRALAMA'])
            Grant = SubElement(Item, 'grant')
            if new['BURS'] != '' : Grant.text = new['BURS']
            cursor = dictList.index(new)
            #print(cursor)
    mydata = ET.tostring(Root,encoding='utf-8')
    ovv = xml.dom.minidom.parseString(mydata)
    mydatas = ovv.toprettyxml(encoding='utf-8')
    myfile = open('b.xml','wb')
    myfile.write(mydatas)
    myfile.close()
CSVtoXML()



xmlp = ET.XMLParser(encoding='utf-8')
f = ET.parse('b.xml',parser=xmlp)
root = f.getroot()
for child in root:
    print(child.tag, child.attrib)
#CSVtoXML()
