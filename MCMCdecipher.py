#!/usr/bin/env python
import numpy as np
import re 
import os
import time
import urllib2

#character map, for mapping chars to the appropriate index
def charmap(c):
	if ord(c)>=65 and ord(c)<=90:
		return ord(c)-65
	elif ord(c)==32:
		return 26

# maps indicies to the appropriate chars
def revmap(n):
	if n>=0 and n<= 25:
		return chr(n + 65)
	elif n == 26:
		return " "

# removes punctuation from each line, capitalizes letters
def cleanstring(text):
	return re.sub(r'[^\w\s]|[\d]','',text).upper() 

# enc of message using a given key 
def enc(msg,key):
	msg = list(msg)
	for i in range(len(msg)):
		msg[i] = revmap(key[charmap(msg[i])])
	msg = ''.join(msg)
	return msg
# decrypts a msg with a key
def dec (msg,key):
	msg = list(msg)
	for i in range(len(msg)):
		msg[i]=revmap(key.index(charmap(msg[i])))
	msg = ''.join(msg)
	return msg
#displays current key as a string
def vkey(key):
	key = list(key)
	for i in range(len(key)):
		key[i] = revmap(key[i])
	key = ''.join(key)
	return key

#plaus function for the m-h algorithm
def plaus(key):
	amt = 0
	guess = dec(msg,key)
	for n in range(len(guess)-1):
		amt += np.log(trans_mat[charmap(guess[n]),charmap(guess[n+1])])
	return amt

identity = list(range(27)) # identity key, c'est boring


print "\n--------NOTE: This is a demonstration of a STOCHASTIC algorithm.  Different runs give different results, even with the same inputs.  If results don't look great the first time, try again!--------\n"

while True:
    try:
        sourceName= raw_input("Please give the FILE NAME of the source text for the transition matrix.  Should be a LONG .txt file.  For default text (War and Peace pulled from Project Gutenberg) type 'default'. \n")
        if sourceName == 'default':
        	source =urllib2.urlopen('http://www.gutenberg.org/cache/epub/2600/pg2600.txt')
    	else:
        	source = open(sourceName,"r") # get text from user
        fname, f_ext = os.path.splitext(sourceName)
        if f_ext != ".txt" and f_ext !='^D' and sourceName!='default':
        	raise ValueError
    except IOError:
        print("\nNot a valid file name. \n")
        continue
    except ValueError:
    	print("\nNot a valid file extension. (needs to be a .txt file, or type 'default' \n")
    	continue 
    else:
    	print("\nReading in source text now...")
        break

trans_mat = np.ones((27,27)) # initializes an empty matrix 
#loop through
sourcelen = 0
for line in source:
	sourcelen += len(line)
	curline = cleanstring(line)
	for n in range(len(curline)-1):
		if curline[n] == "\n" or curline[n+1]=="\n": # might be redundant
			break
		else:
			trans_mat[charmap(curline[n]),charmap(curline[n+1])] += 1


source.close()
print "Done.\n"


true_msg = raw_input("\nPlease enter the message you'd like to encrypt (ideally around 1000+ characters).  For default message type 'default'. \n")
while (True):
	if true_msg == 'default':
		true_msg = "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth"
		break
	elif len(cleanstring(true_msg))<100:
		true_msg = raw_input("\nPlease input a message with at least 100 characters.\n")	
	else:
		break	
true_msg = cleanstring(true_msg)
if len(true_msg)<500:
	print "---------------------------------------------------\n---WARNING: char count low, convergence unlikely---\n---------------------------------------------------"


key = list(np.random.permutation(identity)) # generates a random swapping key
true_key = list(key)
# scrambles the message with the key
msg = enc(true_msg,true_key)

# prints keys for visualization
print "\nOriginal Message: ", true_msg[:80] + "...(continued)"
print "Scrambled Message:", msg[:80] + "...(continued)"
print "\n""Key:", "ABCDEFGHIJKLMNOPQRSTUVWXYZ ", '\n    ', vkey(key), '\n\n'

#character frequency analysis option for intial key selection
freq_an = raw_input("Incorporate frequency analysis (uni-gram attack) for initial proposal key? (y/n)\n")
while True:
	if freq_an == 'y':
		true_freq = " ETAOINSHRDLCUMWFGYPBVKJXQZ" # character frequencies in the english language, descending order
		msg_freq=[]
		for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
			msg_freq.append((c,msg.count(c)))
		msg_freq.sort(key=lambda x: x[1],reverse=True)
		freq=''
		for item in msg_freq:
			freq += item[0]
		key = list(identity)
		for c in true_freq:
			key[charmap(c)]=charmap(freq[true_freq.index(c)])
		break
	elif freq_an == 'n':
		key = list(np.random.permutation(identity))
		break
	else:
		freq_an = raw_input("Please type 'y' or 'n'")

while True:
    try:
        its= int(raw_input("Please give number of iterations you'd like to run the markov chain (1000+ recommended): \n"))
    except ValueError:
        print("Not a valid integer. \n")
        continue
    else:
    	print "Decryption beginning...\n"
        break
print "  0 iterations: ", msg[:80] + "..."



# The M-H algorithm
now = time.time()
for i in range(1,its+1):
	newkey = list(key)
	# random swap proposal
	swap = np.random.randint(27,size=2)
	newkey[swap[0]]=key[swap[1]]
	newkey[swap[1]]=key[swap[0]]
	if plaus(newkey)>=plaus(key):
		key = newkey
	elif np.random.uniform()<np.exp(plaus(newkey)-plaus(key)):
			key = newkey
	if i % 100 == 0 or i == its:
		print i, "iterations: ", dec(msg,key)[:80] + "..."
end = time.time()
#print the final result
print "\nFinal Decryption:\n", dec(msg,key), "\n"

#gets accuracy of final decryption
ac = len([i for i, j in zip(list(true_msg),list(dec(msg,key)))  if i == j])/float(len(msg))


print "\n--------------------Decryption Report--------------------\n"
print "Length of source text: %d" % sourcelen
print "Length of original message (cipher text): %d" % len(msg)
print "Accuracy of final decryption: %f" % ac
print "Number of iterations of chain: %d" % its
print "Frequency analysis for initial proposal key: %s" % freq_an.upper()
print "Total time for M-H algorithm: %r Seconds" % round((end-now),2)
print "\n----------------------------------------------------------\n"
