# Reference material for A Basic Guide to Bug Hunting with Ghidra

The script `GenPyGDB.py` is a Ghidra Python script which generates GDB Python scripts for tracing a program.

An example output, `gdb_script.py` has been provided for `CommandServer`. 

This can be regenerated through Ghidra by following the process in the [PDF](writeup.pdf).

## To test the GDB script:
```
docker build -t ghidra_gdb .
docker run -it ghidra_gdb gdb -q -x gdb_script.py CommandServer
```

## From antother terminal, run:
```
docker exec -it $(docker ps --filter ancestor=ghidra_gdb --format "{{.Names}}") ./CommandClient.py 1 /etc/issue 127.0.0.1:8080
```


