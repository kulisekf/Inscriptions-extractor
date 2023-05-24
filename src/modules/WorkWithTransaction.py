from modules import WorkWithData
from io import BufferedReader

##pokusí se najít zadanou transakci. Pokus ji nenajde, vrátí text chyby, pokud ji najde a transakce obsahuje
#witness, vrátí lokaci witness a počet vstupů, pokud witness nebosahuje vrátí text chyby
def find_transaction(fileName:str, zacatekBloku:str, txHash:str, DIR:str)->list:
    """
    This function goes through the individual transactions of the block and tries to find the specified transaction   
        
        :param str fileName: The name of the file where the transaction should be located
        :param str zacatekBloku: The position in the blkXXX.dat file where the data of the block in which the transaction should be located begins
        :param str txHash: Hash of the searched transaction - it is entered when starting the program within the console
        :param str DIR: The path to the folder that contains the blkXXXX.dat files (absolute/relative - preferred) - it is entered when starting the program within the console

        :returns: In case of successful transaction finding + if the transaction contains a witness part return list containing 2 values. The value at index 0 contains the position in the file where the witness part of the data of the searched transaction begins, the value at index 1 contains number of transaction inputs (for subsequent correct evaluation of the witness part)

        :rtype: list of strings    
    """
    f = open(DIR + fileName,'rb') ##otevře správný soubor
    f.seek(int(zacatekBloku) + 8 + 80) ##přeskočí na začátek bloku, následně za magicnumber a size a nakonec za celou hlavičku - následuje pro čtení hodnota tx count
    txCount = int(WorkWithData.read_varint(f),16)##zjisti mnozstvi transakci v bloku - převede z hexadecimal na decimal
    for k in range(txCount):
        RawTX = WorkWithData.reverse(WorkWithData.read_bytes(f,4)) ## obsahuje TX version number
        Witness, inCount, tmpHex = tx_in_count(f) ##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
        RawTX += WorkWithData.reverse(tmpHex)

        ## projdou se všechny vstupy a přidají se do RawTX
        for m in range(inCount):
            RawTX += read_tx_in(f)

        ## zde se zjišťuje počet outputů
        tmpHex, tmpB = WorkWithData.read_varint_transaction(f)
        outputCount = int(tmpHex,16)
        RawTX += WorkWithData.reverse(tmpHex + tmpB)

        ## projdou se všechny výstupy transakce
        for m in range(outputCount):
            RawTX += read_tx_out(f)

        zacatekWitness = f.tell()
        ##postupně přeskočí celou witness část transakce
        if Witness == True:
            skip_witness(f, inCount)

        RawTX += WorkWithData.reverse(WorkWithData.read_bytes(f,4)) ##hodnota Lock time, reversnutá a přidaná
        RawTXHash = WorkWithData.hash_of_data(RawTX)        ## z Rawtx udělá její hash

        ## zjistí, zda nalezl správnou transakci
        if txHash == RawTXHash:
            if Witness == True:
                f.close()
                return [zacatekWitness, inCount] 
            else:
                raise Exception(f"Error: The entered transaction does not contain the witness part")
    f.close()
    raise Exception(f"Error: Non-exist TX hash in this block")

##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
def tx_in_count(f:BufferedReader)->object:
    """
    This function detects the number of inputs to the transaction, evaluates any segwit flag, and at the same time returns a value for building RawTX  
        
        :param f BufferedReader: File to read data (bytes)

        :returns: Returns a total of 3 values - 1. value is witness identifier (True/False); 2. value is number of inputs; 3. value is all the loaded data that the function worked with

        :rtype: bool, int, str 
    """
    Witness = False
    b = f.read(1)
    tmpB = b.hex().upper()
    bInt = int(b.hex(),16)
    tmpHex = ''
    if bInt == 0:
        tmpB = ''
        f.seek(1,1)
        c = f.read(1)
        bInt = int(c.hex(),16)
        tmpB = c.hex().upper()
        Witness = True
    if bInt < 253:
        c = 0
        tmpHex = hex(bInt)[2:].upper().zfill(2)
        tmpB = ''
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = f.read(1)
        b = b.hex().upper()
        tmpHex = b + tmpHex
        
    inCount = int(tmpHex,16)## obsahuje počet vstupů do transakce
    
    tmpHex = tmpHex + tmpB
    return Witness, inCount, tmpHex

#přeskočí celou witness část dat při průchodu transakcí
def skip_witness(f:BufferedReader, inCount:int)->None:
    """
    This function value is all read and skips the entire witness part of the data when passing the transactional data with which the function worked  
        
        :param f BufferedReader: The file from which the data is read
        :param int inCount: Number of transaction inputs - for the witness part to pass correctly, it is necessary to know how many inputs it contains data for

        :returns: None

    """
    for m in range(inCount): ##pro každý vstup
        WitnessLength = int(WorkWithData.read_varint(f),16) ##zjistí počet prvků ve witness
        for j in range(WitnessLength): #pro každý prvek ve witness
            WitnessItemLength = int(WorkWithData.read_varint(f),16) ##zjistí délku prvku
            f.seek(WitnessItemLength, 1) ##přeskočí celý witness prvek

#projde celý vstup transakce a vrátí jeho data pro použití v RawTX
def read_tx_in(f:BufferedReader)->str:
    """
    This function loops through the entire transaction input and returns its data for build RawTX  
        
        :param f BufferedReader: File to read data (bytes)

        :returns: used for build RawTX

        :rtype: str
    """
    tmpHex = WorkWithData.read_bytes(f,32) ## txid (hash) předchozí tx
    RawTX = WorkWithData.reverse(tmpHex)
    
    tmpHex = WorkWithData.read_bytes(f,4) ## index výstupu předchozí tx            
    RawTX += WorkWithData.reverse(tmpHex)
    ##v předsegwitových tx je na tomto místě podpisový skript, zde prázdné - je ve witness -> načte tuto část
    tmpHex, tmpB = WorkWithData.read_varint_transaction(f)
        
    scriptLength = int(tmpHex,16)
    tmpHex = tmpHex + tmpB
    RawTX += WorkWithData.reverse(tmpHex)
    tmpHex = WorkWithData.read_bytes(f,scriptLength,'B')
    RawTX += tmpHex
    ## sequence - časový zámek/RBF
    tmpHex = WorkWithData.read_bytes(f,4,'B')
    RawTX += tmpHex
    return RawTX

def read_tx_out(f:BufferedReader)->str:
    """
    This function loops through the entire transaction output and returns its data for build RawTX  
        
        :param f BufferedReader: File to read data (bytes)

        :returns: used for build RawTX

        :rtype: str
    """
    ## value v sat
    tmpHex = WorkWithData.read_bytes(f,8)
    ## následující část čte scriptPubKey
    RawTX = WorkWithData.reverse(tmpHex)
    tmpHex = ''
    tmpHex, tmpB = WorkWithData.read_varint_transaction(f)

    scriptLength = int(tmpHex,16)
    tmpHex = tmpHex + tmpB
    RawTX = RawTX + WorkWithData.reverse(tmpHex)
    tmpHex = WorkWithData.read_bytes(f,scriptLength,'B')
    RawTX = RawTX + tmpHex
    tmpHex = ''
    return RawTX