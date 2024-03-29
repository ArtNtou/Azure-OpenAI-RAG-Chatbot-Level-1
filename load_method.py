from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import SKLearnVectorStore
from PyPDF2 import PdfReader


# load files from the app
def load_files(embed_model, pdfs, index_name):
    """
        Loads text from PDF files, splits them into chunks, creates embeddings, and stores them in a vector store.

        :param embed_model: Embedding model used for creating embeddings.
        :type embed_model: langchain.vectorstores.SKLearnVectorStore
        :param pdfs: List of PDF files to load text from.
        :type pdfs: list of str
        :param index_name: Name of the index to store the vector store.
        :type index_name: str

        :return: Text chunks and the vector store containing embeddings of the text chunks.
        :rtype: (list of str, langchain.vectorstores.SKLearnVectorStore)
    """

    # save all documents
    all_texts = []

    # Loop through each uploaded PDF
    for pdf_file in pdfs:
        pdf_reader = PdfReader(pdf_file)

        # Loop through each page in the PDF
        for page_number in range(len(pdf_reader.pages)):
            # Extract text from the current page
            text = pdf_reader.pages[page_number].extract_text()

            # Append the text to the list
            all_texts.append(text)

    # Combine all extracted text into a single string
    combined_text = " ".join(all_texts)

    # split the documents into chunks that chatgpt can handle
    # split the document every 2000 characters with 100 characters overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len
    )

    # create those chunks
    data = text_splitter.split_text(text=combined_text)

    # create the vectorstore that contain basically the embeddings
    vectorstore = SKLearnVectorStore.from_texts(data,
                                                embed_model,
                                                persist_path=f"{index_name}vctrstr.json",
                                                serializer="json")

    # save vectorstore in order to reuse it and create again embeddings for the same documentst
    vectorstore.persist()

    return data, vectorstore
