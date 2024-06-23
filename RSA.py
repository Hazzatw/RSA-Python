#RSA
import math
import random


def IsPrime(number): # using the Miller-Rabin probabilistic primality test
    if number%2 == 0:      #eliminates even numbers
        return(False)
    m = number-1    # sets m to the number below the testing number
    k=0
    while m%2 == 0:
        k=k+1               #n-1=2^k*m find k and m where n is the number
        m= m / (2)
    a = random.randint(2,number-2)                   # a = a<=a<=n-1
    b0 =  pow(int(a),int(m),int(number))                          # b0 = a^m (mod n)
    if b0 == 1 or b0 == number-1:
        return(True)                 # miller-rabin equation is satisfied
    else:
        Result = False
        points = 0
        while Result == False:
            points = points+1
            b0 = pow(b0,2,number)   # b0^2 mod number
            if b0 == 1:              # if 1 satisfied
                Result = True
                return(False)
            elif b0 == number-1:          # if m satisfied
                return(True)
                Result = True
            elif points >= k-1:                 # prevents infinite loop
                return(False)
                Result = True
def PrimeGenerator(repeat):
    Found = False
    while Found==False:        #generates numbers until one is prime
        number = random.randint(pow(10,16),pow(10,20))  # generates random numbers between 10^16 and 10^20,     #numbers big enough to be effective
        if number == repeat:
            Found = False                     # prevent the same prime number twice
        elif IsPrime(number) == True:         # puts it through the primality test
            Found = True
            return(number)           # when a number is prime it is returned

def gcd(a, b):   # standard greatest common divisor
    while b != 0:
        a, b = b, a % b # a is set to b, and b = a%b
    return a     # when b = 0, a%b = 0 so a divisor has been found

def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:                 # extended euclidean algorithm for an extended gcd
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0         # outputs greatest common divisor as well as Bézout coefficients


def ModularInverse(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:      # if mod inv of e, phi(n) = 1, d*emod(phi(n) = 1 has been satisfied
        return x % n

def KeyGenerator():
    p = PrimeGenerator(0) # generates a prime number
    q = PrimeGenerator(p) # generates a second prime number
    n = p*q            # n is the product of these primes
    PHIn = (p-1)*(q-1)    # phi(n) is equal to (p-1)(q-1) as they are prime
    e = random.randint(1,PHIn) # the first condition of e is its between 1 and phi(n), so that's range of numbers
    g=gcd(e,PHIn)  # finds greatest common divisor of random number and phi(n)
    while g != 1:               # when the greatest common divisor is not 1 e is a coprime,
        e = random.randrange(1, PHIn)
        g = gcd(e, PHIn) # continues this until a valid value for e is found, that meets the two conditions
    d =  ModularInverse(e,PHIn)  # d*emod(phi(n) =1 , therefore mod inverse of e and phi(n) should = 1
    return(n,e,d)   # retruns n which is needed for both keys as well as the e and d values

def RSAEncrypt(Plainntext,Publickey,n): # need to have already generated keys
    CipherText = ""
    for i in Plainntext:
        charcter = ord(i)     # turns letter into numeric representation
        cipherLetter = str(pow(charcter,int(Publickey),int(n))) # character^e mod n to encrypt
        CipherText = CipherText + " " + cipherLetter # spaces to separate characters as they now large numbers
    return(CipherText)

def RSADecrypt(CipherText,privatekey,n):
    letter = pow(int(CipherText),int(privatekey),int(n)) # character^d mod n
    letter=chr(letter)   # decrypts a letter at a time
    return(letter)