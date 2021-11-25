# vcf2csv - convert vcf to csv file
The converter is based on VCard version 4 [RFC6350](https://datatracker.ietf.org/doc/html/rfc6350) - but also works with version 3 

## Start the Script

```python3 vcf2csv.py -l -p -i vards.vcf -o contacts.csv```

Options: 

```
-i = Specified the Infile like -i vards.vcf
-o = Specified the Outfile like -o contacts.csv
-l = logs go to stdout 
-p = Add Photos to csv from vcf.
```

## Currently this data is being converted: 

### N:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2

|Name|GivenNames|AdditionalNames|Prefixes|Suffixes|
|----|----------|---------------|--------|--------|

### PHOTO:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.4

Is Base64-Encodet-Img or a URL

|Photo|
|-----|

### ADR:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.3.1

|PostOfficeBox|PostOfficeBoxWork|PostOfficeBoxHome|
|-----|-----|-----|

|ExtendedAddress|ExtendedAddressWork|ExtendedAddressHome|
|-----|-----|-----|

|Street|StreetWork|StreetHome|
|-----|-----|-----|

|City|CityWork|CityHome|
|-----|-----|-----|

|Region|RegionWork|RegionHome|
|-----|-----|-----|

|PostalCode|PostalCodeWork|PostalCodeHome|
|-----|-----|-----|

|Country|CountryWork|CountryHome|
|-----|-----|-----|

### TEL:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1

#### CSV-Header:

|TelVoiceWork|TelVoiceHome|TelVoice0|TelVoice1|TelVoice2|TelVoice3|
|-----|-----|-----|-----|-----|-----|

|TelFaxWork|TelFaxHome|TelFax0|TelFax1|TelFax2|TelFax3|
|-----|-----|-----|-----|-----|-----|

|TelCellWork|TelCellHome|TelCell0|TelCell1|TelCell2|TelCell3|
|-----|-----|-----|-----|-----|-----|

|TelTextWork|TelTextHome|TelText0|TelText1|TelText2|TelText3|
|-----|-----|-----|-----|-----|-----|

|TelVideoHome|TelVideoHome|TelVideo0|TelVideo1|TelVideo2|TelVideo3|
|-----|-----|-----|-----|-----|-----|

|TelPagerWork|TelPagerHome|TelPager0|TelPager1|TelPager2|TelPager3|
|-----|-----|-----|-----|-----|-----|

|TelTextphoneWork|TelTextphoneHome|TelTextphone0|TelTextphone1|TelTextphone2|TelTextphone3|
|-----|-----|-----|-----|-----|-----|

### EMAIL:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2

|EmailWork|EmailWork|EmailHome|Email0|Email1|Email2|EmailPref|
|-----|-----|-----|-----|-----|-----|-----|

In the RFC each email address can have a preference. Only the Email with the heigest preference is linkt in the field "EmailPref"

### TITLE:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.1

|Title|
|-----|

### ORG:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.4

|Organisation|Unit|
|------------|----|

### NOTE:
https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2

|Note|
|----|

## Type:
https://datatracker.ietf.org/doc/html/rfc6350#section-5.6

In the RFC6350 is Type 

1. Work
2. Home
3. None = Work and Home
4. Individual
5. Individual
6. ...

To create predictability for a database query is converted differently from the RCF

## Adr:

1. AdrWork
2. AdrHome
3. AdrNone = None or Individual (if there are several - overwritten by the last)

## Tel:

1. TelWork
2. TelHome
3. Tel0 = None or Individual 
4. Tel1 = None or Individual 
5. Tel2 = None or Individual 
6. Tel3 = None or Individual (if there are more of None or Individual - they addet separetet by commy in this this)


## Email:

1. EmailWork
2. EmailHome
3. Email0
4. Email1
5. Email2 (if there are more of None or Individual - they addet separetet by commy in this this)