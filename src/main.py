import argparse
from workWithBlock import Block
from workWithInscription import Inscription
from workWithTransaction import Transaction


def what_to_find()->list:
    """
    This function uses argparse to retrieve the necessary data entered into the terminal when the application starts and returns it for later use. It also contains a check whether the entered hash values have the appropriate length

        :returns: A list containing 4 values. In this order - the block hash of the block that contains the inscription, the hash of the transaction that contains the inscription, the path to the folder that contains the blkXXXX.dat files and the path to the folder where the inscription is to be stored
    
        :rtype: list of strings 
    """
    parser = argparse.ArgumentParser(description='Extract inscription from block')

    parser.add_argument('-blkHash', required=True, help="hash of block with inscription transaction (required)")
    parser.add_argument('-txHash', required=True, help="transaction hash of transaction with inscription (required)")
    parser.add_argument('-blkDir', default='./.bitcoin/blocks', help="path to the block folder (default: './.bitcoin/blocks')")
    parser.add_argument('-resDir', default='./', help="path to the folder for file save (default: './')")
    args = parser.parse_args()
    DIR = args.blkDir + "/"

    if len(args.blkHash) != 64:
        raise Exception(f"Error: Wrong blkHash value was entered! The hash length does not conform to the standard")
    if len(args.txHash) != 64:
        raise Exception(f"Error: Wrong txHash value was entered! The hash length does not conform to the standard")
    return [args.blkHash.upper(), args.txHash.upper(), DIR, args.resDir]
 
def main():
    """
    The main function, which sequentially calls individual sub-parts while the program is running. At the same time, exception catching is performed at this level
    """
    try:
        coordinates = what_to_find() ##list blockhash, transaction hash
        block = Block()
        block.find_block(coordinates[0], coordinates[2]) ## list nazev souboru .blk ve kterem je hlevany blok, pozice kde blok zacina (pred magicnumber a size)
        
        transaction = Transaction()
        transaction.find_transaction(block.inFile, block.startAtPosition, coordinates[1], coordinates[2]) ##najde zacatek transakce

        inscription = Inscription()
        inscription.find_inscription(block.inFile, transaction.witnessStartAtPosition, transaction.inCount, coordinates[2])
        inscription.save_inscription(coordinates[3])
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()