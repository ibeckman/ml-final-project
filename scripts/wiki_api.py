import wikipedia
import string

if __name__ == "__main__":
    current_year = 1996
    END_DATE = 2006
    while True:
        if current_year > END_DATE:
            break
        else:
            with open("./wiki_data/"+str(current_year)+"_wikipedia.csv", "a") as analysisfile:
                analysisfile.write("ID,Name,SecCode,Sentence\n")
                with open("./wiki_data/" + str(current_year) + ".meta.txt") as f:
                    for line in f:
                        array = line.split()
                        sec_code = array[len(array)-1]
                        company_name = ' '.join(array[3: len(array)-1])
                        id = array[0]
                        s = " "
                        try:
                            ch = wikipedia.summary(company_name, sentences=1).strip()
                            exclude = set(string.punctuation)
                            s =''.join(word.strip(string.punctuation) for word in ch)
                        except wikipedia.exceptions.DisambiguationError as e:
                            print "DisambiguationError"
                        except wikipedia.exceptions.PageError as e:
                            print "Page Error"
                        analysisfile.write(str(id)+"," + str(company_name) + "," + str(sec_code) + "," + s.encode('utf-8') +"\n")
            current_year = current_year +1
