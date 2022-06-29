
awk -f compact.awk SICK.txt > compacted.txt
sort -n sentences.txt > sentences.tmp
sort -n originals.txt > originals.tmp
mv sentences.tmp sentences.txt
mv originals.tmp originals.txt

split -l 2000 sentences.txt sentences-
REL=~/hpsg/logon/lingo/lkb/src/tsdb/skeletons/english/Relations
for f in sentences-??; do
    awk -F "\t" -v OFS="@" 'BEGIN {print "i-origin","i-input"} {print $1, $2}' $f > $f.tsv;
    rm $f;
    delphin mkprof -v -i $f.tsv --delimiter "@" --relations $REL --skeleton $f;
done
rm *.tsv
