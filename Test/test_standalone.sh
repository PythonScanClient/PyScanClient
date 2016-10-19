# Execute all tests that can run without any dependencies

export PYTHONPATH=".."

FAILED=0
python test_range_helper.py
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

python test_scan_settings.py
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

python test_commands.py
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

python test_table_scan.py
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

python test_data.py
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

python -m doctest test_ndim.txt
if [ $? -ne 0 ]
then
    FAILED=`expr $FAILED + 1`
fi

# To run only one specific test:
#  python test_table_scan.py TableScanTest.testParallel


echo
echo "================================================================"
echo "Summary:"
echo "$FAILED tests failed"
