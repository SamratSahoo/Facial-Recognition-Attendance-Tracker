import gspread
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *
import datetime

from init import fullStudentNames
from datetime import datetime


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
    # If page is already formatted, there is no need to format again
    if sheet.acell('A1').value == '':
        addKey()
        addStudentNames()
    # Adds Date regardless of current formatting
    addDate()


def updatePresentPerson(personToFind):
    def getRowNum():
        startCellNum = 9
        for x in range(0, len(fullStudentNames)):
            if fullStudentNames[x].strip() == personToFind.strip():
                startCellNum += x
        return startCellNum

    def getColumnLetter():
        cellStartNum = ord('B')
        date = datetime.today().strftime('X%m/X%d')
        date = date.replace('X0', 'X').replace('X', '')
        columnFound = False
        while not columnFound:
            currentCell = str(chr(cellStartNum)) + '8'
            if sheet.acell(currentCell).value == date:
                return cellStartNum
            else:
                cellStartNum += 1

    cellToPresent = chr(getColumnLetter()) + str(getRowNum())
    presentCell(cellToPresent)


def updateAbsentPerson(personToFind):
    def getRowNum():
        startCellNum = 9
        for x in range(0, len(fullStudentNames)):
            if fullStudentNames[x].strip() == personToFind.strip():
                startCellNum += x
        return startCellNum

    def getColumnLetter():
        cellStartNum = ord('B')
        date = datetime.today().strftime('X%m/X%d')
        date = date.replace('X0', 'X').replace('X', '')
        columnFound = False
        while not columnFound:
            currentCell = str(chr(cellStartNum)) + '8'
            if sheet.acell(currentCell).value == date:
                return cellStartNum
            else:
                cellStartNum += 1

    cellToAbsent = chr(getColumnLetter()) + str(getRowNum())
    absentCell(cellToAbsent)


def updateLatePerson(personToFind):
    def getRowNum():
        startCellNum = 9
        for x in range(0, len(fullStudentNames)):
            if fullStudentNames[x].strip() == personToFind.strip():
                startCellNum += x
        return startCellNum

    def getColumnLetter():
        cellStartNum = ord('B')
        date = datetime.today().strftime('X%m/X%d')
        date = date.replace('X0', 'X').replace('X', '')
        columnFound = False
        while not columnFound:
            currentCell = str(chr(cellStartNum)) + '8'
            if sheet.acell(currentCell).value == date:
                return cellStartNum
            else:
                cellStartNum += 1

    cellToAbsent = chr(getColumnLetter()) + str(getRowNum())
    lateCell(cellToAbsent)


def markOnce(name):
    def getRow():
        startCellNum = 9
        for x in range(0, len(fullStudentNames)):
            if fullStudentNames[x].strip() == name.strip():
                startCellNum += x
                break
        return startCellNum

    def getColumn():
        cellStartNum = ord('B')
        date = datetime.today().strftime('X%m/X%d')
        date = date.replace('X0', 'X').replace('X', '')
        columnFound = False
        while not columnFound:
            currentCell = str(chr(cellStartNum)) + '8'
            if sheet.acell(currentCell).value == date:
                return cellStartNum
            else:
                cellStartNum += 1

    cellToCheck = str(chr(getColumn())) + str(getRow())
    return worksheet.cell(cellToCheck).color != (None, None, None, None)


def markAbsentUnmarked():
    def getColumn():
        cellStartNum = ord('B')
        date = datetime.today().strftime('X%m/X%d')
        date = date.replace('X0', 'X').replace('X', '')
        columnFound = False
        while not columnFound:
            currentCell = str(chr(cellStartNum)) + '8'
            if sheet.acell(currentCell).value == date:
                return cellStartNum
            else:
                cellStartNum += 1

    rowStart = 9
    for x in range(0, len(fullStudentNames)):
        cellToCheck = str(chr(getColumn())) + str(rowStart)
        if worksheet.cell(cellToCheck).color == (None, None, None, None):
            absentCell(cellToCheck)
            rowStart += 1
        else:
            rowStart += 1


try:
    # Gets scope of sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    # Gets sheet credentials and authorizes it
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    # Opens sheet based on sheet name
    sheet = client.open("Attendance Tracking").sheet1

    # Authorize Pygsheets library
    gc = pygsheets.authorize()
    worksheet = gc.open('Attendance Tracking').sheet1

except Exception as e:
    print(e)
