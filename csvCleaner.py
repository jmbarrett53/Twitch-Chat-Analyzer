import pandas as pd
# This code reads in an input .txt file and shaves off the time that the comment was made
# and the name of the commenter
# Lines are still displayed in the order that they were sent
#This code also skips any lines where character encoding gets weird

# IMPORTANT: The twitch chat downloader gives us a .txt file, and the textblob library
# uses .csv ones

def get_input_file_name():
    file_name = input("What is the name of the input file?")
    return file_name

def get_output_file_name():
    file_name = input("What would you like to call the output file?")
    return file_name

input_file = get_input_file_name()
output_file = get_output_file_name()

extracted_lines = []
with open(input_file, "r", encoding = "utf-8", errors = "ignore") as file:
    for line in file:
        try:
            parts = line.split(": ", 1)
            if len(parts) > 1:
                extracted_lines.append(parts[1].strip())
        except UnicodeDecodeError:
            #skip lines that can't be decoded
            continue

with open(input_file, "w", encoding = "utf-8") as file:
    for line in extracted_lines:
        file.write(line + "\n")


# This is a way to turn a .txt into a .csv very easily
# However we must preprocess the data before we can do anything
text_file = pd.read_table(input_file)
print("Check " + output_file)
text_file.to_csv(output_file, index=False)

# This code drops the first column of the .csv where its filled with numbers that don't help
# df = read_csv(output_file)
# df = df.drop(df.columns[0], axis = 1)
# df.to_csv(output_file, index=False)
