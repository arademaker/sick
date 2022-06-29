source ~/venv/bin/activate
cd ~/sick
delphin process -vv -g erg.dat -o "-n 10 --timeout=60 --max-words=150 --max-chart-megabytes=4000 --max-unpack-megabytes=5000 --rooted-derivations --udx --disable-generalization" -z -s $1 $1.full
