#!/bin/bash
#BER fixe, PAYLOAD variable :
#./simul -p <data> <ber> <payload_min> <payload_max><pas>
#Exemple :
#./simul -p 10G 0.001 50 400 20

#PAYLOAD fixe, BER variable (pas fixe) : 
#./simul -b <data> <payload> <ber_min> <ber_max>
#Exemple :
#./simul -b 10G 500 0.00001 0.01

# store arguments in an array 
args=("$@") 
# get number of elements 
ELEMENTS=${#args[@]} 

if [ $# -eq 0 ]; then
    echo "- Usage 1 -> ber fixe, payload variable :"
    echo " ./simul.sh -p <taille donn�es> <BER> <payload_min> <payload_max> <pas>"
    echo "- Usage 2 -> payload fixe, ber variable :"
    echo " ./simul.sh -b <taille donn�es> <payload> <ber_min> <ber_max>"
    exit
fi

rm -f results.txt
echo "Starting simulation..."

if [ $1 == "-p" ]; then
echo "Usage 1 : ber fixe, payload variable"
	
step=$6

for (( payload=$payload_min;payload<=$payload_max;payload+=$step)); do
cd src/
results=$(python main.py -q -P $payload -r $data $ber)
read results< <(echo "$results" | tail -n1)
echo $results
cd ../
touch results.txt
results="$results \n"
echo $results$'\r' >> results.txt
done
gnuplot -p -e "plot 'results.txt' u 3:4 w l"
fi

if [ $1 == "-b" ]; then
echo "Usage 2 : payload fixe, ber variable"
data=$2
payload=$3
ber_min=$4
ber_max=$5

ber=$ber_min
step= 0.00005

while [ $ber -lt $ber_max ]
do
	echo $ber + $step | bc
done

cd src/
results=$(python main.py -q -P $payload -r $data $ber)
read results< <(echo "$results" | tail -n1)
echo $results
cd ../
touch results.txt
results="$results \n"
echo $results$'\r' >> results.txt
#gnuplot -p -e "plot 'results.txt' u 3:4 w l"
fi

echo "done!"
