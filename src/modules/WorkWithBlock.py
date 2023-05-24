import os
import sys
from modules import WorkWithData

def find_block(blockHash:str, DIR:str)->list:
    """
    This function goes through the blkXXXX.dat files and searches them for the required block based on the block hash value      
        
        :param str blockHash: Hash of the block to be found by the function - it is entered when starting the program within the console
        :param str DIR: The path to the folder that contains the blkXXXX.dat files (absolute/relative - preferred) - it is entered when starting the program within the console

        :returns: A list containing 2 values. The value at index 0 contains the name of the blkXXX.dat file in which the searched block is located, the value at index 1 contains the position in the file where the data of the searched block begins (even before the magic number and block size)

        :rtype: list of strings
    """
    ##nacte slozku a nasledne vsechny soubory do listu
    fList = os.listdir(DIR)
    fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
    fList.sort(reverse=True) ##seřadí list sestupně - inscriptions budou spíše v novějších blocích
    ## postupně projde všechny soubory
    for i in fList:
        ##otevře daný soubor
        nameSrc = i
        f = open(DIR + nameSrc,'rb')
        fSize = os.path.getsize(DIR + nameSrc)
        zacatekBloku = 0
        velikostBloku = 1
        #prochází soubor (každý blok), dokud nenarazí na konec souboru, nebo dokud nenajde hledaný blok - pokud najde, vrátí název souboru a pozici v něm, kde začíná hledaný blok
        while f.tell() != fSize and velikostBloku != 0: #velikost bloku pro to, že poslední soubor (ten do kterého se aktuálně zapisují nové bloky) mi to bez tohoto pravidla procházelo i po přečtení nejaktuálnějšího bloku - jednoduše to skákalo po 8 bajtech
            zacatekBloku = f.tell()
            f.seek(zacatekBloku + 4) ##přeskočí magic number            
            velikostBloku = int(WorkWithData.read_bytes(f,4), base=16)##načte velikost bloku - konvertovaná do bajtů
            hlavickaBloku = WorkWithData.read_bytes(f,80,'B')
            hlavickaBlokuHash = WorkWithData.hash_of_data(hlavickaBloku) #vypočítá hash nalezeného bloku
            if hlavickaBlokuHash.__eq__(blockHash):
                f.close()
                return [i, str(zacatekBloku)]
            taproot_activated_block(hlavickaBlokuHash) #ověří, zda nebyl dosažen aktivační Taproot blok - pokud ano zastaví program
            f.seek(velikostBloku + zacatekBloku + 8,0)#přesun na (konec bloku + 1) - není to přímo začátek dalšího bloku, před ním je ještě magic number a velikost bloku
        f.close()          
    raise Exception(f"Error: Non-exist block hash") ##pokud prošel všechny soubory a požadovaný blockhash nenalezl - neexistuje

#kontroluje, zda nalezený blok odpovídá prvnímu taproot bloku - díky taprootu jsou možné inscriptions
def taproot_activated_block(blockHash:str)->None:
    """
    This function checks whether the found block corresponds to the first taproot block - inscriptions are possible thanks to taproot   
        
        :param str blockHash: block Hash to be compared with the hash of the activation taproot block

        :returns: None - if a matching block hash is found, the user is asked through the console whether the program should continue the evaluation or whether it should end (it is necessary to enter the value Y/N in the console)
    """
    if blockHash == '0000000000000000000687BCA986194DC2C1F949318629B44BB54EC0A94D8244':
        print("Block 709,632 reached (Taproot activated block), continue search? (Y/N)")
        stop = str(input())
        while stop != "N" and stop != "Y":
            print("Wrong value was entered! continue search? (Y/N)\n ->")
            stop = str(input())
        if stop == "Y":
            sys.exit("Search stopped")