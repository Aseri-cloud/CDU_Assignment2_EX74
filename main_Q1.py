# """Cipher logic for Q1.

#Encryption rules (apply per character):
#- a–m: shift FORWARD by (shift1 * shift2)
#- n–z: shift BACKWARD by (shift1 + shift2)
#- A–M: shift BACKWARD by (shift1)
#- N–Z: shift FORWARD by (shift2 ** 2)
#- All other characters unchanged.

#Decryption must be the exact inverse of the above.

##**CODE BELOW** - Started the code for the first question - ##Updated## works does everything we need just need to optimise - e.g turn into functions - use the same function to decode etc.
#Maybe add the shift variables to a dict??

f = open("raw_text.txt", 'r')

shift1 = int(input("enter shift value 1: "))
shift2 = int(input("enter shift value 2: "))

# shifting vlaues (could we store this in a dict or tuple?)
shift_lam = shift1 * shift2
shift_lnz = shift1 + shift2
shift_uam = shift1
shift_unz = shift2 * shift2


#Shift modulo 13 to account for large shfiting values - simulates the rotations and the remainder is the shift (Ex. 14 % 13 is 1 so the shift is "14" but is really "1
# ")
shift_lam %= 13
shift_lnz %= 13
shift_unz %= 13
shift_uam %= 13

#Variables for storing the encrypted and decrypted code
code = ''
decode = ''

#to loop through lnes in the text file and then through the characters in the lines
for line in f:
  for ch in line:
    if ch.islower():
      #a-m LOWERCASE
      if ord(ch) >= 97 and ord(ch) <= 109:
        ordval = ord(ch)
        #shifting based on the shift conditions set previously
        cipherValue = ordval + shift_lam
        #this is the wrap around the half alphabet - ex. M shift 3 m -> a ->b -> c (m=c)
        if cipherValue > ord('m'):
          #x is the number of shifts from 'a' is this case
          x = cipherValue - ord('m')
          cipherValue = ord('a') + x-1
        #adding the character to the new  encrypted striong
        code += chr(cipherValue)
      
      #n-z LOWERCASE
      elif ord(ch) >= 110 and ord(ch) <= 122:
        ordval = ord(ch)
        # this is the shifting notice the - for the backward shift
        cipherValue = ordval - shift_lnz

        if cipherValue < ord('n'):
          x = ord('n') - cipherValue
          cipherValue = ord('z') - x+1
        code += chr(cipherValue)
      else:
        code += ch
    #N-Z UPPERCASE
    elif ch.isupper():
      if ord(ch) >= 78 and ord(ch) <= 90:
        ordval = ord(ch)
        cipherValue = ordval + shift_unz

        if cipherValue > ord('Z'):
          x = cipherValue - ord('Z')
          cipherValue = ord('N') + x-1
        code += chr(cipherValue)
      #A-M UPPERCASE
      if ord(ch) >= 65 and ord(ch) <= 77:
        ordval = ord(ch)
        cipherValue = ordval - shift_uam

        if cipherValue < ord('A'):
          x = ord('A') - cipherValue
          cipherValue = ord('M') - x+1
        code += chr(cipherValue)
    else:
      code += ch

#creating the encrypted text file and writing in the encrypted text
with open("encrypted.txt", "w", encoding="utf-8") as f:
    f.write(code)
    



print('\n')


#DECRYPTION METHOD - REVERSING THE SHIFT VALUES
shift_lam = (-shift_lam) %13
shift_lnz = (-shift_lnz) %13
shift_uam = (-shift_uam) %13
shift_unz = (-shift_unz) %13

d = open("encrypted.txt", 'r')

for line in d:
  for ch in line:
      if ch.islower():
        #a-m LOWERCASE
        if ord(ch) >= 97 and ord(ch) <= 109:
          ordval = ord(ch)
          cipherValue = ordval + shift_lam

          if cipherValue > ord('m'):
            x = cipherValue - ord('m')
            cipherValue = ord('a') + x-1
          decode += chr(cipherValue)
        
        #n-z LOWERCASE
        elif ord(ch) >= 110 and ord(ch) <= 122:
          ordval = ord(ch)
          cipherValue = ordval - shift_lnz

          if cipherValue < ord('n'):
            x = ord('n') - cipherValue
            cipherValue = ord('z') - x+1
          decode += chr(cipherValue)
        else:
          decode += ch
      #N-Z UPPERCASE
      elif ch.isupper():
        if ord(ch) >= 78 and ord(ch) <= 90:
          ordval = ord(ch)
          cipherValue = ordval + shift_unz

          if cipherValue > ord('Z'):
            x = cipherValue - ord('Z')
            cipherValue = ord('N') + x-1
          decode += chr(cipherValue)
        #A-M UPPERCASE
        if ord(ch) >= 65 and ord(ch) <= 77:
          ordval = ord(ch)
          cipherValue = ordval - shift_uam

          if cipherValue < ord('A'):
            x = ord('A') - cipherValue
            cipherValue = ord('M') - x+1
          decode += chr(cipherValue)
      else:
        decode += ch

with open("decrypted.txt", "w", encoding="utf-8") as d:
    d.write(decode)
with open('decrypted.txt', 'r') as l:
  check_2 = l.read()

with open('raw_text.txt', 'r') as e:
  check_1 = e.read()

if check_1 == check_2:
  print('success')
else:
  print('fail')

 





f.close()
d.close()
