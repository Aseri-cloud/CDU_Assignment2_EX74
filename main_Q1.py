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

text = open("raw_text.txt", 'r')

shift1 = int(input('>>Enter SHIFT1: '))
shift2 = int(input('>>Enter SHIFT2: '))

print(">>Encryption Proccess: ENGAGED")

def encryption(string1,shift1, shift2):
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
  #to loop through lnes in the text file and then through the characters in the lines

  #Variables for storing the encrypted and decrypted code
  code = ''

  for line in string1:
    for ch in line:
      if ch.islower():
        #a-m LOWERCASE
        if ord(ch) >= 97 and ord(ch) <= 109:
          ordval = ord(ch)
          #the shifting of the ch
          cipherValue = ordval + shift_lam
          #creating the wrap around
          if cipherValue > ord('m'):
            x = cipherValue - ord('m')
            cipherValue = ord('a') + x-1
          code += chr(cipherValue)
        
        #n-z LOWERCASE
        elif ord(ch) >= 110 and ord(ch) <= 122:
          ordval = ord(ch)
          
          #shifting backwards with the minus
          cipherValue = ordval - shift_lnz
          
          #creating the opposite wrap around for the backwards shift
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
    
  return code

test = encryption(text,shift1,shift2)

with open("encrypted_text.txt", "w", encoding="utf-8") as f:
    f.write(test)
    
print(">>Encryption process: COMPLETE")
print(">>Encryption process: ENCRYPTION_TEXT.TXT CREATED")

#decryption  function // using decrypt function same code but the shifts are negative (opposite) to shift back
def decryption(string2,shift1,shift2):

  decode =""
  shift_lam = shift1 * shift2
  shift_lnz = shift1 + shift2
  shift_uam = shift1
  shift_unz = shift2 * shift2

#DECRYPTION METHOD - REVERSING THE SHIFT VALUES
  shift_lam = (-shift_lam) %13
  shift_lnz = (-shift_lnz) %13
  shift_uam = (-shift_uam) %13
  shift_unz = (-shift_unz) %13

  for line in string2:
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
    
  return decode

#assigning the d variable to the encrypted_text file for the decryption

d_txt = open("encrypted_text.txt", 'r')
decode = decryption(d_txt, shift1,shift2)

#UX
print(">>Decryption Protcol: ENGAGED")
print(">>Encryption process: DECRYPTION_TEXT.TXT CREATED")

#verificatioon process
with open("decrypted_text.txt", "w", encoding="utf-8") as d:
    d.write(decode)
with open('decrypted_text.txt', 'r') as l:
  check_2 = l.read()

with open('raw_text.txt', 'r') as e:
  check_1 = e.read()


if check_1 == check_2:
  print('>>Decryption: SUCCESSFUL')
else:
  print('>>Decryption: FAILED')

f.close()
d.close()

    

