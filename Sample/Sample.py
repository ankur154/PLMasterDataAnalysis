import sys
import os
from datetime import datetime
import csv
#import xlrd

if __name__ == '__main__':
    #os.chdir(os.path.dirname(sys.argv[0]))

    def RepresentsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # def csv_from_excel(xlsxfilepath, sheetname, csvfilepath):
    #     isdone = False
    #     try:
    #         wb = xlrd.open_workbook(xlsxfilepath)
    #         sh = wb.sheet_by_name(sheetname)
    #         your_csv_file = open(csvfilepath, 'w')
    #         wr = csv.writer(your_csv_file, quoting=csv.QUOTE_MINIMAL)
    #
    #         for rownum in range(sh.nrows):
    #             xval = sh.row_values(rownum)
    #
    #             for i, a in enumerate(xval):
    #                 if(RepresentsInt(xval[i])):
    #                     xval[i] = int(xval[i])
    #
    #             wr.writerow(xval)
    #         isdone = True
    #     except:
    #         isdone = False
    #     finally:
    #         your_csv_file.close()
    #         return isdone

    def read_csv(csvfilepath):
        name_data = []
        with open(csvfilepath) as File:
            reader = csv.DictReader(File, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                name_data.append(row)
        return name_data

    def read_configuration(confFile):
        confdata= []
        with open(confFile) as File:
            reader = csv.DictReader(File, delimiter='|')
            for row in reader:
                confdata.append((row['WORD'], row['COLUMN_NAME']))
            return confdata

    def get_csvColumnNames(csvFilename):
        cols = []
        with open(csvFilename) as File:
            reader = csv.reader(File)
            cols = next(reader)
        return cols

    def read_postConfiguration(confFile):
        path_dict = {}
        f = open(confFile,'r')
        try:
            for line in f:
                line=line.strip()
                lvals = line.split('=')
                path_dict[lvals[0]] = lvals[1]
        except Exception as e:
            print(confFile)
            print(e)
        finally:
            f.close()
        return path_dict

    configFile = "config_1.csv" # Name of Configuration file
    filePath = "path.txt"       # Has location of Input/Ouput folders

    if not os.path.exists(configFile):
        print('configuration file is missing..')
        sys.exit()

    if not os.path.exists(filePath):
        print('path file is missing..')
        sys.exit()

    confdata = ""
    postconfig = ""
    filtCols = ""
    inputfolder = ""
    outputfolder = ""
    xlsxSheetName = ""

    try:
        confdata = read_configuration(configFile)
    except:
        pass
    try:
        postconfig = read_postConfiguration(filePath)
    except:
        pass
    try:
        filtCols =  str(postconfig['FiltersAppliedOn']).split(',')  # Defined in path file
    except:
        pass
    try:
        inputfolder = str(postconfig['InputFolder'])    # Defined in path file
    except:
        pass
    try:
        outputfolder = str(postconfig['OutputFolder'])  # Defined in path file
    except:
        pass
    # try:
    #     xlsxSheetName = str(postconfig['XlsSheetName'])
    # except:
    #     pass

    if(confdata is "" or postconfig is "" or filtCols is "" or inputfolder is "" or outputfolder is "" ): #or xlsxSheetName is ""):
        print("Something is wrong with the configuration.")


    def extractProcess(testval, allColumnNames ):   # Input records parsing as per configuration file
        description = ''
        for flt in filtCols:
            description = description + testval[flt] + ' '

        newconf = []
        description = description.strip()

        for cnfdata in confdata:
            ipos = description.find(cnfdata[0])
            newconf.append({'word': cnfdata[0], 'col':cnfdata[1], 'ipos':ipos, 'opos':0})

        newconf.sort(key=lambda x: x['ipos'], reverse=False)

        for i in range(0,len(newconf)):
            if(i < (len(newconf)-1)):
                if(newconf[i]['col'] != newconf[i + 1]['col']):
                    newconf[i]['opos'] = newconf[i + 1]['ipos']

        ci = -1
        sdata = {}
        for newcnfdata in newconf:
            if int(newcnfdata['ipos']) > 0 :
                ci = ci + 1
                if (ci is 0):
                    sdata[postconfig['ProductColumnName']] = description[:newcnfdata['ipos']].strip()
                    if (newcnfdata['opos'] > 0):
                        sdata[newcnfdata['col']] = description[newcnfdata['ipos']: newcnfdata['opos']].strip()
                    else:
                        sdata[newcnfdata['col']] = description[newcnfdata['ipos']:].strip()
                else:
                    if(newcnfdata['opos'] > 0):
                        sdata[newcnfdata['col']] = description[newcnfdata['ipos'] : newcnfdata['opos']].strip()
                    else:
                        sdata[newcnfdata['col']] = description[newcnfdata['ipos'] :].strip()
            else:
                sdata[newcnfdata['col']] = ''

        if postconfig['ProductColumnName'] not in sdata:    # Defined in path file
            sdata[postconfig['ProductColumnName']] = description

        for aCol in testval:
            if aCol in sdata:
                pass
            else:
                if aCol not in filtCols:
                    sdata[aCol] = testval[aCol]

        ndata = {}
        for acol in allColumnNames:
            if acol in sdata:
                ndata[acol] = sdata[acol]

        return ndata

    if not os.path.exists(outputfolder):  # Creating Output folder, if it does not exists
        os.makedirs(outputfolder)

    # Begin the execution from here
    if not os.path.exists(inputfolder):
        print("Input folder does not exists.")
    else:
        for file in os.listdir(inputfolder):
            inputFilePath = inputfolder + '/' + file
            print('(' + datetime.time(datetime.now()).strftime('%H:%M:%S') + ')[ ' + file + " ] Processing...")
            csvdata = ""
            cols = []
            isSkip = False
            if (inputFilePath.lower().endswith('xlsx')):
                isdone = csv(inputFilePath, xlsxSheetName, inputFilePath + ".csv")
                if (isdone):
                    csvdata = read_csv(inputFilePath + ".csv")
                    cols = get_csvColumnNames(inputFilePath + ".csv")
                    try:
                        os.remove(inputFilePath + ".csv")
                    except:
                        pass
            elif (inputFilePath.lower().endswith('csv')):
                csvdata = read_csv(inputFilePath)
                cols = get_csvColumnNames(inputFilePath)
            else:
                isSkip = True

            if isSkip is False :
                allColumnNames = []

                for colname in cols:
                    if colname not in allColumnNames:
                        allColumnNames.append(colname)

                for colname in confdata:
                    if colname[1] not in allColumnNames:
                        allColumnNames.append(colname[1])

                mainlist = []
                for csvd in csvdata:
                    csvrowdata = extractProcess(csvd, allColumnNames)
                    mainlist.append(csvrowdata)

                allcolslist = []
                for md in mainlist[0]:
                    allcolslist.append(md)

                #oflname = ('.').join(file.split('.')[:-1])
                oflname  = (datetime.now().strftime('%Y%m%d%H%M%S'))
                with open(outputfolder + '/' + oflname + ".csv", 'w') as csvfile:
                    fieldnames = allcolslist
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    for mnlst in mainlist:
                        writer.writerow(mnlst)

                print('(' + datetime.time(datetime.now()).strftime('%H:%M:%S') + ')[ ' + file + " ] Done.")
            else:
                print('(' + datetime.time(datetime.now()).strftime('%H:%M:%S') + ')[ ' + file + " ] Skipped.")

    print('(' + datetime.time(datetime.now()).strftime('%H:%M:%S') + ') All done!!!')