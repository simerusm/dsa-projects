from trie import Trie

def main():
    word_list = [
        "apple", "app", "application", "apt", "banana", "band", "bandana",
        "can", "candy", "cape", "capital", "dog", "dove", "door"
    ]
    
    trie = Trie()
    for word in word_list:
        trie.insert(word)
    
    print("Autocomplete Program. Type 'exit' to quit.")
    while True:
        prefix = input("\nEnter prefix: ").strip()
        if prefix.lower() == 'exit':
            break
        
        suggestions = trie.get_words_with_prefix(prefix)
        if suggestions:
            print("Suggestions:", suggestions)
        else:
            print("No suggestions found for that prefix.")

if __name__ == "__main__":
    main()