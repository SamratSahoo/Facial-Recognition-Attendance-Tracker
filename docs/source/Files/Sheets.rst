Sheets.py
==============
The ``Sheets.py`` file controls the outputs to a Google sheet. There are several helper methods in ``Sheets.py`` that make outputting possible.

Imports
-------

.. code-block:: python

    import gspread
    import pygsheets
    from oauth2client.service_account import ServiceAccountCredentials
    from gspread_formatting import *
    import datetime
    from init import fullStudentNames
    from datetime import datetime

* ``gspread``: Necessary to access the google sheet
* ``pygsheets``: Necessary to manipulate the Google Sheet
* ``oauth2client``: Necessary to connect to Google's servers
* ``gspread_formatting``: Necessary to format the Google Sheet
* ``datetime``: Necessary to get the date
* ``init``: Necessary to access the arrays

Methods
-------
The ``loadLists()`` method will allow for us to load the list information from ``Full Student Names.txt`` into the arrays in ``init.py``

.. code-block:: python

    def loadLists(textFile):
        with open(textFile) as file:
            list = file.readlines()
            file.close()
            list = [x[:-1] for x in list]
        return list

The ``absentCell()`` method marks a given cell red.

.. code-block:: python

    def absentCell(cell):
        # Add Red Color Cell Format
        format = CellFormat(backgroundColor=Color(.96, .80, .80))
        # Update a Cell as Absent
        format_cell_range(sheet, cell, format)

The ``presentCell()`` method marks a given cell green.

.. code-block:: python

    def presentCell(cell):
        # Add Green Color Cell Format
        format = CellFormat(backgroundColor=Color(.85, .93, .82))
        # Update a Cell as Present
        format_cell_range(sheet, cell, format)

The ``lateCell()`` method marks a given cell yellow.

.. code-block:: python

    def lateCell(cell):
        # Add Yellow Color Cell Format
        format = CellFormat(backgroundColor=Color(1.00, .95, .80))
        # Update a Cell as Late
        format_cell_range(sheet, cell, format)

The ``resetCell()`` method marks a given cell white.

.. code-block:: python

    def resetCell(cell):
        # Add White Color Cell Format
        format = CellFormat(backgroundColor=Color(1, 1, 1))
        # Reset a Cell
        format_cell_range(sheet, cell, format)
        sheet.update_acell(cell, '')

The ``addKey()`` method adds the Sheet key to the upper left hand corner of the sheet.

.. code-block:: python

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

The ``addStudentNames()`` method adds the Student names in the first column of the sheet.

.. code-block:: python

    def addStudentNames():
        # Format and write Student Name subtitle
        format = CellFormat(textFormat=TextFormat(bold=True))
        format_cell_range(sheet, 'A8', format)
        sheet.update_acell('A8', 'Student Names')
        # Write student names from init list
        for n in range(0, len(fullStudentNames)):
            cellLocation = 'A' + str(9 + n)
            sheet.update_acell(cellLocation, fullStudentNames[n])

The ``addDate()`` method adds the current date. In coordination with the application, it marks the date the application is launched.

.. code-block:: python

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

The ``formatPage()`` method formats the page as needed if it has already not been formatted.

.. code-block:: python

    def formatPage():
        # Adds key, student names, and current date
        if sheet.acell('A1').value != 'KEY':
            addKey()
        addStudentNames()
        addDate()

The ``getRowNumber()`` method gets the row number to mark. This is used to mark a certain student.

.. code-block:: python

    def getRowNum(personToFind):
    startCellNum = 9
    for x in range(0, len(fullStudentNames)):
        # Find how many to go down from row 9 by comparing names + arrays
        if fullStudentNames[x].strip() == personToFind.strip():
            # Update row to go to
            startCellNum += x
    return startCellNum

The ``getColumnLetter()`` method gets the column letter to mark. This is used to mark on a certain date.

.. code-block:: python

    def getColumnLetter(sheet):
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
        if sheet[currentCell].value == date:
            return cellStartNum
        else:
            cellStartNum += 1

The ``updatePresentPerson()`` method updates a Google sheet passed on the person's name.

.. code-block:: python

    def updatePresentPerson(personToFind):
        # Change numerical values to cell value
        cellToPresent = chr(getColumnLetter(ws)) + str(getRowNum(personToFind))
        # Mark present
        presentCell(cellToPresent)

The ``updateAbsentPerson()`` method updates an Google sheet passed on the person's name.

.. code-block:: python

    def updateAbsentPerson(personToFind):
        # Change numerical values to cell value
        cellToAbsent = chr(getColumnLetter(ws)) + str(getRowNum(personToFind))
        # Mark Absent
        absentCell(cellToAbsent)


The ``updateLatePerson()`` method updates a Google Sheet passed on the person's name.

.. code-block:: python

    def updateLatePerson(personToFind):
        # Change numerical values to cell value
        cellToAbsent = chr(getColumnLetter(ws)) + str(getRowNum(personToFind))
        # Mark Late
        lateCell(cellToAbsent)

The ``markOnce()`` method is used to make sure a cell is not overwritten.

.. code-block:: python

    def markOnce(name):
        # Change numerical values to cell value
        cellToCheck = str(chr(getColumnLetter())) + str(getRowNum(name))
        # Return False if cell is not white or red
        return worksheet.cell(cellToCheck).color != (None, None, None, None) or worksheet.cell(cellToCheck).color != (
            .96, .80, .80, 1.00)

The ``markAbsentUnmarked()`` method will mark all people who were not present as absent.

.. code-block:: python

    def markAbsentUnmarked():
        rowStart = 9
        for x in range(0, len(fullStudentNames)):
            cellToCheck = str(chr(getColumnLetter())) + str(rowStart)
            if worksheet.cell(cellToCheck).color == (None, None, None, None):
                absentCell(cellToCheck)
                rowStart += 1
            else:
                rowStart += 1

Main Method
-----------
The main method will authorize all of the necessary credentials and then find the Google Sheet within the Google Drive of the respective account. It will lastly autoformat the page.

.. code-block:: python

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

