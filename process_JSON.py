import os
import sys
import json
from fnmatch import fnmatch

import csv
import time

# First task
def scanJsonFile(filePath, goldenList):
	with open(filePath, 'r') as file:
		fileContent = file.read()

	decodedContent = json.loads(fileContent)
	
	fieldsList = decodedContent.keys()

	for currentField in goldenList:
		assert currentField in fieldsList, 'ERROR: \"' + currentField + '\" field does not exist in \"' + filePath + '\" file'

# Second task			
def compareIds(filePath, firstIterationComplete, firstFileIdValue, firstFilePath):
	with open(filePath, 'r') as file:
		fileContent = file.read()

	decodedContent = json.loads(fileContent)
	
	assert 'id' in decodedContent.keys(), 'ERROR: \"id\" field does not exist in \"' + filePath + '\" file'
	
	if firstIterationComplete:
		assert firstFileIdValue == decodedContent['id'], 'ERROR: The \"id\" of \"' + filePath + '\" file does not equal to the \"id\" of \"' + firstFilePath + '\" file'

	else:
		return decodedContent['id']

# Third task
def writeIntoCSV(filePath):
	with open(filePath, 'r') as file:
		fileContent = file.read()

	decodedContent = json.loads(fileContent)
	
	assert 'type' in decodedContent.keys(), 'ERROR: \"type\" field does not exist in \"' + filePath + '\" file'
	assert 'name' in decodedContent.keys(), 'ERROR: \"name\" field does not exist in \"' + filePath + '\" file'

	with open('types.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([decodedContent['type'], decodedContent['name']])
		csvfile.seek(-2, os.SEEK_END)
		csvfile.truncate()

# Fourth task
def removePublishDate(filePath):
	with open(filePath, 'r') as file:
		fileContent = file.read()
	
	decodedContent = json.loads(fileContent)
	
	assert 'publishDate' in decodedContent.keys(), 'ERROR: \"publishDate\" field does not exist in \"' + filePath + '\" file'
	
	del decodedContent['publishDate']
	encodedContent = json.dumps(decodedContent)

	with open(filePath, 'w') as file:
		file.write(encodedContent)
	
# Fifth task	
def replaceDate(filePath, currentDate):
	with open(filePath, 'r') as file:
		fileContent = file.read()
	
	decodedContent = json.loads(fileContent)
	
	assert 'date' in decodedContent.keys(), 'ERROR: \"date\" field does not exist in \"' + filePath + '\" file'
	assert '$date' in decodedContent['date'].keys(), 'ERROR: \"$date\" field does not exist in \"' + filePath + '\" file'
	
	decodedContent['date']['$date'] = currentDate
	encodedContent = json.dumps(decodedContent)

	with open(filePath, 'w') as file:
		file.write(encodedContent)
	

if __name__ == '__main__':
	argsList = sys.argv
	argsDict = {}
	try:
		argsDict = dict(argsList[i:i+2] for i in range(1, len(argsList), 2))
	except ValueError as e:
		print 'ERROR: There is missing argument. Please complete argument list.'
		exit()

	jsonsPath = os.getcwd() # Default value is the current directory
	# Handle '-jp' option and remove from dictionary
	if '-jp' in argsDict.keys():
		jsonsPath = argsDict['-jp']
		del argsDict['-jp']
	
	# After handling all options, the option list should be empty
	if argsDict:
		print 'ERROR: Incorrect options: ',
		for c in argsDict.keys():
			print c + ' '
		exit()
	
	# Collect all json files recursively
	jsonFilesList = []
	for path, subdirs, files in os.walk(jsonsPath):
		for name in files:
			if fnmatch(name, '*.json'):
				jsonFilesList.append(os.path.join(path, name))

	totalCount = len(jsonFilesList)
	
	if totalCount == 0:
		print 'No json file is found in specified directory.'
		exit()
	
	# Starting test
	overallStatus = "SUCCEEDS"
	
	# First task
	print 'Start testing JSON File Scan'
	currentStatus = "SUCCEEDS"
	goldenList = ['id', 'version', 'type', 'date', 'publishDate', 'name']
	for currentJsonFile in jsonFilesList:
		try:
			scanJsonFile(currentJsonFile, goldenList)
		except AssertionError as e:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print e
		except ValueError:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print 'ERROR: JSON File \"' + currentJsonFile +  '\" is corrupted'
	#print '\nEnd JSON File Scan\n'
	print currentStatus, '\n'
				
	# Second task
	print 'Start testing Compare IDs'
	currentStatus = "SUCCEEDS"
	firstIterationComplete = False
	firstFileIdValue = ''
	firstFilePath = ''
	for currentJsonFile in jsonFilesList:
		try:
			if firstIterationComplete:
				compareIds(currentJsonFile, firstIterationComplete, firstFileIdValue, firstFilePath)
				continue
			else:
				firstFilePath = currentJsonFile
				firstFileIdValue = compareIds(currentJsonFile, firstIterationComplete, '', firstFilePath)
				firstIterationComplete = True
		except AssertionError as e:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print e
		except ValueError:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print 'ERROR: JSON File \"' + currentJsonFile +  '\" is corrupted'
	#print '\nEnd Compare IDs\n'
	print currentStatus, '\n'
					
	# Third task
	print 'Start testing Write Into CSV'
	currentStatus = "SUCCEEDS"
	with open('types.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['TYPE', 'NAME'])
		csvfile.seek(-2, os.SEEK_END)
		csvfile.truncate()
	
	for currentJsonFile in jsonFilesList:
		try:
			writeIntoCSV(currentJsonFile)
		except AssertionError as e:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print e
		except ValueError:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print 'ERROR: JSON File \"' + currentJsonFile +  '\" is corrupted'
	#print '\nEnd Write Into CSV\n'
	print currentStatus, '\n'
	
	# Fourth task
	print 'Start testing Remove Publish Date'
	currentStatus = "SUCCEEDS"
	for currentJsonFile in jsonFilesList:
		try:
			removePublishDate(currentJsonFile)
		except AssertionError as e:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print e
		except ValueError:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print 'ERROR: JSON File \"' + currentJsonFile +  '\" is corrupted'
	#print '\nEnd Remove Publish Date\n'
	print currentStatus, '\n'
	
	# Fifth task
	print 'Start testing Replace Date'
	currentStatus = "SUCCEEDS"
	for currentJsonFile in jsonFilesList:
		try:
			replaceDate(currentJsonFile, time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
		except AssertionError as e:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print e
		except ValueError:
			currentStatus = "FAILED!"
			overallStatus = "FAILED!"
			print 'ERROR: JSON File \"' + currentJsonFile +  '\" is corrupted'
	#print '\nEnd Replace Date\n'
	print currentStatus, '\n'
	
	if totalCount > 1:
		print str(totalCount) + ' json files have been tested successfully.'
	else:
		print str(totalCount) + ' json file has been tested successfully.'
	print 'Overall Status: ', overallStatus, '\n'
