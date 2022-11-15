# Bracken2OTU
simple python script that takes Bracken outputs and merges them into one OTU table, user can specify if a subset of outputs need to be summed together prior to appending to the OTU table


## example:

```
Bracken2OTU.py -i *.bracken -sum sum_by_lane -o merged.otu
```

where ```sum_by_lane``` is a two field (tsv) textfile where each line stipulates in the first field the name of the summed OTU entry and the second field, a "+" delimited list of the bracken filenames that should be summed to make said entry
