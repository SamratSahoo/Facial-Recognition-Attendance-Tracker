from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font
from init import *


def absentCell(cell):
    # Add Red Color Cell Format
    redFill = PatternFill(start_color='F4CCCC',
                          end_color='F4CCCC',
                          fill_type='solid')
    ws[cell].fill = redFill


def presentCell(cell):
    # Add Green Color Cell Format
    greenFill = PatternFill(start_color='D9EAD3',
                            end_color='D9EAD3',
                            fill_type='solid')
    ws[cell].fill = greenFill


def lateCell(cell):
    # Add Yellow Color Cell Format
    yellowFill = PatternFill(start_color='FFF2CC',
                             end_color='FFF2CC',
                             fill_type='solid')
    ws[cell].fill = yellowFill


def resetCell(cell):
    # Add White Color Cell Format
    whiteFill = PatternFill(start_color='FFFFFF',
                            end_color='FFFFFF',
                            fill_type='solid')
    ws[cell].fill = whiteFill


def addKey():
    # Reset Top Cells
    for n in range(1, 5):
        cellLocation = 'A' + str(n)
        resetCell(cellLocation)

    # Add Key Colors and Labels
    presentCell('A2')
    absentCell('A3')
    lateCell('A4')
    ws['A1'] = 'KEY'
    ws['A1'].font = Font(bold=True)
    ws['A2'] = 'Present'
    ws['A2'].font = Font(bold=True)
    ws['A3'] = 'Absent'
    ws['A3'].font = Font(bold=True)
    ws['A4'] = 'Late'
    ws['A4'].font = Font(bold=True)


def addStudentNames():
    # Format and write Student Name subtitle
    ws['A8'] = 'Student Names'
    ws['A8'].font = Font(bold=True)
    # Write student names from init list
    for n in range(0, len(fullStudentNames)):
        cellLocation = 'A' + str(9 + n)
        ws[cellLocation] = fullStudentNames[n]


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
        if ws[currentCell] == date:
            return cellStartNum
        else:
            cellStartNum += 1


def addDate():
    # Get and format date
    date = datetime.today().strftime('X%m/X%d')
    date = date.replace('X0', 'X').replace('X', '')
    # character number for "B"
    cellStartNum = ord('B')
    # Flag boolean to exit loop
    emptyDateCell = False

    while not emptyDateCell:
        # Get Current cell location
        currentCell = str(chr(cellStartNum)) + '8'
        # If the date is already there, then you do not need to add another column
        if ws[currentCell] == date:
            break
        else:
            # # If cell is not empty, move over one cell horizontally
            if ws[currentCell] != '':
                cellStartNum = cellStartNum + 1
            else:
                # If cell is empty, write the date
                ws[currentCell] = date
                ws[currentCell].font = Font(bold=True)
                emptyDateCell = True


def formatPage():
    # Adds key, student names, and current date
    if ws['A1'] != 'KEY':
        addKey()
    addStudentNames()
    addDate()


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

    formatPage()
    ws.save("AttendanceExcel.xlsx")
    wb = load_workbook(filename='empty_book.xlsx')


try:
    wb = Workbook()
    ws = wb.active
except:
    print(Exception)
