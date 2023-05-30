from modules import WorkWithData
from io import BufferedReader

class Transaction:
    """
    this class is used to work with transaction. 
    
    Attributes
    ----------
        txHash (str) : transaction hash
        witnessStartAtPosition (int) : the position at which the data within the file begins
        fileName (str) : the name of the file in which the transaction is stored
        startAtPosition (str) : the position in the file at which the transaction starts
        witness (bool) : identifies whether the transaction contains a witness
        inCount (int) : identifies the number of inputs to the transaction
        outputCount (int) : identifies the number of outputs from the transaction

    Methods
    -------
        find_transaction(self: object, fileName:str, zacatekBloku:str, txHash:str, DIR:str)->list:
            This method goes through the individual transactions of the block and tries to find the specified transaction   
        tx_in_count(self: object, f:BufferedReader)->str:
            This method detects the number of inputs to the transaction, evaluates any segwit flag and at the same time returns the value for RawTX
        skip_witness(self: object, f:BufferedReader)->None:
            This method skips the entire witness part of the data when traversing the transaction
        read_tx_in(self: object, f:BufferedReader)->str:
            This method goes through the entire transaction input and returns its data for use in RawTX
        read_tx_out(self: object, f:BufferedReader)->str:
            This method goes through the entire transaction output and returns its data for use in RawTX
    """
    def __init__(self: object) -> None:
        """
        Constructs necessary attributes for the object.           

        Parameters
        ----------
            self (object) : class object

        Returns
        -------
            None
        """
        self.txHash = None
        self.witnessStartAtPosition = None
        self.fileName = None
        self.startAtPosition = None
        self.witness = False
        self.inCount = 0
        self.outputCount = 0

    ##pokusí se najít zadanou transakci. Pokus ji nenajde, vrátí text chyby, pokud ji najde a transakce obsahuje
    #witness, vrátí lokaci witness a počet vstupů, pokud witness nebosahuje vrátí text chyby
    def find_transaction(self: object, fileName:str, zacatekBloku:str, txHash:str, DIR:str)->list:
        """
        This method will try to find the specified transaction. The attempt does not find it, it returns an error text, if it finds it and the transaction contains a witness, it terminates the execution of the method and stores the location of the witness and the number of inputs in the object instance, if the witness transaction does not contain it, it returns an error text        
        Parameters
        ----------
            self (object) : class object
            fileName (str) : The name of the file where the transaction should be located
            zacatekBloku (str) : The position in the blkXXX.dat file where the data of the block in which the transaction should be located begins
            txHash (str) : Hash of the searched transaction - it is entered when starting the program within the console
            DIR (str) : The path to the folder that contains the blkXXXX.dat files (absolute/relative - preferred) - it is entered when starting the program within the console

        Returns
        -------
            None - Return is here to end method execution
        """
        self.fileName = fileName
        f = open(DIR + fileName,'rb') ##otevře správný soubor
        f.seek(int(zacatekBloku) + 8 + 80) ##přeskočí na začátek bloku, následně za magicnumber a size a nakonec za celou hlavičku - následuje pro čtení hodnota tx count
        txCount = int(WorkWithData.read_varint(f),16)##zjisti mnozstvi transakci v bloku - převede z hexadecimal na decimal
        for k in range(txCount):
            self.startAtPosition = f.tell()
            RawTX = WorkWithData.reverse(WorkWithData.read_bytes(f,4)) ## obsahuje TX version number
            tmpHex = self.tx_in_count(f) ##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
            RawTX += WorkWithData.reverse(tmpHex)

            ## projdou se všechny vstupy a přidají se do RawTX
            for m in range(self.inCount):
                RawTX += self.read_tx_in(f)

            ## zde se zjišťuje počet outputů
            tmpHex, tmpB = WorkWithData.read_varint_transaction(f)
            self.outputCount = int(tmpHex,16)
            RawTX += WorkWithData.reverse(tmpHex + tmpB)

            ## projdou se všechny výstupy transakce
            for m in range(self.outputCount):
                RawTX += self.read_tx_out(f)

            self.witnessStartAtPosition = f.tell()
            ##postupně přeskočí celou witness část transakce
            if self.witness == True:
                self.skip_witness(f)

            RawTX += WorkWithData.reverse(WorkWithData.read_bytes(f,4)) ##hodnota Lock time, reversnutá a přidaná
            self.txHash = WorkWithData.hash_of_data(RawTX)        ## z Rawtx udělá její hash

            ## zjistí, zda nalezl správnou transakci
            if txHash == self.txHash:
                if self.witness == True:
                    f.close()
                    return
                else:
                    raise Exception(f"Error: The entered transaction does not contain the witness part")
        f.close()
        raise Exception(f"Error: Non-exist TX hash in this block")

    ##zjistí počet vstupů do transakce, vyhodnotí případný segwit flag a zároveň vrátí i hodnotu pro RawTX
    def tx_in_count(self: object, f:BufferedReader)->str:
        """
        This method detects the number of inputs to the transaction, evaluates any segwit flag, and at the same time returns a value for building RawTX  
        
        Parameters
        ----------
            self (object) : class object
            f (BufferedReader) : File to read data (bytes)

        Returns
        -------
            tmpHex (str) : all the loaded data that the function worked with
        """
        self.witness = False
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
            self.witness = True
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
            
        self.inCount = int(tmpHex,16)## obsahuje počet vstupů do transakce
        
        tmpHex = tmpHex + tmpB
        return tmpHex

    #přeskočí celou witness část dat při průchodu transakcí
    def skip_witness(self: object, f:BufferedReader)->None:
        """
        This method skips the entire witness part of the data when going through the transaction. From the object instance, it works with the inCount value, which lets it know how many blocks of witness data it contains        
        
        Parameters
        ----------
            self (object) : class object
            f (BufferedReader) : The file from which the data is read

        Returns
        -------
            None
        """

        for m in range(self.inCount): ##pro každý vstup
            WitnessLength = int(WorkWithData.read_varint(f),16) ##zjistí počet prvků ve witness
            for j in range(WitnessLength): #pro každý prvek ve witness
                WitnessItemLength = int(WorkWithData.read_varint(f),16) ##zjistí délku prvku
                f.seek(WitnessItemLength, 1) ##přeskočí celý witness prvek

    #projde celý vstup transakce a vrátí jeho data pro použití v RawTX
    def read_tx_in(self: object, f:BufferedReader)->str:
        """
        This method loops through the entire transaction input and returns its data for build RawTX          
        
        Parameters
        ----------
            self (object) : class object
            f (BufferedReader) : The file from which the data is read

        Returns
        -------
            RawTX (str) : uses all data using this method - used for build RawTX
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

    def read_tx_out(self: object, f:BufferedReader)->str:
        """
        This method loops through the entire transaction output and returns its data for build RawTX          
        
        Parameters
        ----------
            self (object) : class object
            f (BufferedReader) : The file from which the data is read

        Returns
        -------
            RawTX (str) : uses all data using this method - used for build RawTX
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