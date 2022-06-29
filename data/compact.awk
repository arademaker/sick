
BEGIN {
    FS = "\t"
    OFS = "\t"
    counter = 1;
    split("2:3",c,/:/);
    split("8:9",d,/:/)
}

NR <= 1 {
    print $0
}    

NR > 1 {
    for(i in c) {
	j = c[i]
	if($j in data)
	    $j = data[$j]
	else {
	    data[$j] = counter++
	    $j = data[$j]
	}
    }
    for(i in d) {
	j = d[i]
	if($j in orig)
	    $j = orig[$j]
	else {
	    orig[$j] = counter++
	    $j = orig[$j]
	}
    }
    print
}

END {
    for(i in data){
	print data[i],i > "sentences.txt"
    }
    for(i in orig){
	print orig[i],i > "originals.txt"
    }

}
