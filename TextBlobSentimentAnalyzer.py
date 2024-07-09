from textblob.classifiers import NaiveBayesClassifier
import keyboard


def file_to_open():
    file_name = input("What's the cleaned chat file name?")
    return file_name
    



# with open('TBReadySportsTwitchChatData.csv', 'r', encoding='latin-1') as f:
#     cl = NaiveBayesClassifier(f, format='csv')

    

# Make a function that prompts the user for input, and have the text classifier classify it
def classify_this():
    with open(file_to_open(), 'r', encoding='latin-1') as f:
        cl = NaiveBayesClassifier(f, format='csv')
    text_to_classify = input("What message would you like to classify?" + "\n")
    print('you said: ' + text_to_classify)

    # print("cl.classify() says: ")
    # print(cl.classify(text_to_classify))

    prob_dist = cl.prob_classify(text_to_classify)
    print("prob_dist,max()")
    print(prob_dist.max())
    print("positive confidence:")
    print(round(prob_dist.prob("pos"), 2))
    print("negative confidence:")
    print(round(prob_dist.prob("neg"), 2))




classify_this()