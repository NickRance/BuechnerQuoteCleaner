import csv
import sys
from pprint import pprint

PATH_BLACKLIST = 'blacklist.txt'

def main():
    print('main')
    readImportFile(sys.argv[1])

def readImportFile(filename):
    cleanList = []
    removalList = []
    with open(filename,'r') as fp:
        reader = csv.DictReader(fp)
        header = reader.fieldnames
        # pprint(header)
        #skips header
        next(reader)
        filterList = ['ä', '§', "_x001A_", "&quot", 'æ', '¤', 'µ','©']
        for (val) in reader:
            deleted = False
            for f in filterList:
                if f in val['Source']:
                    removalList.append(val)
                    del val
                    deleted = True
                    break
            if not deleted:
                # next(reader)
                if "_x001A_" in val['Quote']:
                    val['Quote'] = val['Quote'].replace("_x001A_","'")
                    val['Quote'] = val['Quote'].replace("\xa0",". ")
                    cleanList.append(val)
                else:
                    cleanList.append(val)
        writeCleanedFile("clean.csv",cleanList)
        writeCleanedFile("dirty.csv",removalList)
        blackList = readBlackList(PATH_BLACKLIST)
        flagBlackWords(blackList, cleanList, "flagged.csv")


def writeCleanedFile(outfile, data):
    # pprint(data)
    with open(outfile, 'w') as fou:

        if isinstance(data,dict):
            dw = csv.DictWriter(fou, fieldnames=data.keys())
            dw.writeheader()
            for key, val in sorted(data.items()):
            # print(val)
                dw.writerow({key:val})
        elif isinstance(data,list):
            dw = csv.DictWriter(fou, fieldnames=data[0].keys())
            dw.writeheader()
            for val in data:
                # print(val)
                dw.writerow(val)

def readBlackList(filename):
    output = set()
    with open(filename,'r') as fp:
        for line in fp:
            # print(line)
            if line.strip() == '':
                continue
            else:
                output.add(line.strip())
    # print(output)
    return output

def flagBlackWords(blackList, formattedData, outputFilePath):
    flaggedQuotes = []
    for item in formattedData:
        item['flaggedWords'] = []
        for word in blackList:
            quoteWords = [x.lower() for x in item['Quote'].split(' ')]
            if word in quoteWords:
                item['flaggedWords'].append(word.title())
        if len(item['flaggedWords']) > 0:
            item['Severity Score'] = len(item['flaggedWords'])
            flaggedQuotes.append(item)
    writeCleanedFile(outputFilePath, flaggedQuotes)


if __name__== '__main__':
    main()
