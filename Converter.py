import csv
from xml.etree.ElementTree import Element, SubElement
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
    cursor = -1
    Root = Element('departments')
    while cursor<len(dictList)-1:
        currentUni = dictList[cursor+1]['ÜNİVERSİTE']
        University = SubElement(Root, 'university', name=currentUni, uType=dictList[cursor+1]['ÜNİVERSİTE_TÜRÜ'])
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
                if new['GEÇEN_YIL_MİN_SIRALAMA']=='' or new['GEÇEN_YIL_MİN_SIRALAMA']=='-' : Lastscore.set('order','0')
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

######################################################################3

def XMLtoCSV():
    xmlp = ET.XMLParser(encoding='utf-8')
    f = ET.parse('b.xml',parser=xmlp)
    root = f.getroot()
    newCsv = open('newOne.csv','w',encoding='utf-8')
    newCsv.write('ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n')
    spec = ''
    quota = ''
    field = ''
    period = ''
    order = ''
    lastMin = ''
    for child in root:
        for elem in child:
            newCsv.write(child.get('uType') + ';')
            newCsv.write(child.get('name') + ';')
            newCsv.write(elem.get('faculty') + ';')
            newCsv.write(elem.get('id') + ';')
            for subElem in elem:
                if subElem.tag == 'name':
                    newCsv.write(subElem.text + ';')
                    if subElem.get('lang') == 'en': newCsv.write('İngilizce'+';')
                    else: newCsv.write(';')
                    if subElem.get('second') == 'No' : newCsv.write(';')
                    else : newCsv.write('İkinci Öğretim'+';')
                elif subElem.tag == 'period':
                    period = subElem.text+';'
                elif subElem.tag == 'quota' :
                    spec = subElem.get('spec')+';'
                    quota = subElem.text+';'
                elif subElem.tag == 'field':
                    field = subElem.text+';'
                elif subElem.tag == 'last_min_score':
                    if subElem.get('order') == '0': order = ';'
                    else: order = subElem.get('order')+ ';'
                    if subElem.text != '0':  lastMin = subElem.text
                    else : lastMin = ''
                else:
                    if subElem.text is None:newCsv.write(';')
                    else : newCsv.write(subElem.text+';')
                    newCsv.write(period)
                    newCsv.write(field)
                    newCsv.write(quota)
                    newCsv.write(spec)
                    newCsv.write(order)
                    newCsv.write(lastMin)
                    newCsv.write('\n')
    newCsv.close()

#CSVtoXML()
#XMLtoCSV()

#######################################################

def CSVtoJSON():
    readCSV()
    ov = open('arifke.json','wb')
    cursor = -1
    universityList = []
    while cursor < len(dictList) -1:
        currentUni = dictList[cursor + 1]['ÜNİVERSİTE']
        currentType = dictList[cursor + 1]['ÜNİVERSİTE_TÜRÜ']
        cond = (x for x in dictList if x['ÜNİVERSİTE'] == currentUni)
        itemList = []

        for dictOne in cond:
            if dictOne['DİL'] == "":dictOne['DİL'] = 'tr'
            else: dictOne['DİL'] = 'en'
            if dictOne['ÖĞRENİM_TÜRÜ'] == "":dictOne['ÖĞRENİM_TÜRÜ']='No';
            else:dictOne['ÖĞRENİM_TÜRÜ']='Yes'
            if dictOne['OKUL_BİRİNCİSİ_KONTENJANI'] == "":dictOne['OKUL_BİRİNCİSİ_KONTENJANI'] = '0'
            if dictOne['GEÇEN_YIL_MİN_SIRALAMA'] == "":dictOne['GEÇEN_YIL_MİN_SIRALAMA'] = '0'
            if dictOne['GEÇEN_YIL_MİN_PUAN'] == "" or dictOne['GEÇEN_YIL_MİN_PUAN'] == "-" : dictOne['GEÇEN_YIL_MİN_PUAN'] = '0'
            if dictOne['BURS'] == "": dictOne['BURS'] = None;
            item = {
                '@faculty':dictOne['FAKÜLTE'],
                '@id':dictOne['PROGRAM_KODU']
            }
            name = {
                'name' :{
                '@lang':dictOne['DİL'],
                '@second':dictOne['ÖĞRENİM_TÜRÜ'],
                '#text' :dictOne['PROGRAM']
                }
            }
            period = {
                'period' :dictOne['ÖĞRENİM_SÜRESİ']
            }
            quota = {
                'quota' :{
                '@spec' :dictOne['OKUL_BİRİNCİSİ_KONTENJANI'],
                '#text':dictOne['KONTENJAN']
                }
            }
            field = {
                'field':dictOne['PUAN_TÜRÜ']
            }
            last_min_score = {
                'last_min_score':{
                '@order':dictOne['GEÇEN_YIL_MİN_SIRALAMA'],
                '#text':dictOne['GEÇEN_YIL_MİN_PUAN']
                }
            }
            grandDict = {
                'grant':dictOne['BURS']
            }
            merged = {**name, **period, **quota,**field,**last_min_score,**grandDict}
            item = {**item,**merged}
            itemList.append(item)
            cursor = dictList.index(dictOne)
        university = {

                '@name': currentUni,
                '@uType': currentType,
                'item': itemList
        }
        universityList.append(university)
    departments ={
        'departments':{
            'university':universityList
        }
    }
    json_string = json.dumps(departments, indent=4, ensure_ascii=False).encode('utf8')
    ov.write(json_string)
#CSVtoJSON()




############################################################

def JSONtoCSV():
    newOv = open('arifke.json',encoding='utf-8')
    data = json.load(newOv)
    newCsv = open('json.csv', 'w', encoding='utf-8')
    newCsv.write('ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n')
    university = data['departments']['university']
    for uni in university:
        for item in uni['item']:
            if item['name']['@lang'] == 'en' : item['name']['@lang'] = 'İngilizce'
            else:item['name']['@lang'] = ''
            if item['name']['@second'] == 'Yes' : item['name']['@lang'] = 'İkinci Öğretim'
            else:item['name']['@second'] = ''
            if item['quota']['@spec'] == '0':item['quota']['@spec'] = ''
            if item['last_min_score']['@order'] == '0':item['last_min_score']['@order'] = ''
            if item['last_min_score']['#text'] == '0' :item['last_min_score']['#text'] = ''
            if item['grant'] is None : item['grant'] = ''
            newCsv.write(uni['@uType']+';')
            newCsv.write(uni['@name']+';')
            newCsv.write(item['@faculty']+';')
            newCsv.write(item['@id']+';')
            newCsv.write(item['name']['#text']+';')
            newCsv.write(item['name']['@lang']+';')
            newCsv.write(item['name']['@second']+';')
            newCsv.write(item['grant']+';')
            newCsv.write(item['period'] + ';')
            newCsv.write(item['field'] + ';')
            newCsv.write(item['quota']['#text'] + ';')
            newCsv.write(item['quota']['@spec'] + ';')
            newCsv.write(item['last_min_score']['@order'] + ';')
            newCsv.write(item['last_min_score']['#text']+'\n')


JSONtoCSV()



