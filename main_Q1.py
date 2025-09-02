# """Cipher logic for Q1.

#Encryption rules (apply per character):
#- a–m: shift FORWARD by (shift1 * shift2)
#- n–z: shift BACKWARD by (shift1 + shift2)
#- A–M: shift BACKWARD by (shift1)
#- N–Z: shift FORWARD by (shift2 ** 2)
#- All other characters unchanged.

#Decryption must be the exact inverse of the above.

##**CODE BELOW** - Started the code for the first question - nearly works just needs a couple of edits and put into a function


f = open("raw_text.txt", 'r')

shift1 = int(input("enter shift value 1: "))
shift2 = int(input("enter shift value 2: "))
shift_lam = shift1 * shift2
shift_lnz = shift1 + shift2
shift_uam = shift1
shift_unz = shift2 * shift2
shift_lam %= 13
shift_lnz %= 13
shift_unz %= 13
shift_uam %= 13
code = ''

for line in f:
  for ch in line:
    if ch.islower():
      #a-m LOWERCASE
      if ord(ch) >= 97 and ord(ch) <= 109:
        ordval = ord(ch)
        cipherValue = ordval + shift_lam

        if cipherValue > ord('m'):
          x = cipherValue - ord('m')
          cipherValue = ord('a') + x-1
        code += chr(cipherValue)
      
      #n-z LOWERCASE
      elif ord(ch) >= 110 and ord(ch) <= 122:
        ordval = ord(ch)
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
print("encrypted:", code)


shift_lam = (-shift_lam) %13
shift_lnz = (-shift_lnz) %13
shift_uam = (-shift_uam) %13
shift_unz = (-shift_unz) %13


for ch in code:
    if ch.islower():
      #a-m LOWERCASE
      if ord(ch) >= 97 and ord(ch) <= 109:
        ordval = ord(ch)
        cipherValue = ordval + shift_lam

        if cipherValue > ord('m'):
          x = cipherValue - ord('m')
          cipherValue = ord('a') + x-1
        code += chr(cipherValue)
      
      #n-z LOWERCASE
      elif ord(ch) >= 110 and ord(ch) <= 122:
        ordval = ord(ch)
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
  
f.close()
print("decrypted:", code)
    

