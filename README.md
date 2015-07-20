# MCMC
Demonstration of an MCMC technique for cracking substitution ciphers.

--------------
General Matter
--------------

-Just run the python script from the command line.

-The user is prompted first to supply a large sample of the english language.  This will record
one-step transition probabilities of letters in the provided text in an array.

-The user is then prompted for a message to be randomly encrypted via a substitution cipher,
and then decrypted using the MCMC technique.  See bcboniece.wordpress.com for more mathematical detail.

-Added an option to include an "intelligent" starting point for the markov chain using character
frequency analysis.
