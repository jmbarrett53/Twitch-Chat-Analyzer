import pandas as pd
import os
import csv
import keyboard
import time
from textblob.classifiers import NaiveBayesClassifier
import tkinter
from tkinter import filedialog





def get_output_file_name():
    file_name = input("What would you like to call the cleaned and updated .csv file? (Just the name)" + "\n")
    return file_name

# If you are given a list of strings can you write those to a .csv file?
def write_new_file(input_list, file_name):
    """
    Given a list and a String representing a file name, create a new .csv
    file with that name

    Note: The input must end with .csv
    """
    with open(file_name, mode = "w", errors = "ignore", newline = "") as csvfile:
        csvwriter = csv.writer(csvfile)
        try:
            csvwriter.writerows(input_list)

        except UnicodeDecodeError:
            print("AHHHHH there's an error!!")
        
    print("Check " + file_name + " for your output")

def clean_and_train():
    """
    This code reads in an input .txt file and shaves off the time that the
    comment was made and the name of the commenter
    Lines are still displayed in the order that they were sent
    This code also skips any lines where character encoding gets weird

    IMPORTANT: The twitch chat downloader gives us a .txt file, and the
    textblob library uses .csv ones
    """
    # Prompt user for input and remember
    print("Please select your uncleaned text file." + "\n")
    time.sleep(1)
    input_file = filedialog.askopenfilename()
    output_file = 'temporary output file name'

    # Create a list that will store Strings representing individual comments
    extracted_lines = []

    # Open file and skip lines that cant be decoded
    with open(input_file, "r", encoding = "utf-8", errors = "ignore") as file:
        for line in file:
            try:
                # split based on the only colon in the string,
                # everything after colon is actual comment made by twitch audience member
                parts = line.split(": ", 1)
                if len(parts) > 1:
                    extracted_lines.append(parts[1].strip())
            except UnicodeDecodeError:
                #skip lines that can't be decoded
                continue
    
    # Write to a .csv output file
    with open(output_file, "w", encoding = "utf-8", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        for line in extracted_lines:
            writer.writerow([line])
       
    # close files
    file.close()
    csvfile.close()
    

    # Given a file name, return an updated list containing all of the updated strings
    # that are formatted to the TextBlob standard for sentiment analysis
    
    #create a way to remember updated .csv lines
    global_list = []

    print("Press p to rate a comment as positive")
    print("Press n to rate a comment as negative")
    print("Press q to quit/end early (Ratings will be saved)")
    # Open the csv file that has been cleaned
    with open(output_file, mode = "r", errors = "ignore") as csv_file:
        reader = csv.reader(csv_file)
        while True:
            try:
                for lines in reader:
                    # lines here is a list containing a single string
                    lines = "".join(lines)
                    # lines is now a string

                    # wait because keyboard input can cause issues depending on machine
                    time.sleep(0.12)
                    print(lines)
                    letter_entered = keyboard.read_key()

                    # I decided to use keyboard.read_key() instead of input because
                    # I believe not having to press enter will save more time
                    # letter_entered = input(lines)
                    if letter_entered == "p":
                        # We can access individual lines here
                        # append ",pos" to line
                        new_line = [lines, "pos"]
                        global_list.append(new_line)
                        print("Rated Positive!" + "\n")
                        # then break
                        break
                    
                    if letter_entered == "n":
                        new_line = [lines, "neg"]
                        global_list.append(new_line)
                        print("Rated Negative!" + "\n")
                        break

                    if letter_entered == "q":
                        print("Quitting time!" + "\n")
                        return global_list

                    if letter_entered != "p" or letter_entered != "n" or letter_entered != "q":
                        print("Skipping!" + "\n")
                        break
            except UnicodeDecodeError:
                print("Can't read this chat")
                continue

def control_panel():
    """
    User Interface for the application
    """
    while True:
        print("\n" + "***** Welcome to Jack Twitch Chat Text Classifier! *****" + "\n")
        print("What is your command?")
        print("Press c to clean and grade Twitch Chat comments (This will automatically upate the model as well)")
        print("Press u to update the model with a cleaned and graded .csv file")
        print("Press t to use the text classification system")
        print("Press s to see a summary of the data")
        print("Press q to quit the program")

        keyboard_input = input()

        if keyboard_input == "c":
            new_file_name = get_output_file_name() + ".csv"
            temp_list = clean_and_train()
            # Note that clean_and_train() returns a graded .csv
            # or in other words this .csv file has two columns
            write_new_file(temp_list, new_file_name)
            add_to_master(temp_list)
            # update_model(new_file_name)
            continue

        if keyboard_input == "u":
            print("Please select your cleaned and graded .csv file" + "\n")
            temp_file = os.path.basename(filedialog.askopenfilename())
            update_model(temp_file)
            continue

        if keyboard_input == "t":
            text_classifier()
            continue

        if keyboard_input == "s":
            present_summary()
            continue

        if keyboard_input == "q":
            print("Thanks for using my program!" + "\n")
            break

        if keyboard_input != "c" or keyboard_input != "u" or keyboard_input != "t" or keyboard_input != "s" or keyboard_input != "q":
            print("hmm couldn't make sense of that command. Try again" +"\n")
            continue


def text_classifier():
    """
    Text classification System.

    Think about this as the result of training the model
    """
    # Prompt user for input that will be classified
    while True:
        text_to_classify = input("What is the text that you'd like to classify?" + "\n")
        prob_dist = classifier.prob_classify(text_to_classify)
        if prob_dist.max() == 'pos':
            print("The classifier thinks this statement is positive.")

        if prob_dist.max() == 'neg':
            print("The classifier thinks this statement is negative")
        
        
        print("The classifier is " + str(round(prob_dist.prob("pos"), 2)) + " sure that this statement is positive.")
        print("The classifier is " + str(round(prob_dist.prob("neg"), 2)) + " sure that this statement is negative.")
        if input("Continue? (y/n)" +"\n") == "y":
            continue
        else:
            return
    

def update_model(file_name):
    """
    Update the model with a cleaned and graded .csv file
    """
    # Prompt user for name of input .csv file
    # Note: Not needed with current implementation
    # file_name = filedialog.askopenfilename()

    # add file to master
    if file_name != "master.csv":
        merge_csv("master.csv", file_name)
    
    # Open file and update the text classifier
    with open(file_name, 'r', encoding='latin-1') as file:
        # We need to turn the .csv file into another format
        # it needs to be a list of tuples, where each tuple takes the form of
        # ("twitch comment", "pos/neg")
        reader = csv.reader(file)
        update_data = list(tuple(line) for line in reader)
        classifier.update(update_data)
        print("The model has been updated!" + "\n")
        return file_name
        


def present_summary():
    """
    Present a summary of the model based on the data that the model has
    """
    classifier.show_informative_features(5)


def add_to_master(input_list):
    """
    This function adds a list of graded Twitch comments to a master.csv file
    """
    with open("master.csv", mode = "w", errors = "ignore", newline = "") as csvfile:
        csvwriter = csv.writer(csvfile)      
        try:
            csvwriter.writerows(input_list)
        except UnicodeDecodeError:
            print("AHHHHH there's an error!!")

    update_model("master.csv")
    
def merge_csv(file_name_1, file_name_2):
    """
    Given two csvs, merge the second to the end of the first
    """
    with open(file_name_1, newline="") as f1:
        reader1 = csv.reader(f1)
        first_data = list(reader1)

    with open(file_name_2, newline="")as f2:
        reader2 = csv.reader(f2)
        second_data = list(reader2)
    
    for ele in second_data:
        first_data.append(ele)
    write_new_file(first_data, "master.csv")


def main():
    """
    Drives execution.
    """

    # Get current working directory
    current_dir = os.getcwd()
    # Look for the previous training data
    master_check = current_dir + "\master.csv"
    # If the previous data is not there then create one
    if not os.path.exists(master_check):
        print("hmm.. can't seem to locate the previous data.")
        open("master.csv", "w")
    
    # Update model based on previous data
    update_model("master.csv")

    # This method allows the user to interact with different parts of the
    # Twitch Chat text classification model
    control_panel()

# Create classifier with dummy training data
train = [("W", "pos"), ("L", "neg")]
# Required to be at this indentation for classifier to called in functions
classifier = NaiveBayesClassifier(train)

main()

# Is there a way to add an updatrred cleaned and graded .csv file to a master.csv file?


# Add a gui