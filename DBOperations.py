import sys
import pickle
import os
from VectorStore import VectorStore

def init_db():
    filename = '.vectorstore'
    try:
        with open(filename, "w") as f:
            pass
    except Exception as e:
        print("Error initializing Vector Store")
        sys.exit(1)

def read_vectorstore():
    try:
        with open(".vectorstore", "rb") as f:
            if len(f.peek()) > 0:
                corpus: VectorStore = pickle.load(f)
            else:
                corpus = VectorStore()
            return corpus
    except:
        return "Vector Store not initalized!! Use `python main.py init` to intialize a new database."

def write_to_vectorstore(vector_store: VectorStore):
    try:
        with open(".vectorstore", "wb") as f:
            pickle.dump(vector_store, f)
            print("Updated Corpus!")
    except:
        return "Vector Store not initalized!! Use `python main.py init` to intialize a new database."

def feed_corpus(implicit:bool = False, new_phrase: str = None):
    existing_corpus = read_vectorstore()
    if not implicit:
        if type(existing_corpus) != str:
            existing_phrases = list(existing_corpus.vector_data.keys())
            num_phrases = int(input("How many phrases do you want to feed?(Enter 0 to exit): "))
            if num_phrases:
                phrases = []
                print("Enter the phrases(Enter `q!` to exit): ")
                while(num_phrases):
                    phrase = input("")
                    if phrase == "q!":
                        break
                    elif phrase in existing_phrases:
                        print("Phrase already in corpus! Enter a different phrase")
                    else:
                        phrases.append(phrase.strip())
                        num_phrases -= 1
                
                phrases = phrases + existing_phrases
                vocab = existing_corpus.get_vocab(phrases)
                
                phrase_vector = existing_corpus.get_phrase_vector(vocab, phrases)
                
                # add to vector store
                for phrase, vector in phrase_vector.items():
                    existing_corpus.add_vector(phrase, vector)
                
                # update similarity matrix
                for phrase, vector in phrase_vector.items():
                    existing_corpus._update_index(phrase, vector)
                
                write_to_vectorstore(existing_corpus)
            return None
        else:
            print(existing_corpus)
            sys.exit(1)
    else:
        if type(existing_corpus) != str:
            existing_phrases = list(existing_corpus.vector_data.keys())
            if new_phrase not in existing_phrases:
                existing_phrases.append(new_phrase)
                phrases = existing_phrases
                vocab = existing_corpus.get_vocab(phrases)
                phrase_vector = existing_corpus.get_phrase_vector(vocab, phrases)
                
                # add to vector store
                for phrase, vector in phrase_vector.items():
                    existing_corpus.add_vector(phrase, vector)
                
                # update similarity matrix
                for phrase, vector in phrase_vector.items():
                    existing_corpus._update_index(phrase, vector)
                
                write_to_vectorstore(existing_corpus)
        else:
            print(existing_corpus)
            sys.exit(1)

def view(c: bool, v:bool, m:bool):
    existing_corpus = read_vectorstore()
    if type(existing_corpus) != str:
        phrases = list(existing_corpus.vector_data.keys())
        if not c:
            if len(phrases) > 0:
                print("Corpus:")
                for phrase in phrases:
                    print(f"\t{phrase}")
            else:
                print("Corpus empty!")
        if not v:
            vocabs = VectorStore.get_vocab(None, phrases)
            if len(vocabs) > 0:
                print("Vocabulary:")
                for vocab in vocabs:
                    print(f"\t{vocab}")
            else:
                print("Vocabulary empty!")
        if not m:
            existing_corpus.view_similarity_matrix()
        return None
    else:
        print(existing_corpus)
        sys.exit(1)

def clear_db():
    existing_corpus = read_vectorstore()
    if type(existing_corpus) != str:
        confirmation = input("Are you sure? (Enter 'Y' to clear, 'n' to cancel): ")
        if confirmation == 'Y':
            init_db()
            print("Vector store cleared!")
            return None
        elif confirmation == 'n':
            print("Clear aborted!")
            sys.exit(1)
        else:
            print("Invalid input.")
            sys.exit(1)
    else:
        print(existing_corpus)
        sys.exit(1)
    
def delete_db():
    if os.path.exists('.vectorstore'):
        confirmation = input("Are you sure? (Enter 'Y' to delete, 'n' to cancel): ")
        if confirmation == 'Y':
            os.remove('.vectorstore')
            print("Vector store deleted!")
            return None
        elif confirmation == 'n':
            print("Delete aborted!")
            sys.exit(1)
        else:
            print("Invalid input.")
            sys.exit(1)
    else:
        print("Vector Store not initalized!! Use `python main.py init` to intialize a new database.")
        sys.exit(1)

def isValidQuery(query):
    if len(query) == 0:
        return False
    return True

def query_store():
    existing_corpus = read_vectorstore()
    if type(existing_corpus) != str:
        query = input("Enter the sentence/phrase you'd like to check the similarity: (`q!` to exit): ").strip()
        while not isValidQuery(query):
            query = input("Please enter a valid sentence to query! (`q!` to exit) ").strip()

        if query == "q!":
            sys.exit(1)
        else: 
            num_results = int(input("How many results would you like? (Enter 0 to skip question): "))    

            phrases = list(existing_corpus.vector_data.keys())
            query_vector = existing_corpus.get_vector(phrases, query)

            if num_results == 0:
                similar_phrases = existing_corpus.find_similar_vectors(query_vector)
            else:
                similar_phrases = existing_corpus.find_similar_vectors(query_vector, num_results)
            
            feed_corpus(implicit=True, new_phrase=query)
            for phrase, similarity in similar_phrases:
                print(f"{phrase} :: {similarity}")

    else:
        print(existing_corpus)
        sys.exit(1)