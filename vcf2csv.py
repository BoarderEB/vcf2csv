# https://github.com/BoarderEB/
# GPLv2+
# V: 0.01-Alpha

from os import replace
import re
import csv
import sys
import os.path
import io

InFile = ''
OutFile = ''
Log = "false" #true / false
AddPhotoToCsv = "false" #true / false
TelNoTyp = "false"
MustHaveUid = "false"
Encoding = "UTF-8"

for Index, Arg in enumerate(sys.argv):
    
    ## Get InFile -i
    if Arg == '-i':
        ArgNext = Index + 1
        InFile = sys.argv[ArgNext]
    ##Get OutFile -o 
    if Arg == '-o':
        ArgNext = Index + 1
        OutFile = sys.argv[ArgNext]

    if Arg == '-e':
        ArgNext = Index + 1
        Encoding = sys.argv[ArgNext]

    ## Log to STDOUT -l
    ArgTest = re.match("^-[a-zA-Z]{0,}l", Arg)
    if ArgTest:
        Log = "true"
    ## Add Photo to CSV
    ArgTest = re.match("^-[a-zA-Z]{0,}p", Arg)
    if ArgTest:
        AddPhotoToCsv = "true"
    ##TelNoTyp
    ArgTest = re.match("^--[tT][eE][ll][nN][oO][tT][yY][pP]", Arg)
    if ArgTest:
        TelNoTyp = "true"
    ##MustHaveUid
    ArgTest = re.match("^--[mM][uU][sS][tT][hH][aA][vV][eE][uU][iI][dD]", Arg)
    if ArgTest:
        MustHaveUid = "true"




if InFile == '':
    print("Error: No Infile \"-i file.vcf\" is specified")
    exit(1)

if os.path.isfile(InFile) != True:
    print("Error: Infile -", InFile ,"- don't exist")
    exit(1)
    
if OutFile == '':
    print("Error: No Outfile \"-o file.csv\" is specified" )
    exit(1)

## init-variablen and Arrays
count = 0 # VCard-Count
VCard = [] #VCard as array

fieldnames = [
    'Name',
    'GivenNames',
    'AdditionalNames',
    'Prefixes','Suffixes',
    'Organisation',
    'Unit',
    'Title',
    'PostOfficeBox',
    'ExtendedAddress',
    'Street',
    'City',
    'Region',
    'PostalCode',
    'Country',
    'PostOfficeBoxWork',
    'ExtendedAddressWork',
    'StreetWork',
    'CityWork',
    'RegionWork',
    'PostalCodeWork',
    'CountryWork',
    'PostOfficeBoxHome',
    'ExtendedAddressHome',
    'StreetHome',
    'CityHome',
    'RegionHome',
    'PostalCodeHome',
    'CountryHome',
    'EmailWork',
    'EmailHome',
    'Email0',
    'Email1',
    'Email2',
    'EmailPref',
    'Note',
    'Uid'
    ]

if TelNoTyp == 'true':
    fieldnames.append('Tel0')
    fieldnames.append('Tel1')
    fieldnames.append('Tel2')
    fieldnames.append('TelFax')
else:
    fieldnames.append('TelTextWork')
    fieldnames.append('TelVoiceWork')
    fieldnames.append('TelFaxWork')
    fieldnames.append('TelCellWork')
    fieldnames.append('TelVideoWork')
    fieldnames.append('TelPagerWork')
    fieldnames.append('TelTextphoneWork')
    fieldnames.append('TelTextHome')
    fieldnames.append('TelVoiceHome')
    fieldnames.append('TelFaxHome')
    fieldnames.append('TelCellHome')
    fieldnames.append('TelVideoHome')
    fieldnames.append('TelPagerHome')
    fieldnames.append('TelTextphoneHome')
    fieldnames.append('TelText0')
    fieldnames.append('TelVoice0')
    fieldnames.append('TelFax0')
    fieldnames.append('TelCell0')
    fieldnames.append('TelVideo0')
    fieldnames.append('TelPager0')
    fieldnames.append('TelTextphone0')
    fieldnames.append('TelText1')
    fieldnames.append('TelVoice1')
    fieldnames.append('TelFax1')
    fieldnames.append('TelCell1')
    fieldnames.append('TelVideo1')
    fieldnames.append('TelPager1')
    fieldnames.append('TelTextphone1')
    fieldnames.append('TelText2')
    fieldnames.append('TelVoice2')
    fieldnames.append('TelFax2')
    fieldnames.append('TelCell2')
    fieldnames.append('TelVideo2')
    fieldnames.append('TelPager2')
    fieldnames.append('TelTextphone2')
    fieldnames.append('TelText3')
    fieldnames.append('TelVoice3')
    fieldnames.append('TelFax3')
    fieldnames.append('TelCell3')
    fieldnames.append('TelVideo3')
    fieldnames.append('TelPager3')
    fieldnames.append('TelTextphone3')

if AddPhotoToCsv == 'true':
    fieldnames.append('Photo')

## write header of csv-file
with open(OutFile, 'w', newline='', encoding=Encoding) as csvfile:   
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

## write Vcard-Lins of csv-file
def WriteVcard2Csv():
    with open(OutFile, 'a', newline='', encoding=Encoding) as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        ToWrite = []
        for i in fieldnames:                   
            #print(globals()[i])
            ToWrite.append(globals()[i])
        writer.writerow(ToWrite)


## read vcf-file
with io.open(InFile, mode="r", encoding=Encoding) as file:
    for Line in file:
        CurLine = Line.rstrip()
   
        ## Add line of vcf-file to VCard-Array
        CurLineStartWhiteSpace = re.match("^\s", CurLine)
        if CurLineStartWhiteSpace:
            Last = len(VCard)
            Last = Last - 1
            CurLine = re.sub(r"^\s",'',CurLine)
            VCard[Last] = "".join((VCard[Last],CurLine))
        else:   
            VCard.append(CurLine)

        ## End of VCard in vcf-file 
        CurLineEndVcard = re.match("[eE][nN][dD][:][vV][cC][aA][rR][dD]", CurLine)
        if CurLineEndVcard:

            ## Init. empty strings, so that the string is available during export. Even if the line is not in the VCard. 

            ## Init. empty strings form fieldnames[] so that the string is available during export.
            for i in fieldnames:
                str = i
                globals()[str] = ''

            EmailPrefInt = 1000 #init - max in rfc6350 is 100 - so we init it at 1000 that it is ever the lowest preferenz

            ## Start Export new VCard
            for Index, CurLine in enumerate(VCard):

                ### VCard Uid
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.6

                IsVcardUid = re.match("^[uU][iI][dD].{0,}[:]", CurLine)
                if IsVcardUid:
                    UidSuf = re.sub(r'^[uU][iI][dD].{0,}[:]','',CurLine)
                    UidPre = CurLine.replace(UidSuf,'')
                    Uid = UidSuf

                    if Log == 'true':
                        print('Uid: ', Uid)

                ### VCard Note
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2

                IsVcardNote = re.match("^[nN][oO][tT][eE][:]|^[nN][oO][tT][eE][;].{0,}[:]", CurLine)
                if IsVcardNote:
                    Note = CurLine.split(':',1)
                    NotePre = Note[0]
                    NoteSuf = Note[1]
                    #replace \n with working \n (next-line)
                    Note = re.sub(r'\\n','\n',NoteSuf)
                    Note = Note.strip()
                    #remove "\" befor spezial char
                    Note = re.sub(r'\\\,',',',Note)
                    Note = re.sub(r'\\\;',';',Note)
                    Note = re.sub(r'\\\:',':',Note)
                    Note = Note
                    
                    if Log == 'true':
                        print('Note: ',Note)
                

                ### VCard Photo
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.4

                IsVcardPhoto = re.match("^[pP][hH][oO][tT][oO][:]|^[pP][hH][oO][tT][oO][;].{0,}[:]", CurLine)
                if IsVcardPhoto:

                    IsVcardPhotoBase64 = re.match(".*[bB][aA][sS][eE]64|.*[eE][nN][cC][oO][dD][iI][nN][gG]=[bB]", CurLine)
                    if IsVcardPhotoBase64:
                        Photo = re.sub('^.*[,;:]', '', CurLine)

                    IsVcardPhotoUrl = re.match(".*[hH][tT][tT][pP][sS]{0,1}:\/\/", CurLine)
                    if IsVcardPhotoUrl:
                        #get string from https(s)
                        Photo = re.sub('[hH][tT][tT][pP][sS]{0,1}:\/\/.*', '', CurLine)
                        Photo = re.sub(Photo, '', CurLine)
                        ## remove all after url
                        Photo = re.split(r';',Photo)
                        Photo = Photo[0]

                    if Log == 'true':
                        print('Photo: ', Photo)

            
                ### Vcard Tel
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
                
                IsVcardTel = re.match("^[tT][eE][lL][:]|^[tT][eE][lL][;].{0,}[:]", CurLine)
                if IsVcardTel: 
                    Tel = re.split(r'(?<!\\)(?:\\\\)*:',CurLine)
                    TelPre = Tel[0]
                    TelSuf = len(Tel)
                    TelSuf = Tel[TelSuf-1]
                    TelSuf = re.split(r'(?<!\\)(?:\\\\)*;',TelSuf)
                    if len(TelSuf) > 1:
                        ## Durchwahl von Extern
                        TelExt = TelSuf[1]
                        ## TelNumber
                        TelSuf = TelSuf[0]
                    else:
                        TelSuf = TelSuf[0]

                    ##Type (Work,Home)
                    IsVcardTelWork = re.match(".*[tT][yY][pP][eE][=].*[wW][oO][rR][kK]\W|.*[tT][yY][pP][eE][=].*[wW][oO][rR][kK]$", TelPre)
                    IsVcardTelHome = re.match(".*[tT][yY][pP][eE][=].*[hH][oO][mM][eE]\W|.*[tT][yY][pP][eE][=].*[hH][oO][mM][eE]$", TelPre)
                    
                    #Type: (text,voice,fax,cell,video,pager,textphone)
                    IsVcardTelText = re.match(".*[tT][yY][pP][eE][=].*[tT][eE][xX][tT]\W|.*[tT][yY][pP][eE][=].*[tT][eE][xX][tT]$", TelPre)
                    IsVcardTelVoice = re.match(".*[tT][yY][pP][eE][=].*[vV][oO][iI][cC][eE]\W|.*[tT][yY][pP][eE][=].*[vV][oO][iI][cC][eE]$", TelPre)
                    IsVcardTelFax = re.match(".*[tT][yY][pP][eE][=].*[fF][aA][xX]\W|.*[tT][yY][pP][eE][=].*[fF][aA][xX]$", TelPre)
                    IsVcardTelCell = re.match(".*[tT][yY][pP][eE][=].*[cC][eE][lL][lL]\W|.*[tT][yY][pP][eE][=].*[cC][eE][lL][lL]$", TelPre)
                    IsVcardTelVideo = re.match(".*[tT][yY][pP][eE][=].*[vV][iI][dD][eE][oO]\W|.*[tT][yY][pP][eE][=].*[vV][iI][dD][eE][oO]$", TelPre)
                    IsVcardTelPager = re.match(".*[tT][yY][pP][eE][=].*[pP][aA][gG][eE][rR]\W|.*[tT][yY][pP][eE][=].*[pP][aA][gG][eE][rR]$", TelPre)
                    IsVcardTelTextphone = re.match(".*[tT][yY][pP][eE][=].*[tT][eE][xX][tT][pP][hH][oO][nN][eE]\W|.*[tT][yY][pP][eE][=].*[tT][eE][xX][tT][pP][hH][oO][nN][eE]$", TelPre)

                    if TelNoTyp == 'true':
                        if IsVcardTelFax:
                            TelFax = TelSuf
                        elif Tel0 == '':
                            Tel0 = TelSuf
                        elif Tel1 == '':
                            Tel1 = TelSuf
                        elif Tel2 == '':
                            Tel2 = TelSuf
                        else:
                            Tel2 = "".join((Tel2,', ',TelSuf))
                    else:                            
                        if IsVcardTelWork:
                            if IsVcardTelCell:
                                TelCellWork = TelSuf
                            elif IsVcardTelVoice:
                                TelVoiceWork = TelSuf
                            elif IsVcardTelText:
                                TelTextWork = TelSuf
                            elif IsVcardTelFax:
                                TelFaxWork = TelSuf
                            elif IsVcardTelVideo:
                                TelVideoWork = TelSuf
                            elif IsVcardTelPager:
                                TelPagerWork = TelSuf
                            elif IsVcardTelTextphone:
                                TelTextphoneWork = TelSuf
                            else:
                                TelVoiceWork = TelSuf
                        elif IsVcardTelHome:
                            if IsVcardTelCell:
                                TelCellHome = TelSuf
                            elif IsVcardTelVoice:
                                TelVoiceHome = TelSuf
                            elif IsVcardTelText:
                                TelTextHome = TelSuf
                            elif IsVcardTelFax:
                                TelFaxHome = TelSuf
                            elif IsVcardTelVideo:
                                TelVideoHome = TelSuf
                            elif IsVcardTelPager:
                                TelPagerHome = TelSuf
                            elif IsVcardTelTextphone:
                                TelTextphoneHome = TelSuf
                            else:
                                TelVoiceHome = TelSuf
                        else:
                            if IsVcardTelCell:
                                if TelCell0 == '':
                                    TelCell0 = TelSuf
                                elif TelCell1 == '':
                                    TelCell1 = TelSuf
                                elif TelCell2 == '':
                                    TelCell2 = TelSuf
                                elif TelCell3 == '':
                                    TelCell3 = TelSuf
                                else:
                                    TelCell3 = "".join((TelCell3,', ',TelSuf))

                            elif IsVcardTelVoice:
                                if TelVoice0 == '':
                                    TelVoice0 = TelSuf
                                elif TelVoice1 == '':
                                    TelVoice1 = TelSuf
                                elif TelVoice2 == '':
                                    TelVoice2 = TelSuf
                                elif TelVoice3 == '':
                                    TelVoice3 = TelSuf
                                else:
                                    TelVoice3 = "".join((TelVoice3,', ',TelSuf))
                                
                            elif IsVcardTelText:
                                if TelText0 == '':
                                    TelText0 = TelSuf
                                elif TelText1 == '':
                                    TelText1 = TelSuf
                                elif TelText2 == '':
                                    TelText2 = TelSuf
                                elif TelText3 == '':
                                    TelText3 = TelSuf
                                else:
                                    TelText3 = "".join((TelText3,', ',TelSuf))

                            elif IsVcardTelFax:
                                if TelFax0 == '':
                                    TelFax0 = TelSuf
                                elif TelFax1 == '':
                                    TelFax1 = TelSuf
                                elif TelFax2 == '':
                                    TelFax2 = TelSuf
                                elif TelFax3 == '':
                                    TelFax3 = TelSuf
                                else:
                                    TelFax3 = "".join((TelFax3,', ',TelSuf))

                            elif IsVcardTelVideo:
                                if TelVideo0 == '':
                                    TelVideo0 = TelSuf
                                elif TelVideo1 == '':
                                    TelVideo1 = TelSuf
                                elif TelVideo2 == '':
                                    TelVideo2 = TelSuf
                                elif TelVideo3 == '':
                                    TelVideo3 = TelSuf
                                else:
                                    TelVideo3 = "".join((TelVideo3,', ',TelSuf))

                            elif IsVcardTelPager:
                                if TelPager0 == '':
                                    TelPager0 = TelSuf
                                elif TelPager1 == '':
                                    TelPager1 = TelSuf
                                elif TelPager2 == '':
                                    TelPager2 = TelSuf
                                elif TelPager3 == '':
                                    TelPager3 = TelSuf
                                else:
                                    TelPager3 = "".join((TelPager3,', ',TelSuf))

                            elif IsVcardTelTextphone:
                                if TelTextphone0 == '':
                                    TelTextphone0 = TelSuf
                                elif TelTextphone1 == '':
                                    TelTextphone1 = TelSuf
                                elif TelTextphone2 == '':
                                    TelTextphone2 = TelSuf
                                elif TelTextphone3 == '':
                                    TelTextphone3 = TelSuf
                                else:
                                    TelTextphone3 = "".join((TelTextphone3,', ',TelSuf))

                            else:
                                if TelVoice0 == '':
                                    TelVoice0 = TelSuf
                                elif TelVoice1 == '':
                                    TelVoice1 = TelSuf
                                elif TelVoice2 == '':
                                    TelVoice2 = TelSuf
                                elif TelVoice3 == '':
                                    TelVoice3 = TelSuf
                                else:
                                    TelVoice3 = "".join((TelVoice3,', ',TelSuf))

                ### Vcard EMAIL
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
                
                IsVcardEmail = re.match("^[eE][mM][aA][iI][lL][:]|^[eE][mM][aA][iI][lL][;].{0,}[:]", CurLine)
                if IsVcardEmail: 
                    Email = CurLine.split(':',1)
                    EmailPre = Email[0]
                    EmailSuf = Email[1]

                    IsVcardEmailWork = re.match(".*[tT][yY][pP][eE][=].*[wW][oO][rR][kK]\W|.*[tT][yY][pP][eE][=].*[wW][oO][rR][kK]$", EmailPre)
                    IsVcardEmailHome = re.match(".*[tT][yY][pP][eE][=].*[hH][oO][mM][eE]\W|.*[tT][yY][pP][eE][=].*[hH][oO][mM][eE]$", EmailPre)
                    IsVcardEmailPref = re.match(".*[pP][rR][eE][fF]\W|.*.*[pP][rR][eE][fF]$", EmailPre)
                    
                    EmailPrefIntTest = 'false'
                    if IsVcardEmailPref:
                        EmailPrefIntTest = re.search("(?<=PREF=)[0-9]{1,3}", EmailPre)
                        if EmailPrefIntTest:
                            EmailPrefIntTest = EmailPrefIntTest.group(0)
                            EmailPrefIntTest = int(EmailPrefIntTest)
                            if EmailPrefIntTest <  EmailPrefInt:
                                EmailPrefInt = EmailPrefIntTest
                                EmailPrefIntTest = 'true'

                    if IsVcardEmailWork:
                        EmailWork = EmailSuf
                        if IsVcardEmailPref:
                            if EmailPrefIntTest:
                                EmailPref = 'EmailWork'
                            elif EmailPrefInt == 1000:
                                EmailPref = 'EmailWork'
                    elif IsVcardEmailHome:
                        EmailHome = EmailSuf
                        if IsVcardEmailPref:
                            if EmailPrefIntTest:
                                EmailPref = 'EmailHome'
                            elif EmailPrefInt == 1000:
                                EmailPref = 'EmailHome'  
                    else:
                        if Email0 == '':
                            Email0 = EmailSuf
                            if IsVcardEmailPref:
                                if EmailPrefIntTest:
                                    EmailPref = 'Email0'
                                elif EmailPrefInt == 1000:
                                    EmailPref = 'Email0'
                        elif Email1 == '':
                            Email1 = EmailSuf
                            if IsVcardEmailPref:
                                if EmailPrefIntTest:
                                    EmailPref = 'Email1'
                                elif EmailPrefInt == 1000:
                                    EmailPref = 'Email1'
                        else:
                            if Email2 == '':
                                Email2 = EmailSuf
                                if IsVcardEmailPref:
                                    if EmailPrefIntTest:
                                        EmailPref = 'Email2'
                                    elif EmailPrefInt == 1000:
                                        EmailPref = 'Email2'
                            else:
                                Email2 = "".join((Email2,', ',EmailSuf))
                                if IsVcardEmailPref:
                                    if EmailPrefIntTest:
                                        EmailPref = ''
                                    elif EmailPrefInt == 1000:
                                        EmailPref = ''
                if Log == 'true':
                    print("EmailWork: ",EmailWork,"EmailHome: ",EmailHome,"Email0: ",Email0,"Email1: ",Email1,"Email2: ",Email2, "Prefert: ",EmailPref)    

                ### Vcard Adr
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.3.1
                IsVcardAdr = re.match("^[aA][dD][rR][:]|^[aA][dD][rR][;].{0,}[:]", CurLine)
                if IsVcardAdr: 
                    Adr = CurLine.split(':',1)
                    AdrPre = Adr[0]
                    AdrSuf = Adr[1]
                    Adr = re.split(r'(?<!\\)(?:\\\\)*;',AdrSuf)

                    IsVcardAdrWork = re.match(".*[tT][yY][pP][eE][=][wW][oO][rR][kK]\W|.*[tT][yY][pP][eE][=][wW][oO][rR][kK]$", AdrPre)
                    IsVcardAdrHome = re.match(".*[tT][yY][pP][eE][=][hH][oO][mM][eE]\W|.*[tT][yY][pP][eE][=][hH][oO][mM][eE]$", AdrPre)

                    for Index,Field in enumerate(Adr):
                        Field = Field.replace('\\n',' ')
                        Field = Field.replace('\\','')
                        Adr[Index] = Field
                    
                    if IsVcardAdrWork:

                        for Index,Field in enumerate(Adr):
                            if Index == 0:
                                PostOfficeBoxWork = Field
                            if Index == 1:
                                ExtendedAddressWork = Field
                            if Index == 2:
                                StreetWork = Field
                            if Index == 3:
                                CityWork = Field
                            if Index == 4:
                                RegionWork = Field
                            if Index == 5:
                                PostalCodeWork = Field
                            if Index == 6:
                                CountryWork = Field

                    elif IsVcardAdrHome:

                        for Index,Field in enumerate(Adr):
                            if Index == 0:
                                PostOfficeBoxHome = Field
                            if Index == 1:
                                ExtendedAddressHome = Field
                            if Index == 2:
                                StreetHome = Field
                            if Index == 3:
                                CityHome = Field
                            if Index == 4:
                                RegionHome = Field
                            if Index == 5:
                                PostalCodeHome = Field
                            if Index == 6:
                                CountryHome = Field
                    else:
                        
                        for Index,Field in enumerate(Adr):
                            if Index == 0:
                                PostOfficeBox = Field
                            if Index == 1:
                                ExtendedAddress = Field
                            if Index == 2:
                                Street = Field
                            if Index == 3:
                                City = Field
                            if Index == 4:
                                Region = Field
                            if Index == 5:
                                PostalCode = Field
                            if Index == 6:
                                Country = Field

                    if Log == 'true':
                        print('ADR-Work!: ','PostOfficeBox: ',PostOfficeBoxWork, 'ExtendedAddress: ', ExtendedAddressWork, 'Street: ',StreetWork, 'City: ',CityWork, 'Region: ',RegionWork, 'PostalCode: ',PostalCodeWork, 'Country: ',CountryWork)
                        print('ADR-Home!: ','PostOfficeBox: ',PostOfficeBoxHome, 'ExtendedAddress: ', ExtendedAddressHome, 'Street: ',StreetHome, 'City: ',CityHome, 'Region: ',RegionHome, 'PostalCode: ',PostalCodeHome, 'Country: ',CountryHome)
                        print('ADR!: ','PostOfficeBox: ',PostOfficeBox, 'ExtendedAddress: ', ExtendedAddress, 'Street: ',Street, 'City: ',City, 'Region: ',Region, 'PostalCode: ',PostalCode, 'Country: ',Country)

                ### Vcard N
                ### Referenz: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2
                IsVcardN = re.match("^[nN][:]|^[nN][;].{0,}[:]", CurLine)
                if IsVcardN:
                    N = CurLine.split(':',1)
                    NPre = N[0]
                    NSuf = N[1]
                    N = re.split(r'(?<!\\)(?:\\\\)*;',NSuf)
                    

                    for Index, Field in enumerate(N):
                        #Famalie Names / Nachnahme
                        if Index == 0:
                            Name = N[0].replace('\\','')
                        if Index == 1:
                            #Given Names / Vorname(n)
                            GivenNames = N[1].replace('\\','')
                        if Index == 2:
                            #Additional Names / Weitere Namen
                            AdditionalNames = N[2].replace('\\','')
                        if Index == 3:
                            #Prefixes / Vor dem Namen wie Dr. Dipl. Frau Herr usw.
                            Prefixes = N[3].replace('\\','')
                        if Index == 4:
                            #Suffixes / Nach dem Namen
                            Suffixes = N[4].replace('\\','')

                    if Log == 'true':
                        print("Name: ",Name, " GivenNames: ",GivenNames," AdditionalNames: ",AdditionalNames," Prefixes: ",Prefixes," Suffixes: ",Suffixes)

                ### Vcard Org
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.4
                IsVcardOrg = re.match("^[oO][rR][gG][:]|^[oO][rR][gG][;].{0,}[:]", CurLine)
                if IsVcardOrg: 
                    Org = CurLine.split(':',1)
                    OrgPre = Org[0]
                    OrgSuf = Org[1]
                    Org = re.split(r'(?<!\\)(?:\\\\)*;',OrgSuf)

                    Unit = ''
                    if len(Org) > 1:
                        for Index, Uni in enumerate(Org):
                            if Index > 0:
                                Uni = Uni.replace('\\','')
                                if Index == 1:
                                    Unit = Uni
                                else:
                                    Unit = "".join((Unit,', ',Uni))

                    #Organisation / Firma
                    Organisation = Org[0].replace('\\','')
                    #Organization Unit / Abteilung
                    Unit = Unit.strip()
                    
                    if Log == 'true':
                        print('Organisation: ',Organisation,'Abteilung: ',Unit)

                ### Vcard TITLE
                ### https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.1
                IsVcardTitle = re.match("^[tT][iI][tT][lL][eE][:]|^[tT][iI][tT][lL][eE][;].{0,}[:]", CurLine)
                if IsVcardTitle: 
                    Title = CurLine.split(':',1)
                    
                    #Title / Postion in einer Firma
                    Title = Title[1].replace('\\','')

                    if Log == 'true':  
                        print(Title)

            if Log == 'true':    
                if TelNoTyp == 'true':
                    print("Tel0:", Tel0,"Tel1: ",Tel1,"Tel2: ",Tel2,"TelFax: ",TelFax)
                    fieldnames.append('Tel0')
                    fieldnames.append('Tel1')
                    fieldnames.append('Tel2')
                    fieldnames.append('TelFax')
                else:
                    print("TelTextWork:", TelTextWork,"TelVoiceWork: ",TelVoiceWork,"TelFaxWork: ",TelFaxWork,"TelCellWork: ",TelCellWork,"TelVideoWork: ",TelVideoWork,"TelPagerWork: ",TelPagerWork,"TelTextphoneWork: ",TelTextphoneWork)
                    print("TelTextHome:", TelTextHome,"TelVoiceHome: ",TelVoiceHome,"TelFaxHome: ",TelFaxHome,"TelCellHome: ",TelCellHome,"TelVideoHome: ",TelVideoHome,"TelPagerHome: ",TelPagerHome,"TelTextphoneHome: ",TelTextphoneHome)
                    print("TelText0:", TelText0,"TelVoice0: ",TelVoice0,"TelFax0: ",TelFax0,"TelCell0: ",TelCell0,"TelVideo0: ",TelVideo0,"TelPager0: ",TelPager0,"TelTextphone0: ",TelTextphone0)
                    print("TelText1:", TelText1,"TelVoice1: ",TelVoice1,"TelFax1: ",TelFax1,"TelCell1: ",TelCell1,"TelVideo1: ",TelVideo1,"TelPager1: ",TelPager1,"TelTextphone1: ",TelTextphone1)
                    print("TelText2:", TelText2,"TelVoice2: ",TelVoice2,"TelFax2: ",TelFax2,"TelCell2: ",TelCell2,"TelVideo2: ",TelVideo2,"TelPager2: ",TelPager2,"TelTextphone2: ",TelTextphone2)
                    print("TelText3:", TelText3,"TelVoice3: ",TelVoice3,"TelFax3: ",TelFax3,"TelCell3: ",TelCell3,"TelVideo3: ",TelVideo3,"TelPager3: ",TelPager3,"TelTextphone3: ",TelTextphone3)

            if MustHaveUid == 'true':
                if Uid != '':
                    WriteVcard2Csv()
                    if Log == 'true':
                        print('Write Vcard to CSV')
                else:
                    if Log == 'true':
                        print('Don\'t write Vcard to CSV - there is no Uid')
            else:
                WriteVcard2Csv()
                if Log == 'true':
                        print('Write Vcard to CSV')


            if Log == 'true':
                count += 1
                print("End-VCard-Num: ",count)

            EmailPrefInt = 1000 #clear for new VCard - max in rfc6350 is 100          
            VCard = [] #clear VCard-Array for the next VCard

exit(0)