""" 
Project 1 - Wikipedia Scraping/Crawler
Flavio Stoll Toaldo
Start Date: March 26, 2019
Finish Date(v1): March 30, 2019
"""
# TODO
# * set the word I as an exception
# user can choose between iterate over number of articles or target number 
    # of unique words
# __main__ (???)
# IDEAS:
    # relate words (by their synonims?)
    # plot the information (matplotlib?)
    # implement on a website   
    # keep a list of articles visited, if already visited, go to another one (shoul be extremely rare)
# ---------------------------

import bs4 as bs
import urllib.request
import json
import pandas as pd
import os
from collections import defaultdict

# initiate global variables to be used in multiple functions
word_bank = defaultdict(list)
global_word_counter = 0

def management():
    """ manages the execution, prompts user to choose to iterate over # of articles \
    or # of words found and call functions to complete the execution """

    print("Please choose an option: \n")
    print("[A] Iterate over # of ARTICLES\n[W] Iterate over # WORDS\n")
    option = input(">>> ").lower()
    iterations = 0

    # iterate over # of articles
    if option == 'a':
        # input error handling
        while True:
            try:
                target = int(input("\nNumber of ARTICLES to iterate? "))
                break
            except:
                print("Please choose a number between 1 and 100,000")
        # controls if the target set by the user was reached and stops if true
        while iterations < target:
            web_content = get_random_url()
            word_processing(web_content, option)
            iterations += 1  

    # iterate over # of words
    elif option == 'w':
        # input error handling
        while True:
            try:
                target = int(input("\nNumber of WORDS to analyze? "))
                if target > 50000:
                    print("It may take some time")
                    break
                else: break
            except:
                print("Please choose a number between 1 and 500,000")
        # controls if the target set by the user was reached and stops if true
        while iterations < target:
            web_content = get_random_url()
            iterations = word_processing(web_content, option, word_count_target=target)
    else: 
        print("Not a valid option. Please enter A or W")
        management()

    print_report()
        

def get_random_url():
    """ gets a new link (wikipedia random), creates soup, and find contents of \
        interest """

    source_url =  "https://en.wikipedia.org/wiki/Special:Random"
    # open first link and creat a soup to work with
    source = urllib.request.urlopen(source_url)
    soup = bs.BeautifulSoup(source, "lxml")
    article_name = soup.title.string.replace(" - Wikipedia", '')
    print("Retrieving data from: {}".format(article_name))

    # extract all paragraph tags inside the div tree inside the body
    main_content = soup.find(id="mw-content-text") \
                    .find(class_="mw-parser-output").find_all('p')
    
    return main_content
    

def word_processing(contents, option, word_count_target=0):
    """ cleans every word found, check if it is a valid word by comparing with \
        english dictionary (json) and counts how many times a given word has \
            appeared in the sampling """

    global global_word_counter
    global word_bank

    # opens and load json dicitionary (curated list of english words)
    with open("dict/english_words.json", 'r') as json_dict:
        english_dict = json.load(json_dict)
        # iterate over all words, clean them, check if they are all english and
        # if they are, add to the bank, count frequency and total number of words found
        for paragraph in contents:
            # breaks out of the loop if iterating over number of words and
            # target has been achieved
            if option == 'w' and global_word_counter == word_count_target: break
            else:
                for word in paragraph.text.split():
                    # remove digits, and special characters except "-"
                    clean_word = "".join([c for c in word if c.isalpha() or c == "-"]).lower()
                    # check if word is not empty and that is a valid word
                    if clean_word != "" and clean_word in english_dict:
                        global_word_counter += 1
                        # check if new word
                        if clean_word in word_bank:
                            word_bank[clean_word][0] += 1
                        # increments count of given word, if not a new word
                        else:
                            word_bank[clean_word].append(1)
                        # breaks out of the loop if iterating over number of words and
                        # target has been achieved
                        if option == 'w' and global_word_counter == word_count_target:
                            break
                    else: continue

    return global_word_counter

      
def print_report():
    """ gives the option to print raw dictionary of found words, export as .csv \
        or quit the execution"""

    global global_word_counter
    global word_bank
    unique_words = len(word_bank)

    # total number of words found
    print("\nWords found: {}".format(global_word_counter))
    # unique words found
    print("Unique words found: {}".format(unique_words))
    # unique / total words ratio
    print("{:.0%} of total words found are unique".format(unique_words/global_word_counter))

    # output menu
    print("\nPlease, choose an option:")
    print("[P] Print\n[C] .csv\n[A] Run program again\n\n[Q] Quit\n")

    # error handling for user's input
    while True:
        output_format = input(">>> ").lower()
        if output_format in ('p', 'c', 'a', 'q'): break
        else: print("\nPlease enter a valid option\n")
    
    # print
    if output_format == 'p':
        print("DATA WILL BE LOST AFTER PRINTING\n")
        print(word_bank)

    # .csv using pandas
    elif output_format == 'c':
        for word in word_bank:
            # appends a field to display/store the frequency of the word
            word_bank[word].append(word_bank[word][0] / global_word_counter)
        # creates panda dataframe and transpose, to generate the csv properly
        df = pd.DataFrame(word_bank).transpose()

        # outputs .csv file
        df.to_csv("output/word_freq.csv")

    # run the program again
    elif output_format == 'a':
        os.system("cls")
        # resets global variables to a fresh restart and call initial function
        word_bank = {}
        global_word_counter = 0
        management()

    # quit
    elif output_format == 'q':
        quit()            

    return None

# clear screen and calls first function
os.system("cls")
management()



















