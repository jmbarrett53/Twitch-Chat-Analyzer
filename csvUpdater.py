import keyboard
import csv
import time
import pandas as pd

#create a way to remember updated .csv lines
global_list = []




def update_csv(input_string):
    """
    Given a file name, return an updated list containing all of the updated strings that are formatted to the TextBlob standard for sentiment analysis
    """
    with open(input_string, mode = "r", errors = "ignore") as csv_file:
        reader = csv.reader(csv_file)

        while True:
            try:
                for lines in reader:
                    lines = "".join(lines)
                    if lines.endswith(",pos") or lines.endswith(",neg"):
                        continue
                    time.sleep(0.12)
                    #print(type(lines))
                    #lines = "".join(lines)
                    #print(type(lines))
                    print(lines)
                
                    letter_entered = keyboard.read_key()

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

                    if letter_entered == "s":
                        print("Skipping!" + "\n")
                        break

                    if letter_entered == "q":
                        print("quitting time!" + "\n")
                        #print(global_list)
                        return global_list


        
            except UnicodeDecodeError:
                print("Can't read this chat")
                continue

        




# If you are given a list of strings can you write those to a .csv file?
def write_new_file(input_list, file_name):
    with open(file_name, mode = "w", errors = "ignore", newline = "") as csvfile:
        csvwriter = csv.writer(csvfile)


        
        try:
            csvwriter.writerows(input_list)

        except UnicodeDecodeError:
            print("AHHHHH there's an error!!")
        
    print("Check " + file_name + " for your output")


# A way to tell the program which file to use
# Currently its hard coded just to make testing faster but in the end I would like the
# user to be able to specify which file to use and what they want to call the output file
def get_input_file_name():
    file_name = input("What is the name of the input file?")
    return file_name

def get_output_file_name():
    file_name = input("What would you like to call the output file?")
    return file_name
    


#update_csv("SportsTwitchChatData.csv")
input_file_name = get_input_file_name()
output_file_name = get_output_file_name()

write_new_file(update_csv(input_file_name), output_file_name)

#text_file = pd.read_table(output_file_name, encoding = "latin-1")
#text_file.to_csv("TBReadySportsTwitchChatData.csv", index = False, header = False, encoding = "latin-1")
