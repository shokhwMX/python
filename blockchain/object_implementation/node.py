from utility.verification import Verification
from transaction import Transaction
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet

class Node():

    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        #self.blockchain = None
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        '''
        Accept value from the user to send amount to a recipient via blockchain
        '''
        tx_recipient = input('\nEnter the recipient of the transaction : ')
        tx_amount = float(input('\nEnter the amount please : '))
        return tx_recipient, tx_amount


    def display_blockchain(self):
        #if self.blockchain_exist():
        print('The Blockchain value is : ')
        for block in self.blockchain.chain:
            print(block)


    def get_user_choice(self):
        '''
        Get User choice to perform operations on the Blockchain
        '''
        while True:
            print('\n\tChoose Menu')
            print('\n1. Add a new transaction value')
            print('\n2. Mine a Block')
            print('\n3. Display Chain')
            print('\n4. Validate Blockchain')
            print('\n5. Verify Transactions')
            print('\n6. Create Wallet')
            print('\n7. Load Wallet')
            print('\n8. Save Wallet')
            print('\nQ. Quit')
            ch = input('\nEnter Choice : ')    
            if ch not in ('1','2','3','4','q','Q','5','6','7','8'):
                print('Invalid Choice. Try Again.')
            else:
                return ch


    def listen_for_input(self):
        while True:
            user_input = self.get_user_choice()
            if user_input == '1':
                tx_data = self.get_transaction_value()
                #unpacking tuple
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient,self.wallet.public_key, signature, amount):
                    print('Transaction Added')
                else:
                    print('Transaction Failed')
                #print(open_transactions)
            elif user_input == '2':
                if not self.blockchain.mine_block():
                    print('No Wallet. Mining Failed')
            elif user_input == '3':
                self.display_blockchain()
            elif user_input == '4':
                if Verification.verify_chain(self.blockchain.chain):
                    print('\nThe Blockchain is Valid')
                else:
                    print('\nThe Blockchain has been compromised')
                    break
            elif user_input == '5':
                if Verification.verify_transactions(self.blockchain.get_open_transaction, self.blockchain.get_balances):
                    print('Valid Transactions')
                else:
                    print('Invalid Transactions')
            elif user_input == '6':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_input == '7':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_input == '8':
                self.wallet.save_keys()
            else:
                break
            print('New Balance for {} : {:10.2f}'.format(self.wallet.public_key, self.blockchain.get_balances()))
            if not Verification.verify_chain(self.blockchain.chain):
                print('\nThe Blockchain has been compromised')
                break

if __name__ == "__main__":
    node = Node()
    node.listen_for_input()