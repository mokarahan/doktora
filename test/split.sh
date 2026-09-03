grep discharge metadata.csv | grep B0005 |  awk -F',' '{print $8}'|more
