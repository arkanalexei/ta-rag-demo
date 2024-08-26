from langchain_text_splitters import RecursiveCharacterTextSplitter


def document_splitter(docs, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    all_splits = text_splitter.split_documents(docs)

    # add source to each split
    for doc in all_splits:
        if doc.metadata['page_number'] != None:
            doc.page_content = doc.page_content + \
                f"\n\nSource: [{doc.metadata['title']}]({doc.metadata['dokumen_peraturan']}#page={doc.metadata['page_number']})"
        else:
            doc.page_content = doc.page_content + \
                f"\n\nSource: [{doc.metadata['title']}]({doc.metadata['dokumen_peraturan']})"

    print(f"Split {len(docs)} documents into {len(all_splits)} chunks")

    return all_splits
