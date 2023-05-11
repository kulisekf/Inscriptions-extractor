## Inscriptions extractor

- the application extracts the inscription data from the required transaction and saves it in the required format

## Deploy and run
- prerequisites
    - python version 3
    - the application uses the modules hashlib, os, sys, io and argparse - all of them should be part of python 3 by default
    - bitcoin-core - application directly uses blkXXXXX.dat files, you need to have direct access to these files 

- run the file main.py
    - when running through the terminal, it requires 2 mandatory arguments: 
        - -blkHash BLKHASH -> hash of block with inscription transaction
        - -txHash TYHASH -> transaction hash of transaction with inscription
    - umožňuje zadání 2 volitelných parametrů: 
        - -blkDir BLKDIR -> path to the block folder (default: './.bitcoin/blocks')
        - -resDir RESDIR -> path to the folder for file save (defpříault: './')
    - example:
        - `python3 main.py -blkHash 00000000000000000000b1bdfdb4a667d57b5e5890eebaea608f7bcc0fe9bd63 -txHash 52ed0a201a5b3bde92fe485e8550a78dd03dac71e7488eb61c1e8b5b4a779deb`
        - `python3 main.py -blkDir ./blocks -resDir ./result -blkHash 00000000000000000000b1bdfdb4a667d57b5e5890eebaea608f7bcc0fe9bd63 -txHash 52ed0a201a5b3bde92fe485e8550a78dd03dac71e7488eb61c1e8b5b4a779deb`
    - help can be invoked directly within the terminal:
        - python3 main.py -h

## return value
- does not contain a return value at the end of the program run
- runtime errors will be written to the console
- upon successful completion of the run, no message is written to the console, when inscription data is found and recognized, the data is saved in the correct format to the inscription.xxx file. If the format is not recognized, the resulting data, including information about the required data type, is stored in the inscription.txt file

## inscription search phase
- the course of the program is programmatically divided into 5 parts:
    - obtaining the required data from the values entered into the terminal when the program is started
    - finding the blkXXX.dat file in which the searched block is stored - the result is the return of the file name together with the position where the beginning of the searched block is located
    - finding the desired transaction and return value that represents the initial position of the witness field stored within the blkXXX.dat file
    - extracting inscription data from witness - data type and data itself
    - save to file based on data type
- thanks to the division into several logical parts, the program can be easily modified to serve, for example, as a data parser or to search for other, specific values within a transaction or block
- jednotlivé části a funkce obsahují velké množství komentářů, které napomáhají pochopení funkce části kódu a také s jakými daty určitá část pracuje
    - NOTICE: all comments are in the Czech language