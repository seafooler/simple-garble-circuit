A simple implemetation to understand Yao's garble circuit.

This implementation is pretty simplified since:
 - No Oblivious Transfer is utilized
 - Only one gate is considered
 - The output to be encrypted is directly the bit set of {0, 1}. 
 Thus, Bob can get the decrypted value (i.e., 0 or 1) directly. 
 By contrast, in Yao's original protocol, the output to be encrypted
 are also some random string. Therefore, Bob cannot know which bit
 the decrypted value corresponds to. Instead, Bob can only know the bit
 after receiving the extra information from Alice.
 
The only two data sent from Alice to Bob are:
- encrypted and shuffled circuit
- two inputs
 
