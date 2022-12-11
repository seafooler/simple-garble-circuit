from cryptography.fernet import Fernet
from random import SystemRandom
import json

crypto_rand = SystemRandom()


def custom_to_json(python_object):
    if isinstance(python_object, bytes):
        return {"__class__": "bytes", "__value__": list(python_object)}
    else:
        raise TypeError(repr(python_object) + " not JSON serializable or not bytes.")


def shuffle(l):
    for i in range(len(l)-1, 0, -1):
        j = crypto_rand.randrange(i+1)
        l[i], l[j] = l[j], l[i]


def key_pair():
    return {0: Fernet.generate_key(), 1: Fernet.generate_key()}


class Gate(object):

    gate_ref = {
        "AND": (lambda x, y: x and y),
        "OR": (lambda x, y: x or y),
        "XOR": (lambda x, y: x ^ y)
    }

    def __init__(self, g_id, c_type, inputs):
        self.g_id = g_id
        self.table = []
        self.outputs = [bytes([0]), bytes([1])]
        self.wires = {x: key_pair() for x in inputs}

        f = {}
        for i in (0, 1):
            f[i] = {}
            for j in (0, 1):
                f[i][j] = Fernet(self.wires[i][j])

        for i in range(2):
            for j in range(2):
                if self.gate_ref[c_type](i, j):
                    enc = f[0][i].encrypt(self.outputs[1])
                    self.table.append(f[1][j].encrypt(enc))
                else:
                    enc = f[0][i].encrypt(self.outputs[0])
                    self.table.append(f[1][j].encrypt(enc))

        shuffle(self.table)

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
        # return result_table


gate = Gate(0, 'OR', [0, 1])


def write_json(file_name, j):
    with open(file_name, 'w') as outfile:
        json.dump(j, outfile, default=custom_to_json, separators=(',', ':'))


write_json("table.json", gate.table)

my_input = [gate.wires[0][1], gate.wires[1][0]]

write_json("my_inputs.json", my_input)
gate.fire(my_input)