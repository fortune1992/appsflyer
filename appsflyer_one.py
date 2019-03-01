# -*- coding: utf-8 -*-

import csv
import os
import re
import urllib2
import datetime
import numpy
import collections

Tier1 = ['US']
Tier2 = ['NZ', 'AU','CA','JP']
Tier3 = ['DE', 'FR', 'GB', 'CH', 'LU']
Tier4 = ['CN', 'ZA', 'HK', 'SG', 'TW', 'SA', 'RU', 'PA', 'NL', 'IT', 'IL', 'ES', 'CR', 'BR', 'AE', 'AT', 'BE', 'GT', 'KE', 'MO', 'SK', 'TT', 'KR']
Tier5 = ['CL', 'KW', 'AR', 'CO', 'MX', 'PE', 'UA', 'EC', 'DO', 'KZ', 'MA', 'MY', 'ID', 'TH', 'BH', 'BY', 'HN', 'JM', 'MD', 'OM', 'PY', 'SV']
Tier6 = ['BO', 'JO', 'KG', 'LB', 'PH', 'UZ']
Tier7 = ['DZ', 'IQ', 'NP', 'TN', 'VE', 'YE', 'TR', 'VN', 'PK', 'EG']
Tier8 = ['IN']

Apps = collections.OrderedDict([('Space_A', 'com.oneapp.max.cleaner.booster')])

TierDataHeader = []

TierType = ['Tier1', 'Tier2', 'Tier3', 'Tier4', 'Tier5', 'Tier6', 'Tier7', 'Tier8']

def getTierDataHeader():
    for key in Apps: 
        TierDataHeader.append(key + '_DNU_All')
        TierDataHeader.append(key + '_DNU_Organic')
        TierDataHeader.append(key + '_DNU_Facebook')
        TierDataHeader.append(key + '_DNU_Adw')
        TierDataHeader.append(key + '_Ovalue')
        TierDataHeader.append(key + '_Retention_All')
        TierDataHeader.append(key + '_Retention_Organic')
        TierDataHeader.append(key + '_Retention_NonOrganic')
        TierDataHeader.append(key + '_Retention_Facebook')
        TierDataHeader.append(key + '_Retention_Adw')
    return TierDataHeader

def createTierDataFile(fileName, tierData):
     with open(tierFileName, "wb") as tierFile:
        writer = csv.writer(tierFile)
        TierDataHeader.insert(0, '')
        writer.writerow(TierDataHeader)
        for j in range(tierData.shape[0]):
            temp = tierData[j].tolist()
            temp.insert(0, 'Tier%d' % (j + 1))
            writer.writerow(temp)
        tierFile.close()

def createAppDataFile(fileName, dataArray):
    with open(fileName, 'wb') as dataFile:
        writer = csv.writer(dataFile)
        header = ['country', 'organic','non-organic', 'o-value', 'total']
        writer.writerow(header)
        for i in range(len(dataArray)):
            countryInfo = dataArray[i]
            if ((countryInfo[0] in TierType) or (countryInfo[0] == 'other')):
                continue
            row = []
            row.append(countryInfo[0])
            countInfo = countryInfo[1]
            row.append(countInfo['organic'])
            row.append(countInfo['non-organic'])
            if (countInfo['non-organic'] == 0):
                row.append(-1)
            else:
                row.append(format(float(countInfo['organic']) / float(countInfo['non-organic']), '.2f'))
            row.append(countInfo['total'])
            writer.writerow(row)
    dataFile.close()

def analyzeTierData(item, result):

    if result.has_key(item[0]):
        count = result[item[0]]
    else:
        count = {}
        count['organic'] = 0L
        count['non-organic'] = 0L
        count['total'] = 0L
        count['retention'] = 0L

    if (item[1] == "Organic"):
        count['organic'] += long(item[2])
    else:
        count['non-organic'] += long(item[2])
    count['total'] += long(item[2])
    count['retention'] += long(item[3])
    
    tierType = ''
    tierMedia = []

    # organic_install organic_retention facebook_ads_install facebook_ads_retention googleadwords_int_install googleadwords_int_retention nonorganic_install nonorganic_retention
    if item[0] in Tier1:
        tierType = TierType[0]
        if result.has_key(TierType[0]):
            tierMedia = result[TierType[0]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])
            
            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier2:
        tierType = TierType[1]
        if result.has_key(TierType[1]):
            tierMedia = result[TierType[1]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier3:
        tierType = TierType[2]
        if result.has_key(TierType[2]):
            tierMedia = result[TierType[2]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier4:
        tierType = TierType[3]
        if result.has_key(TierType[3]):
            tierMedia = result[TierType[3]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier5:
        tierType = TierType[4]
        if result.has_key(TierType[4]):
            tierMedia = result[TierType[4]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier6:
        tierType = TierType[5]
        if result.has_key(TierType[5]):
            tierMedia = result[TierType[5]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier7:
        tierType = TierType[6]
        if result.has_key(TierType[6]):
            tierMedia = result[TierType[6]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])

    elif item[0] in Tier8:
        tierType = TierType[7]
        if result.has_key(TierType[7]):
            tierMedia = result[TierType[7]]
        else:
            tierMedia = [0] * 8

        if (item[1] == "Organic"):
            tierMedia[0] += long(item[2])
            tierMedia[1] += long(item[3])

        else:
            if (item[1] == 'Facebook Ads'):
                tierMedia[2] += long(item[2])
                tierMedia[3] += long(item[3])

            elif (item[1] == 'googleadwords_int'):
                tierMedia[4] += long(item[2])
                tierMedia[5] += long(item[3])

            tierMedia[6] += long(item[2])
            tierMedia[7] += long(item[3])
    else:
        tierType = 'other'
        tierMedia = [0] * 8

    return count, tierType, tierMedia

def analyzeCsvDataFile(fileName):
    csvFile = open(fileName, "rb")
    csvFile.readline() #skip firt line
    reader = csv.reader(csvFile)
    result = {}
    for item in reader:
        count, tierType, tierMedia = analyzeTierData(item, result)
        result[item[0]] = count
        result[tierType] = tierMedia

    sortedResult = sorted(result.items(), key=lambda x:x[0], reverse=False)

    ###  按渠道分Tier计算数据  ###
    organic_retention = [0] * len(TierType)
    organic_install = [0] * len(TierType)
    facebook_ads_retention = [0] * len(TierType)
    facebook_ads_install = [0] * len(TierType)
    google_ad_retention = [0] * len(TierType)
    google_ad_install = [0] * len(TierType)
    nonorganic_retention = [0] * len(TierType)

# organic_install organic_retention facebook_ads_install facebook_ads_retention googleadwords_int_install googleadwords_int_retention nonorganic_install nonorganic_retention
    for i in range(len(TierType)):
        if (result[TierType[i]][0]):
            organic_install[i] += result[TierType[i]][0]
            organic_retention[i] = format(float(result[TierType[i]][1]) / float(result[TierType[i]][0]), '.4f')
            

        if (result[TierType[i]][2]):
            facebook_ads_install[i] += result[TierType[i]][2]
            facebook_ads_retention[i] = format(float(result[TierType[i]][3]) / float(result[TierType[i]][2]), '.4f') 

        if (result[TierType[i]][4]):
            google_ad_install[i] += result[TierType[i]][4]
            google_ad_retention[i] = format(float(result[TierType[i]][5]) / float(result[TierType[i]][4]), '.4f') 

        if (result[TierType[i]][6]):
            nonorganic_retention[i] = format(float(result[TierType[i]][7]) / float(result[TierType[i]][6]), '.4f') 

    
    ### 按国家分Tier计算数据  ###
    oValue = [0] * len(TierType)  
    dnu = [0] * len(TierType)
    retention = [0] * len(TierType)
    tier = {}
    for type in TierType:
        tier[type] = [0] * (len(TierType) * 3)

    for i in range(len(sortedResult)):
        countryInfo = sortedResult[i]
        countInfo = countryInfo[1]
        if countryInfo[0] in Tier1:
            tier[TierType[0]][0] += countInfo['organic']
            tier[TierType[0]][1] += countInfo['non-organic']
            tier[TierType[0]][2] += countInfo['retention']

        elif countryInfo[0] in Tier2:
            tier[TierType[1]][0] += countInfo['organic']
            tier[TierType[1]][1] += countInfo['non-organic']
            tier[TierType[1]][2] += countInfo['retention']

        elif countryInfo[0] in Tier3:
            tier[TierType[2]][0] += countInfo['organic']
            tier[TierType[2]][1] += countInfo['non-organic']
            tier[TierType[2]][2] += countInfo['retention']

        elif countryInfo[0] in Tier4:
            tier[TierType[3]][0] += countInfo['organic']
            tier[TierType[3]][1] += countInfo['non-organic']
            tier[TierType[3]][2] += countInfo['retention']

        if countryInfo[0] in Tier5:
            tier[TierType[4]][0] += countInfo['organic']
            tier[TierType[4]][1] += countInfo['non-organic']
            tier[TierType[4]][2] += countInfo['retention']

        elif countryInfo[0] in Tier6:
            tier[TierType[5]][0] += countInfo['organic']
            tier[TierType[5]][1] += countInfo['non-organic']
            tier[TierType[5]][2] += countInfo['retention']

        elif countryInfo[0] in Tier7:
            tier[TierType[6]][0] += countInfo['organic']
            tier[TierType[6]][1] += countInfo['non-organic']
            tier[TierType[6]][2] += countInfo['retention']

        elif countryInfo[0] in Tier8:
            tier[TierType[7]][0] += countInfo['organic']
            tier[TierType[7]][1] += countInfo['non-organic']
            tier[TierType[7]][2] += countInfo['retention']

    for j in range(len(TierType)):
        if (tier[TierType[j]][1] == 0):
            oValue[j] = -1
        else:
            oValue[j] = format(float(tier[TierType[j]][0]) / float(tier[TierType[j]][1]), '.2f')

        dnu[j] = (tier[TierType[j]][0] + tier[TierType[j]][1])
        retention[j] = format(float(tier[TierType[j]][2]) / float(tier[TierType[j]][0] + tier[TierType[j]][1]), '.4f');
    return sortedResult, dnu, organic_install, facebook_ads_install, google_ad_install, oValue, retention, organic_retention, facebook_ads_retention, google_ad_retention, nonorganic_retention

def downloadRawData(url=""):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "parameters are invalid, please check it."
        exit(-1)
    if response.getcode() != 200:
        print "parameters are invalid, please check it."
        exit(-1)
    content = response.read()
    if (len(content) == 0):
        print "data is empty!"
        exit(-1)
    return content


if __name__ == "__main__":
    print "================ start fetching ================"
    apiToken = '29692403-60a5-48f7-94a6-cc381d2f3a1c'
    appId = ''
    startDate = ''
    endDate = ''
    dataFileName = ''
    url = ''

    date = datetime.datetime.now()
    endDate = date + datetime.timedelta(days=-3)
    startDate = date + datetime.timedelta(days=-9)
    endDate = endDate.strftime('%Y-%m-%d')
    startDate = startDate.strftime('%Y-%m-%d')
    print 'from: ', startDate
    print 'to: ', endDate
    
    TierDataHeader = getTierDataHeader();
    numpy.set_printoptions(threshold=numpy.nan)
    appsTierInfo = numpy.zeros([len(TierDataHeader), len(TierType)])

    print "please wait..."

    rows = len(TierDataHeader) / len(Apps)
    i = 0
    for key in Apps:
        startTime = datetime.datetime.now()
        appId = Apps[key]
        url = "https://hq.appsflyer.com/export/master_report/v4?api_token=29692403-60a5-48f7-94a6-cc381d2f3a1c&app_id=%s&from=%s&to=%s&groupings=geo,pid&kpis=installs,retention_day_1&timezone=preferred" % (appId, startDate, endDate)
        content = downloadRawData(url)

        rawDataFileName = "rawdata.csv"
        with open(rawDataFileName, "wb") as rawDataFile:
            rawDataFile.write(content)

        result, dnu, organic_install, facebook_ads_install, google_ad_install, oValue, retention, organic_retention, facebook_ads_retention, google_ad_retention, nonorganic_retention = analyzeCsvDataFile(rawDataFileName)
        
        appsTierInfo[rows * i] = dnu
        appsTierInfo[rows * i + 1] = organic_install
        appsTierInfo[rows * i + 2] = facebook_ads_install
        appsTierInfo[rows * i + 3] = google_ad_install
        appsTierInfo[rows * i + 4] = oValue
        appsTierInfo[rows * i + 5] = retention
        appsTierInfo[rows * i + 6] = organic_retention
        appsTierInfo[rows * i + 7] = nonorganic_retention
        appsTierInfo[rows * i + 8] = facebook_ads_retention
        appsTierInfo[rows * i + 9] = google_ad_retention

        os.remove(rawDataFileName)

        analyzedDataFileName = '%s.csv' % key
        createAppDataFile(analyzedDataFileName, result)
        print 'data file has been successfully restored in %s' % os.path.abspath(analyzedDataFileName)
        endTime = datetime.datetime.now()
        print 'used %d seconds...' % (endTime - startTime).seconds 
    	i += 1

    appsTierInfo = appsTierInfo.T
    tierFileName = 'tier.csv'
    createTierDataFile(tierFileName, appsTierInfo)
    print ''
    print '================================ export tier data successfully ================================'
    print 'Tier file has been successfully restored in %s' % os.path.abspath(tierFileName)

# -*- coding: UTF-8 -*-
import numpy as np

myList = [([]) for i in range(3)]
myList[0] = [1,2,3,4]
myList[0].append('ss')
myList[1] = [5,6,7,8]
myList[1].append('ss')
myList[2] = [9,10,11,12]
myList[2].append('ss')
print myList

list1 = np.transpose(myList)
print list1
