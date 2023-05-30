from modules import WorkWithData
from modules import enums
from modules import Script

class Inscription:
    """
    this class is used to work with inscription. 
    
    Attributes
    ----------
        type (str) : inscription type in hex format stored in a string according to the inscription standard
        data (int) : content inscription data

    Methods
    -------
        find_inscription(self, fileName:str, zacatekWitness:str, inCount:str, DIR:str)->list:
            This method it goes through all witness transactions, tries to find the correct one - decides according to the prefix corresponding to the inscription
        extract_inscription(self, inscription:str):
            if a section with inscriptions was found in the witness data, it creates an instance of the ScriptEvaluation class from Script and uses it to process the content of the inscription data
        save_inscription(self, result_dir:str)->None:
            This method detects the inscriptions type and saves it to the correct file
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
        self.type = None
        self.data = None

    ##projde všechna witness transakce, pokusí se najít správné - rozhoduje dle prefixu odpovídajícímu inscription
    def find_inscription(self: object, fileName:str, zacatekWitness:str, inCount:str, DIR:str)->list:
        """
        Based on information about the number of transaction inputs and the beginning of the witness block, this method goes through the entire witness and looks for the block containing the inscription - based on the prefix that corresponds to the inscription standard (OP_0, OP_IF .... OP_PUSHBYTES_1 01)
        
        Parameters
        ----------
            self (object) : class object
            fileName (str) : the name of the file that contains the block with the transaction containing the inscription
            zacatekWitness (str) : the beginning of the witness part of the data within the file
            inCount (str) : the number of entries of the transaction that contains the inscription
            DIR (str) : the folder where the XXXX.blk files with the blocks are located

        Returns
        -------
            None - Return is here to end method execution
        """

        f = open(DIR + fileName,'rb')
        f.seek(zacatekWitness)
        inscription = ""
        ## pro každý ze vstupů - bude nejspíše 1, ale sichr je sichr
        for m in range(inCount):
            tmpHex = WorkWithData.read_varint(f)

            #přeskočí první část witness - nepotřebuji, myslím že pubkey
            WitnessItemLength = int(WorkWithData.read_varint(f),16)
            f.seek(WitnessItemLength, 1)

            ##načtu 2. část witness
            tmpHex = WorkWithData.read_varint(f)
            WitnessItemLength = int(tmpHex,16)
            tmpHex = WorkWithData.reverse(WorkWithData.read_bytes(f,WitnessItemLength))
            f.close()
            inscription += tmpHex
            tmpHex = ''

            inscription = inscription[68:] ##smažu část witness - signature a OP_CHECKSIG
            
            ## z ničeho nic se to objevilo, zatím jsem nenašel co to má být, tak prostě přeskakuji
            if inscription[0:2] == "06":
                inscription = inscription[16:]
            ## zjistí, zda se jedná o inscriptions - shodný prefix
            if inscription[0:16] == "0063036F72640101":
                return self.extract_inscription(inscription[16:])##odstraním prefix (OP_0, OP_IF .... OP_PUSHBYTES_1 01)
        raise Exception(f"Error: Transaction does not contain inscription")

    ##pokud se ve witness datech podařilo najít část s inscriptions, projde zbytek a vyextrahuje čistě inscription data zde uložená
    def extract_inscription(self: object, inscription:str) -> None:
        """
        This method is used if a part with inscriptions was found in the witness - it goes through the rest and extracts purely the inscription data stored here
        
        Parameters
        ----------
            self (object) : class object
            inscription (str) : string with the witness data part that contains the inscription data

        Returns
        -------
            None
        """
        data = Script.ScriptEvaluation()

        while len(inscription) != 2:
            inscription = data.Execute_opcode(inscription)
        
        self.data = "".join(data.stack[2:])
        self.type = data.stack[0]

    ##zjistí typ inscriptions a uloží ho do správného souboru
    def save_inscription(self: object, result_dir:str)->None:
        """
        This method evaluates the inscription type and saves it to the correct file
        
        Parameters
        ----------
            self (object) : class object - contains inscription data to be saved to a file
            result_dir (str) : The path to the folder where the inscription file should be saved (absolute/relative - preferred) - entered when starting the program in the console

        Returns
        -------
            None
        """
        suffix = enums.InscriptionFileType.convert_hexType_to_suffix(self.type)
        if suffix.__eq__('Error'):
            data = bytes("!!!unknown type of content!!!\n\ntype: ",'UTF-8') + bytes.fromhex(self.type) + bytes("\n\ninscription data: " + self.data,'UTF-8')
            WorkWithData.save_file("txt", data, result_dir) 
        else:
            WorkWithData.save_file(suffix, bytes.fromhex(self.data), result_dir) 