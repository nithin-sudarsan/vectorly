# Vectorly

A terminal-based interactive app to generate vector text-embeddings, that gets smarter as you use!

Train on example sentences, then query to find the most similar ones with similarity percentages.

---

## Features

- **Initialize a vector database** for storing phrase embeddings.
- **Feed new phrases** to the corpus and update the vector store.
- **Query phrases** to find the most similar ones in the corpus using cosine similarity.
- **View corpus, vocabulary, and similarity matrix**.
- **Clear or delete** the vector database.

---

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nithin-sudarsan/vectorly.git
    cd vectorly
    ```
2. Install dependencies:
    ```sh
    pip install numpy pandas
    ```

---

## Usage

Run the app from the terminal:
```sh
python main.py <command>
```

### Commands

- `init`  
  Initialize a new vector database.

- `feed`  
  Feed new phrases into the existing corpus interactively.

- `query`  
  Query a phrase to find the most similar ones from the corpus.

- `view [-c] [-v] [-m]`  
  View corpus (`-c`), vocabulary (`-v`), and similarity matrix (`-m`).

- `clear`  
  Clear all phrases from the existing corpus.

- `delete`  
  Delete the existing corpus.

- `--help`  
  Display help message.

---

## How It Works

- **Vector Representation:**  
  Each phrase is tokenized and represented as a vector based on word counts (bag-of-words model).

- **Cosine Similarity:**  
  Similarity between phrases is computed using cosine similarity.

- **Persistence:**  
  The corpus and vectors are stored in a binary file `.vectorstore` using Python's `pickle` module.

---

## File Structure

- `main.py`: CLI entry point and command parser.
- `DBOperations.py`: Handles database operations (init, feed, query, view, clear, delete).
- `VectorStore.py`: Implements the vector store, vectorization, similarity computation, and matrix viewing.
- `utils.py`: Utility functions (cosine similarity).
- `.vectorstore`: Binary file storing the vector database.
- `.gitignore`: Ignores virtual environment and cache files.

---

## Example Workflow

1. **Initialize the database:**
    ```sh
    python main.py init
    ```

2. **Feed phrases:**
    ```sh
    python main.py feed
    ```
    Enter phrases interactively.

3. **Query for similar phrases:**
    ```sh
    python main.py query
    ```
    Enter a phrase to find similar ones.

4. **View corpus, vocabulary, and similarity matrix:**
    ```sh
    python main.py view -c none -v none -m none
    ```

5. **Clear or delete the database:**
    ```sh
    python main.py clear
    python main.py delete
    ```

---

## Implementation Details

- **VectorStore Class:**  
  - Stores phrase vectors and similarity indices.
  - Methods for adding vectors, updating similarity matrix, finding similar vectors, and viewing the similarity matrix.

- **DBOperations:**  
  - Handles reading/writing the vector store, feeding new phrases, querying, viewing, clearing, and deleting the database.

- **CLI:**  
  - Uses `argparse` for command parsing and interactive input for feeding/querying phrases.
