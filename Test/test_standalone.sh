# Execute all tests that can run without any dependencies
DIRNAME=`dirname "$0"`

PYTHON="${PYTHON:-python}"

export PYTHONPATH=".."

FAILED=0
$PYTHON "$DIRNAME/test_range_helper.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON "$DIRNAME/test_scan_settings.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON "$DIRNAME/test_commands.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON "$DIRNAME/test_table_scan.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON "$DIRNAME/test_data.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON -m doctest "$DIRNAME/test_ndim.txt"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON -m doctest "$DIRNAME/test_alignment.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

$PYTHON -m doctest "$DIRNAME/test_spreadsheet.py"
if [ $? -ne 0 ]
then
    echo "FAILED!"
    FAILED=`expr $FAILED + 1`
fi

# To run only one specific test:
#  python test_table_scan.py TableScanTest.testParallel


echo
echo "================================================================"
echo "Summary:"
echo "$FAILED tests failed"
