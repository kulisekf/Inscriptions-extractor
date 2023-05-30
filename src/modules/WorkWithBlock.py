import os
import sys
from modules import WorkWithData

class Block:
    """
    this class is used to work with Bitcoin block. 
    
    Attributes
    ----------
        inFile (str) : the name of the XXXX.blk file that contains the given block
        startAtPosition (int) : represents the position at which the block starts in the given file
        blockHash (str) : block hash

    Methods
    -------
        find_block(self: object, blockHash:str, DIR:str)->list:
            This method goes through the blkXXXX.dat files and searches them for the required block based on the block hash value   
        taproot_activated_block(blockHash:str)->None:
            During the file search based on the block hash, it checks if the Taproot activation block has not been reached
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
        self.inFile = None
        self.startAtPosition = None
        self.blockHash = None

    def find_block(self: object, blockHash:str, DIR:str)->list:
        """
        Method parameters contain values to search for the block in XXXX.blk files. This method will use these values and go through each file until it finds a matching block (based on the block hash). Subsequently, it terminates its activity, with the block hash, the file in which the block is located and the position at which the block starts within the file remaining within the instance of the object.   

        Parameters
        ----------
            self (object) : class object
            blockHash (str) : Hash of the block to be found by the function - it is entered when starting the program within the console
            DIR (str) : The path to the folder that contains the blkXXXX.dat files (absolute/relative - preferred) - it is entered when starting the program within the console
            
        Returns
        -------
            None
        """

        ##nacte slozku a nasledne vsechny soubory do listu
        fList = os.listdir(DIR)
        fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
        fList.sort(reverse=True) ##seřadí list sestupně - inscriptions budou spíše v novějších blocích
        ## postupně projde všechny soubory
        for i in fList:
            ##otevře daný soubor
            self.inFile = i
            f = open(DIR + self.inFile,'rb')
            fSize = os.path.getsize(DIR + self.inFile)
            velikostBloku = 1
            #prochází soubor (každý blok), dokud nenarazí na konec souboru, nebo dokud nenajde hledaný blok - pokud najde, vrátí název souboru a pozici v něm, kde začíná hledaný blok
            while f.tell() != fSize and velikostBloku != 0: #velikost bloku pro to, že poslední soubor (ten do kterého se aktuálně zapisují nové bloky) mi to bez tohoto pravidla procházelo i po přečtení nejaktuálnějšího bloku - jednoduše to skákalo po 8 bajtech
                self.startAtPosition = f.tell()
                f.seek(self.startAtPosition + 4) ##přeskočí magic number            
                velikostBloku = int(WorkWithData.read_bytes(f,4), base=16)##načte velikost bloku - konvertovaná do bajtů
                hlavickaBloku = WorkWithData.read_bytes(f,80,'B')
                self.blockHash = WorkWithData.hash_of_data(hlavickaBloku) #vypočítá hash nalezeného bloku
                if self.blockHash.__eq__(blockHash):
                    f.close()
                    return
                Block.taproot_activated_block(self.blockHash) #ověří, zda nebyl dosažen aktivační Taproot blok - pokud ano zastaví program
                f.seek(velikostBloku + self.startAtPosition + 8,0)#přesun na (konec bloku + 1) - není to přímo začátek dalšího bloku, před ním je ještě magic number a velikost bloku
            f.close()          
        raise Exception(f"Error: Non-exist block hash") ##pokud prošel všechny soubory a požadovaný blockhash nenalezl - neexistuje

    #kontroluje, zda nalezený blok odpovídá prvnímu taproot bloku - díky taprootu jsou možné inscriptions
    def taproot_activated_block(blockHash:str)->None:
        """
        This function checks whether the found block corresponds to the first taproot block - inscriptions are possible thanks to taproot. If the block has been reached, a warning will be written to the console and the program will wait for the user to enter a value representing whether the search should be stopped or not

        Parameters
        ----------
            blockHash (str) : hash of the block to be compared to the taproot activating block hash
            
        Returns
        -------
            None
        """
        if blockHash == '0000000000000000000687BCA986194DC2C1F949318629B44BB54EC0A94D8244':
            print("Block 709,632 reached (Taproot activated block), continue search? (Y/N)")
            stop = str(input())
            while stop != "N" and stop != "Y":
                print("Wrong value was entered! continue search? (Y/N)\n ->")
                stop = str(input())
            if stop == "N":
                sys.exit("Search stopped")
            elif stop == "Y":
                print("The search continues")