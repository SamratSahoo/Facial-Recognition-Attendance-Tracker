import gspread
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *
import datetime

from init import fullStudentNames
from datetime import datetime


def loadLists(textFile):
    with open(textFile) as file:
        list = file.readlines()
        file.close()
        list = [x[:-1] for x in list]
    return list


def absentCell(cell):
    # Add Red Color Cell Format
    format = CellFormat(backgroundColor=Color(.96, .80, .80))
    # Update a Cell as Absent
    format_cell_range(sheet, cell, format)


def presentCell(cell):
    # Add Green Color Cell Format
    format = CellFormat(backgroundColor=Color(.85, .93, .82))
    # Update a Cell as Present
    format_cell_range(sheet, cell, format)


def lateCell(cell):
    # Add Yellow Color Cell Format
    format = CellFormat(backgroundColor=Color(1.00, .95, .80))
    # Update a Cell as Late
    format_cell_range(sheet, cell, format)


def resetCell(cell):
    # Add White Color Cell Format
    format = CellFormat(backgroundColor=Color(1, 1, 1))
    # Reset a Cell
    format_cell_range(sheet, cell, format)
    sheet.update_acell(cell, '')


def addKey():
    # Reset Top Cells
    for n in range(1, 5):
        cellLocation = 'A' + str(n)
        resetCell(cellLocation)

    # Add Key Colors and Labels
    presentCell('A2')
    absentCell('A3')
    lateCell('A4')
    format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet, 'A1', format)
    sheet.update_acell('A1', 'KEY')
    sheet.update_acell('A2', 'Present')
    sheet.update_acell('A3', 'Absent')
    sheet.update_acell('A4', 'Late')


def addStudentNames():
    # Format and write Student Name subtitle
    format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet, 'A8', format)
    sheet.update_acell('A8', 'Student Names')
    # Write student names from init list
    for n in range(0, len(fullStudentNames)):
        cellLocation = 'A' + str(9 + n)
        sheet.update_acell(cellLocation, fullStudentNames[n])


def addDate():
    # Get and format date
    date = datetime.today().strftime('X%m/X%d')
    date = date.replace('X0', 'X').replace('X', '')
    # character number for "B"
    cellStartNum = ord('B')
    # Flag boolean to exit loop
    emptyDateCell = False
    # Format Date Subtitles
    format = CellFormat(textFormat=TextFormat(bold=True), horizontalAlignment='RIGHT')

    while not emptyDateCell:
        # Get Current cell location
        currentCell = str(chr(cellStartNum)) + '8'
        # If the date is already there, then you do not need to add another column
        if sheet.acell(currentCell).value == date:
            break
        else:
            # # If cell is not empty, move over one cell horizontally
            if sheet.acell(currentCell).value != '':
                cellStartNum = cellStartNum + 1
            else:
                # If cell is empty, write the date
                format_cell_range(sheet, currentCell, format)
                sheet.update_acell(currentCell, date)
                emptyDateCell = True


def formatPage():
    # Adds key, student names, and current date
    if sheet.acell('A1').value != 'KEY':
        addKey()
    addStudentNames()
    addDate()


def getRowNum(personToFind):
    startCellNum = 9
    for x in range(0, len(fullStudentNames)):
        # Find how many to go down from row 9 by comparing names + arrays
        if fullStudentNames[x].strip() == personToFind.strip():
            # Update row to go to
            startCellNum += x
    return startCellNum


def getColumnLetter():
    # Start column is B
    cellStartNum = ord('B')
    # Get date because column will correspond
    date = datetime.today().strftime('X%m/X%d')
    date = date.replace('X0', 'X').replace('X', '')
    columnFound = False
    # Compare current date to column date
    while not columnFound:
        currentCell = str(chr(cellStartNum)) + '8'
        # If found, return cell column Letter
        if sheet.acell(currentCell).value == date:
            return cellStartNum
        else:
            cellStartNum += 1


def updatePresentPerson(personToFind):
    # Change numerical values to cell value
    cellToPresent = chr(getColumnLetter()) + str(getRowNum(personToFind))
    # Mark present
    presentCell(cellToPresent)


def updateAbsentPerson(personToFind):
    # Change numerical values to cell value
    cellToAbsent = chr(getColumnLetter()) + str(getRowNum(personToFind))
    # Mark Absent
    absentCell(cellToAbsent)


def updateLatePerson(personToFind):
    # Change numerical values to cell value
    cellToAbsent = chr(getColumnLetter()) + str(getRowNum(personToFind))
    # Mark Late
    lateCell(cellToAbsent)


def markOnce(name):
    # Change numerical values to cell value
    cellToCheck = str(chr(getColumnLetter())) + str(getRowNum(name))
    # Return False if cell is not white or red
    return worksheet.cell(cellToCheck).color != (None, None, None, None) or worksheet.cell(cellToCheck).color != (
        .96, .80, .80, 1.00)


def markAbsentUnmarked():
    rowStart = 9
    for x in range(0, len(fullStudentNames)):
        cellToCheck = str(chr(getColumnLetter())) + str(rowStart)
        if worksheet.cell(cellToCheck).color == (None, None, None, None):
            absentCell(cellToCheck)
            rowStart += 1
        else:
            rowStart += 1


try:
    fullStudentNames = loadLists("List Information/Full Student Names")
    # Gets scope of sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    # Gets sheet credentials and authorizes it
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    # Opens sheet based on sheet name
    sheet = client.open("19/20 Attendance").sheet1

    # Authorize Pygsheets library
    gc = pygsheets.authorize()
    worksheet = gc.open('19/20 Attendance').sheet1
    formatPage()
except Exception as e:
    print(e)
