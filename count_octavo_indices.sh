timenow=$(date +"%D - %T")
e11=$(wc -l output/octavo_indices/ecco1_ids1/summary.csv | awk '{print $1 -2}')
e12=$(wc -l output/octavo_indices/ecco1_ids2/summary.csv | awk '{print $1 -2}')
e13=$(wc -l output/octavo_indices/ecco1_ids3/summary.csv | awk '{print $1 -2}')
e14=$(wc -l output/octavo_indices/ecco1_ids4/summary.csv | awk '{print $1 -2}')
all=$(expr $e11 + $e12 + $e13 + $e14)
echo Time: $timenow
echo Total ids processed: $all
