f=open("DataS3.txt","r");
for line in f:
    line=line.strip()
    a=line.split("\t")
    x=a[6].split("_")
    print "\t".join([x[0],x[1],x[2],x[3],"0",a[4]])
