from modules import WorkWithData
from modules import enums
from modules import Script

##projde všechna witness transakce, pokusí se najít správné - rozhoduje dle prefixu odpovídajícímu inscription
def find_inscription(fileName:str, zacatekWitness:str, inCount:str, DIR:str)->list:
    """
    This function loops through the entire transaction output and returns its data for build RawTX  
        
        :param f BufferedReader: File to read data (bytes)

        :returns: used for build RawTX

        :rtype: str
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
            return extract_inscription(inscription[16:])##odstraním prefix (OP_0, OP_IF .... OP_PUSHBYTES_1 01)
    raise Exception(f"Error: Transaction does not contain inscription")

##pokud se ve witness datech podařilo najít část s inscriptions, projde zbytek a vyextrahuje čistě inscription data zde uložená
def extract_inscription(inscription:str)->list:
    """
    This function is used if a part with inscriptions was found in the witness - it goes through the rest and extracts purely the inscription data stored here
        
        :param inscription str: string with the witness data part that contains the inscription data

        :returns: A list containing 2 values. The value at index 0 contains type of inscription data, the value at index 1 contains the inscription data itself

        :rtype: list of strings
    """
    data = Script.ScriptEvaluation()

    while len(inscription) != 2:
        inscription = data.Execute_opcode(inscription)
    
    return [data.stack[0], "".join(data.stack[2:])]

##zjistí typ inscriptions a uloží ho do správného souboru
def save_inscription(type:str, inscription:str, result_dir:str)->None:
    """
    This function evaluates the inscription type and saves it to the correct file
        
        :param type str: Data inscription type - the file type for data storage depends on it
        :param inscription str: Inscription data to save to file
        :param result_dir str: The path to the folder where the inscription file should be saved (absolute/relative - preferred) - entered when starting the program in the console

        :returns: None
    """
    suffix = enums.InscriptionFileType.convert_hexType_to_suffix(type)
    if suffix.__eq__('Error'):
        data = bytes("!!!unknown type of content!!!\n\ntype: ",'UTF-8') + bytes.fromhex(type) + bytes("\n\ninscription data: " + inscription,'UTF-8')
        WorkWithData.save_file("txt", data, result_dir) 
    else:
        WorkWithData.save_file(suffix, bytes.fromhex(inscription), result_dir) 