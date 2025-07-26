import argparse
from DBOperations import init_db, feed_corpus, view,clear_db, delete_db, query_store

def welcomeMessage():
    print("Welcome to Vectorly!")
    print("Available commands:")
    print("\tinit: Initialize a new vector database")
    print("\tfeed: Feed new phrases existing corpus")
    print("\tquery: Query new phrases to find the most similar ones from the corpus")
    print("\tview: New phrases, vocabulary and similarity matrix of corpus")
    print("\tclear: Clear all phrases from existing corpus")
    print("\tdelete: Delete existing corpus")
    print("\t--help: Display help message")

def main():
    parser = argparse.ArgumentParser(description = "Vector Database for text embedding.")
    subparser = parser.add_subparsers(dest="command", help="Subcommand help")

    init_parser = subparser.add_parser("init", help="Initialize a new vector database")
    
    feed_parser = subparser.add_parser("feed", help="Feed phrases into existing corpus")

    query_parser = subparser.add_parser("query", help="Query new phrase to find the most similar ones from the corpus")
    query_parser.add_argument("-q", nargs=1, help="Enter phrase to query corpus")

    view_parser = subparser.add_parser("view", help="View all phrases in corpus")
    view_parser.add_argument("-c", nargs="?", help="View copus", default="none")
    view_parser.add_argument("-v", nargs="?", help="View vocabulary", default="none")
    view_parser.add_argument("-m", nargs="?", help="View vocabulary", default="none")

    clear_parser = subparser.add_parser("clear", help="Clear existing vector database")

    delete_parser = subparser.add_parser("delete", help="Delete existing corpus")

    args = parser.parse_args()
    args_dict = args.__dict__

    cmd = args_dict["command"]

    match cmd:
        case "init":
            init_db()
        
        case "feed":
            return feed_corpus()
        
        case "query":
            return query_store()
        
        case "view":
            return view(args_dict["c"], args_dict["v"], args_dict["m"])
        
        case "delete":
            return delete_db()

        case "clear":
            return clear_db()
        
        case default:
            welcomeMessage()

if __name__ == "__main__":
    main()