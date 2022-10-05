'''
Authors: Bridgette Bryant, Tera Parish
NetIDs: BMB180001, TXP200011



'''

import pickle
import math
from nltk import word_tokenize
from nltk import ngrams

def calc_prob(text, unigram_dict, bigram_dict, NUM_TOKENS, VOCAB_SIZE):

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p_laplace = p_laplace * ((n + 1) / (d + VOCAB_SIZE))

    #print("probability with laplace smoothing is ", p_laplace)

    return p_laplace

if __name__ == '__main__':

    # Load in all the pickle files (containing dictionaries)
    uni_eng_dict = pickle.load(open('uni_English.pickle', 'rb'))
    uni_fch_dict = pickle.load(open('uni_French.pickle', 'rb'))
    uni_itl_dict = pickle.load(open('uni_Italian.pickle', 'rb'))

    bi_eng_dict = pickle.load(open('bi_English.pickle', 'rb'))
    bi_fch_dict = pickle.load(open('bi_French.pickle', 'rb'))
    bi_itl_dict = pickle.load(open('bi_Italian.pickle', 'rb'))

    # Set the NUM_TOKENS and NUM_VOCAB for each language
    eng_num_tokens = 0
    eng_num_vocab = len(uni_eng_dict)
    fch_num_tokens = 0
    fch_num_vocab = len(uni_fch_dict)
    itl_num_tokens = 0
    itl_num_vocab = len(uni_itl_dict)

    # Adds up the values from the dictionary to get the size from the number of tokens

    # For english dictionary
    for n in uni_eng_dict.values():
        eng_num_tokens = eng_num_tokens + n

    #print("eng_num_tokens: ", eng_num_tokens)

    # For french dictionary
    for n in uni_fch_dict.values():
        fch_num_tokens = fch_num_tokens + n

    #print("fch_num_tokens: ", fch_num_tokens)

    # For italian dictionary
    for n in uni_itl_dict.values():
        itl_num_tokens = itl_num_tokens + n

    #print("itl_num_tokens: ", itl_num_tokens)


    # Open test text file and save the lines as separate lines
    with open('LangId.test', 'r', encoding="utf-8") as test_file:
        test_text_lines = test_file.read().splitlines()

    # Create and open a predictions file which will say our language prediction on each line
    with open('LangId.predict', 'w', encoding="utf-8") as predict_file:

        line_num = 1    # The current line we are on in test and predict file

        # Iterate through each line of the test file lines and get the probabilities for each
        for line in test_text_lines:
            #print(line)
            # For english
            eng_p = calc_prob(line, uni_eng_dict, bi_eng_dict, eng_num_tokens, eng_num_vocab + fch_num_vocab + itl_num_vocab)
            # For french
            fch_p = calc_prob(line, uni_fch_dict, bi_fch_dict, fch_num_tokens, eng_num_vocab + fch_num_vocab + itl_num_vocab)
            # For italian
            itl_p = calc_prob(line, uni_itl_dict, bi_itl_dict, itl_num_tokens, eng_num_vocab + fch_num_vocab + itl_num_vocab)

            prediction = ""
            # Take the highest of the three probabilities
            # If english is the highest
            if eng_p == max(eng_p, fch_p, itl_p):
                prediction = str(line_num) + " English\n"
            elif fch_p == max(eng_p, fch_p, itl_p): # If french is the highest
                prediction = str(line_num) + " French\n"
            else: # Otherwise italian must be the highest
                prediction = str(line_num) + " Italian\n"

            # Write the line to our prediction file
            predict_file.write(prediction)
            # Increment line_num
            line_num = line_num + 1


    # Get accuracy by comparing the predictions and solutions files
    with open('LangId.sol', 'r', encoding="utf-8") as solution_file:
        with open('LangId.predict', 'r', encoding="utf-8") as prediction_file:

            solution_lines = solution_file.readlines()
            prediction_lines = prediction_file.readlines()

            total_num = 0   # the total number of predictions
            correct_num = 0 # the number of correct predictions
            incorrect_line_numbers = []     # The list of incorrect line numbers

            # For each line in both files
            for sol_line, pred_line in enumerate(prediction_lines):
                # Split both to only test if the last part (language name) matches
                sol_lang = (solution_lines[sol_line].split())[1]
                pred_lang = (pred_line.split())[1]

                # If the match (correct prediction)
                if pred_lang == sol_lang:
                    # Add to the number of correct predictions
                    correct_num = correct_num + 1
                else:
                    # Add the line number to the incorrect number of line numbers list
                    incorrect_line_numbers.append((solution_lines[sol_line].split())[0])

                # Increment total_num (total number of predictions
                total_num = total_num + 1

            # Calculate and print the accuracy
            accuracy = (correct_num / total_num) * 100

            print("Accuracy: ", accuracy)

            # Print the incorrect line numbers list
            print("Incorrect Line Numbers:")
            for l in incorrect_line_numbers:
                print(l)
