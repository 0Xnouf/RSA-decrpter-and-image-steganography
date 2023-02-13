import random
from pathlib import Path
from stegano import lsb
import cv2
import os.path
#color
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
BOLD = "\033[;1m"
pink = '\033[95m'


def generatePrimeNumber():  #geneate prime number
     num=random.randint(3,1000)  #start from 3 to ensure not select number <=2

     if (num % 2 == 0): #to verify that it is an odd number
         return False

     accu = True
     for i in range(2, num): #to get the prime
            if num % i == 0: #to ensure it is prime "Not divisible by any number except 1 and itself --> its prime
                return False
     return num

def checkPrimeNumbers(): #check the required condition of the selected prime numbers
    prime1=generatePrimeNumber() #generate value of p
    prime2=generatePrimeNumber() #generate value of q

    if (prime1==prime2): #change the values if they are equal to each other
        generatePrimeNumber()

    while(not prime1): #so it is any number, to ensure that the returend value is not "False"
        prime1 = generatePrimeNumber() #if it is False, it will change the value until it get a correct prime number
        if prime1: #if the value selected correctly then continue, if it is any number the condition will be true
            pass

    while(not prime2): #to ensure that the returend value is not "False", if it is any number the condition will be false
        prime2 = generatePrimeNumber()  #if the value of the number "False", it will change the value until it get a correct prime number
        if prime2: #if the value selected correctly then continue, if it is any number the condition will be true
            pass

    return prime1,prime2

def GCD(e,phi): #to get the gcd between the given values
    while phi != 0: #MATH THEOREM: if gcd(a,0) then return a, so here we test for gcd(e,phi)
        e, phi = phi, e % phi #MATH THEOREM: to find gcd(a,b) recursive call for gcd(b,a%b) untill it become gcd(a,0)
    return e

def findInverseOfE(e,phi,N): #to find the inverse of the public key(defined here as e), which will be the private key(defined here as d)
    for d in range(1,N):
        rem=((e*d)%phi) #to find the inverse of e it shoud met this condition, (e*d=1 mod phi), "phi=(p-1)*(q-1), where p and q is primes
        if rem==1: # if the reminder 1 between e and d applying mod N, then we find the private key(defined here as d)
            return d

def generatekeys(): #to generate the required keys for the encryption and decryption
    p,q=checkPrimeNumbers() #two prime numbers
    N=p*q #a composite number of two primes
    phi=((p-1)*(q-1)) #clculate the phi
    e=random.randint(1,phi) #choose any value of e, which will be the private key

    while GCD(e,phi) != 1: #to ensure that the e "the private key has an inverse, the gcd(e,phi) should be 1
        e = random.randint(1, phi) #if the gcd(e,phi) not equal 1, then choose another value of e, until the condition is met

    d=findInverseOfE(e,phi,N) #this is the private key which is the inverse of e

    # print("the p:", p)  # to check the correctness of the number
    # print("the q:", q)  # to check the correctness of the number
    # print("the N:", N)  # to check the correctness of the number
    # print("the phi:", phi)  # to check the correctness of the number
    # print("the e:", e)  # to check the correctness of the number
    # print("the d:", d)  # to check the correctness of the number

    return N,e,d

def encrypt(plainText,publicKey,N):
    e=publicKey
    chipertextList=[]
    cipherText=""

    for char in plainText:
        asciiValue=ord(char) #the ascii code correponding to the char
        #print("The ascii: char",asciiValue)
        c=((asciiValue**e)%N) #to encrypt the char (c=m^e mod N)
        chipertextList.append(c)
        #print(c)

    for i in chipertextList:
        cipherText+=str(i) #to get the char corresponding to the ascii code and convert it to str to concatenate

    return chipertextList,cipherText

def decrypt(cipherText,privateKey,N):
    d=privateKey
    plainText=""

    for char in cipherText:
        m=((int(char)**d)%N) #to decrypt the char (m=c^d mod N),
        #print("The ascii of m: ",m) #to check the ascii code
        plainText += str(chr(m)) #concatenate the strings to retrive the whole original text
        #print(str(chr(m)))

    return plainText


def encryptText():
    N, publicKey, privateKey = generatekeys()  # retrive the required values from the function
    plainText = input("Enter a taxt: ")
    cipherTextlist, cipherText = encrypt(plainText, publicKey, N)
    originalText = decrypt(cipherTextlist, privateKey, N)
    print("The text you entered: ", plainText)  # which the user entered in line 101
    print("The ciphertext (encrypted): ", cipherText)  # which the encrypt function returend in line 102
    print("The plaintext (decrypted): ", originalText)  # which the decrypt function returend in line 103
    menu()

def encryptFile():
    N, publicKey, privateKey = generatekeys()  # retrive the required values from the function
    plainTextFileList=[]
    cipherTextlist=[]
    e=publicKey
    i=0
    pathOfFile = input("Enter the path of the file: ")
    path=(Path(pathOfFile))
    if path.is_file()==True:
        fP = open(pathOfFile,'r')
        while (True):
            plainTextFileList.append(fP.read(1))
            if not plainTextFileList[i]:
                plainTextFileList=plainTextFileList[0:len(plainTextFileList)-1]
                break
            i += 1
        fP.close()

    else:
        print("Incorrect path of a file!")
        encryptFile()
    #print(plainTextFileList)
    i=0
    fC = open("encryptedText.txt", "a")
    for char in plainTextFileList:
        asciiValue = ord(char)  # the ascii code corresponding to the char
        #print("The ascii: char",asciiValue)
        c = ((asciiValue ** e) % N)  # to encrypt the char (c=m^e mod N)
        cipherTextlist.append(c)
        #print("The c: char",c)
        fC.write(str(cipherTextlist[i]))
        i += 1
    fC.close()
    #print(cipherTextlist)

    print("The encryption done successfully, with file name: encryptedText.txt\n")
    decryptFile(cipherTextlist, privateKey, N)


    menu()

def decryptFile(cipherTextlist, privateKey, N):
    d = privateKey
    plainText = ""
    fO = open("originalText.txt", "a")
    for char in cipherTextlist:
        m = ((int(char) ** d) % N)  # to decrypt the char (m=c^d mod N),
        fO.write(str(chr(m)))  # concatenate the strings to retreive the whole original text
    fO.close()
    print("The decryption done successfully, with file name: originalText.txt\n")

    #print("The text you entered: ", plainTextF)  # which the user entered in line 101
    #print("The ciphertext (encrypted): ", cipherText)  # which the encrypt function returend in line 102
    #print("The plaintext (decrypted): ", originalText)  # which the decrypt function returend in line 103

def steganoEmb():  #to hide any message in image
  im= input("Enter image name that you want to hide text in it, with extension: ")
  if(not(os.path.exists(im))): #to check if image exist
   print(" image does not exist , please enter correct name with ex")
   steganoEmb()
  text = input("Enter Text that you want to hide it : ") #hidden message
  z=lsb.hide(im,text)
  z.save("Secret.png") #save new image
  print("")
  menu()

def steganoExt(): #This method will extract hidden message in image
    try:
      x=input("Enter image name that you want to extract text from ,with extension  : ")
      OutMessage = lsb.reveal(x)
      print("The hidden Message is :", OutMessage)
    except Exception as e :
        print("Error :",e)

    menu()

def menu():
    print(WHITE,"Choose what you want to do:")
    ch=int(input("1- Encrypt a normal text \n2- Encrypt a content of file \n3- Hide data inside image \n4- Extract data from image \n5- Exit \n"))
    if ch==1:
        encryptText()
    if ch==2:
        encryptFile()
    if ch==3:
        steganoEmb()
    if ch==4:
        steganoExt()
    if ch==5:
        print("~I hope you enjoyed with us!, Thank you.")
        print("----------------------------------------")
        print("~Team members:")
        print("Asma Alanazi \nLayan Musbah \nNouf Alzahrani \nShahad Alshalawi \nWaad Almulhim")
        print("---------------")
        print("~Supervised by:")
        print("Mr. Hussain Alattas")
        quit()

    if ch!=1 or ch!=2 or ch!=3 or ch!=4 or ch!=5:
        print("Incorrect input! choose either 1, 2, 3, 4 or 5:")
        menu()



if __name__ == "__main__":
    print(BOLD,CYAN,"-------------------WELCOME TO OUR SYSTEM-------------------")
    print(BOLD,BLUE,"You will live an enjoyable cryptography experience with us!")
    print(BOLD,CYAN,"-----------------------------------------------------------\n")
    menu()
