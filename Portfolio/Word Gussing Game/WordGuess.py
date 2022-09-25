# Portfolio Chapter 5: Word Guess Game
# Tera Parish
# txp200011

import sys
import pathlib
import re
import nltk
from nltk.corpus import stopwords   # stopwords
from nltk.stem import WordNetLemmatizer # lemmatization
from random import randint  # random number


def process_text(raw):
    stepA= [t.lower() for t in raw
                if t.isalpha()
                and len(t)>5
                and t not in stopwords.words('english')]

    # lemmatize the tokens
    wnl= WordNetLemmatizer()
    stepB= list(set([wnl.lemmatize(t) for t in stepA]))

    # POS tagging
    stepC= nltk.pos_tag(stepB)
    print('\nThe first 20 tagged items:')
    print(stepC[:20])

    # create a list of nouns
    stepD= []
    for token, pos in stepC:
        if pos== 'NN' or pos== 'NNS':
            stepD.append(token)

    # print number of tokens, number of nouns
    print("\nNumber of tokens: ", len(stepA))
    print("Number of nouns (NN and NNS): ", len(stepD),)

    return list(stepA), stepD


def guessingGame(wordList):
    print('\n\t_____________________________________________________')
    print('\t☺ Let\'s Play a Word Guessing Game!\n')
    print('\t- You have 5 chance to guess to start with')
    print('\t- Game ends when the total score is negative')
    print('\t- To terminate the game at any point, enter a \'!\'')
    print('\t_____________________________________________________\n\n')

    # pick a random word from the list
    idx = randint(0, 49)
    target = list(wordList[idx])
    guess = ''
    score = 5

    print('\t_________[Start]_________\n')
    # for each letter in the word, print an underscore '_'
    display= list('_' * len(target))
    print('\t'.join(display))
    print('Score:', score)
    guess = input('Guess a letter: ')

    while(guess!= '!' and score> 1):

        # scored
        if (guess in target and guess not in display):
            score += 1

            for c in range(len(target)):
                if (target[c]== guess):
                    display[c]= guess

            # completed
            if ('_' not in display):
                print('\n\t______________________________')
                print('\t╰( ^o^)╮ You got it! ╰( ^o^)╮')
                print('\tThe word was:', ''.join(target))
                print('\t______________________________\n\n')
                print('\n\t_________[New Game]_________\n')

            else:
                print('\n(✯◡✯) Scored!')
                print('\t'.join(display))
                # keep prompting input
                print('Score:', score)
                guess = input('Guess a letter: ')

        # pick a new word
        elif ('_' not in display):
            idx = randint(0, 49)
            target = list(wordList[idx])
            display = list('_' * len(target))
            print('\t'.join(display))
            print('Score:', score)
            guess = input('Guess a letter: ')

        else:
            score-= 1
            print('\nಥ_ಥ Try again!')
            print('\t'.join(display))

            # keep prompting input
            print('Score:', score)
            guess = input('Guess a letter: ')


    print('\n\t_____________________________')
    if (score==1):
        print('\t(⋟﹏⋞) No more guess left...')
        print('\tThe word was:', ''.join(target))

    print('\t_________[Game Over]_________\n\n')


# standard way to start a program
if __name__ == '__main__':
    # check if a system argument is passed in
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    rel_path= sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as file:
        text_in = file.read()

    raw= nltk.word_tokenize(text_in)
    uni= set(raw)

    # lexical diversity
    print('\nLexical diversity: %.2f' %(len(uni)/ len(raw)))

    # process raw text
    tokens, nouns= process_text(raw)

    # dictionary {noun: noun count in tokens}
    dic={n: tokens.count(n) for n in nouns}

    # sort the dictionary by count
    afterSorted= sorted(dic.items(), key=lambda item: item[1], reverse=True)

    # print the 50 most common words
    print('\nThe 50 most common words:')
    for w in afterSorted[:50]:
        print(w)

    # store those 50 words to a list
    words= []
    for w, c in afterSorted[:50]:
        words.append(w)

    guessingGame(words)
