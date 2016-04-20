#/bin/bash

# Create directory for vendor
DIRECTORY=MeasurementResults_Princeton/$1
if [ ! -d "$DIRECTORY" ]; then
    mkdir MeasurementResults_Princeton/$1
fi
inport=$2
outport=$3

# Run add test
#bash add_test.sh $1 $inport $outport

# Run mod test
bash mod_test.sh $1 $inport $outport

# Run mod 2 test
bash mod_test_2.sh $1 $inport $outport
