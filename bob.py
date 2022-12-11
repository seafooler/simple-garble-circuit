import json
from cryptography.fernet import Fernet

def keypair():
    return {0: Fernet.generate_key(), 1: Fernet.generate_key()}

class Gate(object):

    def __init__(self):
        self.table = []

    def create_table(self, table_json):
        for e in table_json:
            self.table.append(bytes(bytearray(e["__value__"])))

    def fire(self, my_inputs):
        fn0 = Fernet(my_inputs[0])
        fn1 = Fernet(my_inputs[1])

        decrypt_table = self.table

        new_table = []
        for ciphertext in decrypt_table:
            dec = None
            try:
                dec = fn1.decrypt(ciphertext)
            except:
                pass
            if dec is not None:
                new_table.append(dec)

        result_table = []
        for ciphertext in new_table:
            dec = None
            try:
                dec = fn0.decrypt(ciphertext)
            except:
                pass
            if dec is not None:
                result_table.append(dec)

        if len(result_table) != 1:
            raise ValueError("decrypt_table should be length 1 after decrypting")
        else:
            print(result_table[0])

with open('table.json') as data_file:
    table_data = json.load(data_file)

with open('my_inputs.json') as data_file:
    my_writes_data = json.load(data_file)

gate = Gate()
gate.create_table(table_data)

my_inputs = []
for mwd in my_writes_data:
    my_inputs.append(bytes(bytearray(mwd["__value__"])))

gate.fire(my_inputs)