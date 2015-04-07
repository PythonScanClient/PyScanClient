import unittest
import os
from scan.util.spreadsheet import readSpreadsheet, writeSpreadsheet
from scan.util.scan_settings import ScanSettings
from scan.table.table_scan import loadTableScan

class SpreadsheetTest(unittest.TestCase):
    def testSpreadsheet(self):
        table = [ [ 'X', 'Y' ], [ '1', '2' ], [ '3', '4' ] ]
        
        filename = '/tmp/spreadsheet.csv'
        writeSpreadsheet(filename, table)
        
        table2 = readSpreadsheet(filename)
        print table2
        self.assertEqual(table, table2)

        os.remove(filename)


    def testTableScan(self):
        sheet = [ [ 'X', 'Y' ], [ '1', '2' ], [ '3', '4' ] ]
        
        filename = '/tmp/spreadsheet.csv'
        writeSpreadsheet(filename, sheet)
        
        table = loadTableScan(ScanSettings(), filename)
        print table
        self.assertEqual(table.headers, sheet[0])
        self.assertEqual(table.rows, sheet[1:])

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()