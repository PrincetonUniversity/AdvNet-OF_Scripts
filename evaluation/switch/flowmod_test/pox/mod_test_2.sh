#/bin/bash
#current=`date +"%s"`
vendor=$1
inport=$2
outport=$3
mode=mod_2
DIRECTORY=MeasurementResults_Princeton/$vendor"/"$mode

if [ ! -d "$DIRECTORY" ]; then
    mkdir MeasurementResults_Princeton/$vendor"/"$mode
fi

for i in 50 100 200; do
    for j in {10..100..10}; do
        folder=MeasurementResults_Princeton/$vendor"/"$mode"/"$j"_"$i
        if [ ! -d "$folder" ]; then
            mkdir $folder
        fi
        for k in {1..5..1}; do
            sudo bash clean.sh
            sudo bash single_run.sh $mode $j $i $inport $outport
            mkdir $folder"/round"$k
#            mv conn.log $folder"/round"$k

            mv poxout1 $folder"/round"$k
            mv sorted_flow_delay.txt $folder"/round"$k
            mv flow_delays.txt $folder"/round"$k
#            mv results.txt $folder"/round"$k
            cp delay_plain.gp $folder"/round"$k
            sleep 10
            
        # Get distribution
#        python get_dist.py $folder
#        cp delay_cdf.gp $folder
        done
    done
done
