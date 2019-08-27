from __future__ import print_function
import unittest
import os
from scan.util.spreadsheet import readSpreadsheet, writeSpreadsheet
from scan.table.table_scan import TableScan, loadTableScan

class SpreadsheetTest(unittest.TestCase):
    def testSpreadsheet(self):
        table = [ [ 'XPos', 'YPos' ], [ '1', '2' ], [ '3', '4' ] ]
        
        filename = '/tmp/spreadsheet.csv'
        writeSpreadsheet(filename, table)
        
        table2 = readSpreadsheet(filename)
        print(table2)
        self.assertEqual(table, table2)

        os.remove(filename)


    def testTableScan(self):
        table = TableScan([ 'XPos', 'YPos' ], [ [ '1', '2' ], [ '3', '4' ] ] )
        filename = '/tmp/spreadsheet.csv'
        table.save(filename)
        
        table2 = loadTableScan(filename)
        print(table)
        self.assertEqual(table.headers, table2.headers)
        self.assertEqual(table.rows, table2.rows)

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()