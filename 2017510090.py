
# !!! BEFORE RUNNING:
#Pythonic Converter Tool is programmed on Python 3.6
#It will be problem if it runs under Python 3.5 version. Because of dictionary merging function syntax.
#Also, if it runs on Python 2 versions it will return encoding error. Because of special Turkish characters.
import csv
from xml.etree.ElementTree import Element, SubElement
import xml.dom.minidom #it is just used for pretty print xml doc.
import xml.etree.ElementTree as ET
from lxml import etree
import json
import sys

# Controlling argv are valid or not:
if len(sys.argv) == 4:
    SOURCE_FILE = sys.argv[1]
    DESTINATION_FILE = sys.argv[2]
    CONVERTION = sys.argv[3]
    dictList = [] #Global dictionary variable for using in convertion methods.
else:
    print('There is a input error.A typical command line usage is as follows:')
    print('python <filename> <input file> <output file/xsd file> <type>')
    sys.exit(0)


# MAIN METHOD:
# It is invoked on the bottom of the code.
def main():
    #Calling convertion methods corresponding to operation type and controllinf file extensions.
    if CONVERTION=='1' and SOURCE_FILE.endswith('.csv') and DESTINATION_FILE.endswith('.xml'):CSVtoXML()
    elif CONVERTION=='2' and SOURCE_FILE.endswith('.xml') and DESTINATION_FILE.endswith('.csv'):XMLtoCSV()
    elif CONVERTION=='3' and SOURCE_FILE.endswith('.csv') and DESTINATION_FILE.endswith('.json'):CSVtoJSON()
    elif CONVERTION=='4' and SOURCE_FILE.endswith('.json') and DESTINATION_FILE.endswith('.csv'):JSONtoCSV()
    elif CONVERTION=='5' and SOURCE_FILE.endswith('.xml') and DESTINATION_FILE.endswith('.json'):XMLtoJSON()
    elif CONVERTION=='6' and SOURCE_FILE.endswith('.json') and DESTINATION_FILE.endswith('.xml'):JSONtoXML()
    elif CONVERTION=='7' and SOURCE_FILE.endswith('.xml') and DESTINATION_FILE.endswith('.xsd'):ValidateXML();sys.exit(0)
    else:
        print('Invalid operation number or invalid file extension. Use these operation numbers:')
        print('1=CSV to XML, 2=XML to CSV, 3=XML to JSON,4=JSON to XML, 5=CSV to JSON, 6=JSON to CSV,7=XML validates with XSD')
        sys.exit(0)
    print('FILE CONVERTION IS SUCCESSFULL.')


# READ CSV METHOD:
def readCSV():
    try:
        #encoding option is used for special characters in csv file.
        with open(SOURCE_FILE, 'r', encoding="utf8") as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=";")
            for row in csvreader:
                dictList.append(dict(row))
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)


# CSV TO XML CONVERTION:
def CSVtoXML():
    readCSV()
    #cursor for controlling university names:
    cursor = -1
    Root = Element('departments')
    while cursor<len(dictList)-1:
        currentUni = dictList[cursor+1]['ÜNİVERSİTE']
        # new university element for each university:
        University = SubElement(Root, 'university', name=currentUni, uType=dictList[cursor+1]['ÜNİVERSİTE_TÜRÜ'])
        # picking same universities:
        cond = (x for x in dictList if x['ÜNİVERSİTE'] == currentUni)
        for new in cond:

            # Controlling each column and adding new subelements for item element.
            # Some subelements and attributes is controlling for csv empty column.

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
            if new['GEÇEN_YIL_MİN_PUAN'] == '' or new['GEÇEN_YIL_MİN_PUAN'] == '-':
                Lastscore = SubElement(Item, 'last_min_score');Lastscore.text = '0'
                if new['GEÇEN_YIL_MİN_SIRALAMA']=='' : Lastscore.set('order','0')
                else: Name.set('order',new['GEÇEN_YIL_MİN_SIRALAMA'])
            else:
                Lastscore = SubElement(Item, 'last_min_score');Lastscore.text = new['GEÇEN_YIL_MİN_PUAN']
                if new['GEÇEN_YIL_MİN_SIRALAMA']=='' or new['GEÇEN_YIL_MİN_SIRALAMA']=='-' : Lastscore.set('order','0')
                else: Lastscore.set('order',new['GEÇEN_YIL_MİN_SIRALAMA'])
            Grant = SubElement(Item, 'grant')
            if new['BURS'] != '' : Grant.text = new['BURS']
            # final of each item.
            #updating cursor:
            cursor = dictList.index(new)
    # Transforming  root element to string object.
    mydata = ET.tostring(Root,encoding='utf-8')
    ovv = xml.dom.minidom.parseString(mydata)
    mydatas = ovv.toprettyxml(encoding='utf-8')  # minidom for pretty printing.
    myfile = open(DESTINATION_FILE,'wb')
    myfile.write(mydatas)
    myfile.close()

#******************************************************  END OF CSV TO XML


# XML TO CSV CONVERTION :
def XMLtoCSV():
    #opening the xml file and parsing it:
    xmlp = ET.XMLParser(encoding='utf-8')
    try:
        f = ET.parse(SOURCE_FILE,parser=xmlp)
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)

    root = f.getroot()
    newCsv = open(DESTINATION_FILE,'w',encoding='utf-8')
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
                #storing all item subelements and attributes with conditions:

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
                    #printing all values to csv file.
                    newCsv.write(period)
                    newCsv.write(field)
                    newCsv.write(quota)
                    newCsv.write(spec)
                    newCsv.write(order)
                    newCsv.write(lastMin)
                    newCsv.write('\n')
    newCsv.close()

#******************************************************  END OF XML TO CSV


#CSV TO JSON CONVERTION:
def CSVtoJSON():
    readCSV()
    ov = open(DESTINATION_FILE,'wb')
    cursor = -1
    universityList = []
    while cursor < len(dictList) -1:
        currentUni = dictList[cursor + 1]['ÜNİVERSİTE']
        currentType = dictList[cursor + 1]['ÜNİVERSİTE_TÜRÜ']
        cond = (x for x in dictList if x['ÜNİVERSİTE'] == currentUni)
        itemList = []

        for dictOne in cond:
            #controlling csv empty columns:
            if dictOne['DİL'] == "":dictOne['DİL'] = 'tr'
            else: dictOne['DİL'] = 'en'
            if dictOne['ÖĞRENİM_TÜRÜ'] == "":dictOne['ÖĞRENİM_TÜRÜ']='No';
            else:dictOne['ÖĞRENİM_TÜRÜ']='Yes'
            if dictOne['OKUL_BİRİNCİSİ_KONTENJANI'] == "":dictOne['OKUL_BİRİNCİSİ_KONTENJANI'] = '0'
            if dictOne['GEÇEN_YIL_MİN_SIRALAMA'] == "":dictOne['GEÇEN_YIL_MİN_SIRALAMA'] = '0'
            if dictOne['GEÇEN_YIL_MİN_PUAN'] == "" or dictOne['GEÇEN_YIL_MİN_PUAN'] == "-":dictOne['GEÇEN_YIL_MİN_PUAN'] = '0'
            if dictOne['BURS'] == "": dictOne['BURS'] = None;
            ####



            # dictioanries for subelements:
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
            # !!!!   merging all sub dictionaries
            merged = {**name, **period, **quota,**field,**last_min_score,**grandDict}
            # !!!! and merging again with item dictionary
            item = {**item,**merged}
            # apend to item list:
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
    #dumping dicitonary:
    json_string = json.dumps(departments, indent=4, ensure_ascii=False).encode('utf8')
    ov.write(json_string)

#******************************************************  END OF CSV TO JSON


#JSON TO CSV CONVERTION:

def JSONtoCSV():
    #opening json file:
    try:
        newOv = open(SOURCE_FILE,encoding='utf-8')
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)
    newCsv = open(DESTINATION_FILE, 'w', encoding='utf-8')


    data = json.load(newOv)
    newCsv.write('ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n')
    university = data['departments']['university']

    #printing all keys and values to csv file.
    for uni in university:
        for item in uni['item']:
            #controlling empty csv columns:
            if item['name']['@lang'] == 'en' : item['name']['@lang'] = 'İngilizce'
            else:item['name']['@lang'] = ''
            if item['name']['@second'] == 'Yes' : item['name']['@lang'] = 'İkinci Öğretim'
            else:item['name']['@second'] = ''
            if item['quota']['@spec'] == '0':item['quota']['@spec'] = ''
            if item['last_min_score']['@order'] == '0':item['last_min_score']['@order'] = ''
            if item['last_min_score']['#text'] == '0' :item['last_min_score']['#text'] = ''
            if item['grant'] is None : item['grant'] = ''
            ####

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


#******************************************************  END OF JSON TO CSV


#JSON TO XML CONVERTION:

def JSONtoXML():

    #opening json file
    try:
        newJs = open(SOURCE_FILE,encoding='utf-8')
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)

    #loading json and traversing it:
    data = json.load(newJs)
    Root = Element('departments')
    university = data['departments']['university']
    for uni in university:
        University = SubElement(Root,'university',name = uni['@name'],uType=uni['@uType'])
        for item in uni['item']:

            #adding subelements.
            Item = SubElement(University, 'item', id=item['@id'], faculty=item['@faculty'])
            Name = SubElement(Item, 'name',lang=item['name']['@lang'],second=item['name']['@second']);Name.text = item['name']['#text']
            Period = SubElement(Item, 'period');Period.text = item['period']
            Quota = SubElement(Item, 'quota',spec=item['quota']['@spec']);Quota.text = item['quota']['#text']
            Field = SubElement(Item, 'field');Field.text = item['field']
            Lastscore = SubElement(Item, 'last_min_score', order=item['last_min_score']['@order']);Lastscore.text = item['last_min_score']['#text']
            Grant = SubElement(Item, 'grant');Grant.text = item['grant']

    # Transforming  root element to string object.
    mydata = ET.tostring(Root,encoding='utf-8')
    ovv = xml.dom.minidom.parseString(mydata)  #minidom for pretty printing.
    mydatas = ovv.toprettyxml(encoding='utf-8')
    myfile = open(DESTINATION_FILE,'wb')
    myfile.write(mydatas)
    myfile.close()


#******************************************************  END OF JSON TO XML


#XML TO JSON CONVERTOR:

def XMLtoJSON():

    #opening xml file and parsing it:
    xmlp = ET.XMLParser(encoding='utf-8')
    try:
        f = ET.parse(SOURCE_FILE,parser=xmlp)
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)

    ## getting root and empt dictionaries to fill in loop:
    root = f.getroot()
    universityList = []
    name = {}
    period ={}
    quota = {}
    field={}
    last_min_score = {}
    grandDict = {}

    # traversing xml to reaching all elements and filling dictionaries:
    for child in root:
        itemList = []
        for elem in child:
            item = {
                '@faculty':elem.get('faculty'),
                '@id':elem.get('id')
            }
            for subElem in elem:
                if subElem.tag == 'name':
                    name = {
                        'name': {
                            '@lang': subElem.get('lang'),
                            '@second': subElem.get('second'),
                            '#text': subElem.text
                        }
                    }
                elif subElem.tag == 'period':
                    period = {
                        'period': subElem.text
                    }
                elif subElem.tag == 'quota':
                    quota = {
                        'quota': {
                            '@spec': subElem.get('spec'),
                            '#text': subElem.text
                        }
                    }
                elif subElem.tag == 'field':
                    field = {
                        'field': subElem.text
                    }
                elif subElem.tag == 'last_min_score':
                    last_min_score = {
                        'last_min_score': {
                            '@order': subElem.get('order'),
                            '#text':  subElem.text
                        }
                    }
                elif subElem.tag == 'grant':
                    grandDict = {
                        'grant': subElem.text,
                    }
            # !!!!   merging all sub dictionaries
            merged = {**name, **period, **quota,**field,**last_min_score,**grandDict}
            # !!!! and merging again with item dictionary
            item = {**item,**merged}
            # apend to item list:
            itemList.append(item)
        university = {

                '@name': child.get('name'),
                '@uType': child.get('uType'),
                'item': itemList
        }
        universityList.append(university)
    departments ={
        'departments':{
            'university':universityList
        }
    }

    # dumping json to string
    json_string = json.dumps(departments, indent=4, ensure_ascii=False).encode('utf8')
    ov = open(DESTINATION_FILE, 'wb')
    ov.write(json_string)

#******************************************************  END OF XML TO JSON


# XML VALIDATION :

def ValidateXML():

    #opening and parsing xml file:
    xmlp = ET.XMLParser(encoding='utf-8')
    try:
        f = ET.parse(SOURCE_FILE,parser=xmlp)
    except IOError:
        print('Source file is undetermined. Please check the input file name')
        sys.exit(0)
    root = f.getroot()

    #opening xsd file:
    try:
        xmlschema_doc = etree.parse(DESTINATION_FILE)
    except IOError:
        print('Xsd file is undetermined. Please check the input file name')
        sys.exit(0)

    #validation part with lxml module:
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(ET.tostring(root, encoding='utf-8'))
    validation_result = xmlschema.validate(doc)
    if validation_result:
        print('Validation is SUCCESSFULL.')
    else:
        print('Validation is UNSUCCESFULL !!!.')


# running main method.
if __name__ == "__main__":
    main()




