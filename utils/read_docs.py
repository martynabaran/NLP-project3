""" Read documents module """
import os
from timeit import default_timer as timer
from typing import Tuple

import fitz  # type: ignore
from langchain.docstore.document import Document
from langchain_community.document_loaders import (CSVLoader, TextLoader, PyPDFLoader, PyMuPDFLoader, PDFMinerLoader,
                                                  PDFPlumberLoader, UnstructuredWordDocumentLoader)
from langchain_community.document_loaders.pdf import BasePDFLoader

from globals import (get_length_of_text, global_debug, flag_text_file_save, supported_file_types, contains_non_special_characters)
from ocr import ocr2text


class PyMuPDFXHTMLLoader(BasePDFLoader):
    """Custom PDF Loader that extracts XHTML content from a PDF."""

    def __init__(self, file_path: str):  # pylint: disable=super-init-not-called
        """Initialize with path to the PDF file."""
        self.file_path = file_path

    def load(self) -> list[Document]:
        """Load and extract the XHTML content from the PDF."""
        # Open the PDF file with PyMuPDF
        doc = fitz.open(self.file_path)
        documents = []

        # Loop through each page and extract XML content
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            xhtml_content = page.get_text("xhtml", flags=fitz.TEXT_MEDIABOX_CLIP)

            # Create a Document object from Langchain for each page's XML content
            documents.append(Document(page_content=xhtml_content, metadata={"page": page_num + 1}))

        return documents


# read_docs.py: select PDF parser
pdf_parsers_list = {
    "PyPDFLoader": (PyPDFLoader, {}),
    "PyPDFLoaderOCR": (PyPDFLoader, {"extract_images": True}),
    "PyMuPDFLoader": (PyMuPDFLoader, {}),
    "PyMuPDFXHTMLLoader": (PyMuPDFXHTMLLoader, {}),
    "PDFMinerLoader": (PDFMinerLoader, {}),
    "PDFPlumberLoader": (PDFPlumberLoader, {}),
}

pdf_parser = pdf_parsers_list["PDFPlumberLoader"]
# print(pdf_parser)

FILE_LOADER_MAPPING = {
    "csv": (CSVLoader, {"encoding": "utf-8"}),
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "pdf": (PDFPlumberLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
    "rtf": (TextLoader, {"encoding": "utf8"}),
}


def file2text(filepath: str, ext: str) -> Tuple[str, bool, int]:
    """
    Extracts text from a file and handles potential OCR-based processing.

    Parameters:
    filepath (str): The path to the input file.
    ext (str): The file extension (used to verify support).

    Returns:
    Tuple[str, bool, int]: A tuple containing:
        - content (str): The extracted text content.
        - ok_status (bool): Whether the extraction was successful.
        - no_pages (int): The number of pages in the document.
    """

    content = ""  # The extracted content of the PDF
    ok_status = False  # Status indicating if the extraction was successful
    no_pages = 0  # Number of pages in the document

    # Check if the file extension is supported by FILE_LOADER_MAPPING
    if ext in FILE_LOADER_MAPPING:
        loader_class, loader_args = FILE_LOADER_MAPPING[ext]  # Get loader class and arguments
        loader = loader_class(filepath, **loader_args)  # Instantiate the loader
        pages = loader.load()  # Load the pages

        no_pages = len(pages)  # Count the number of pages
        blank_pages = 0  # Counter for blank pages

        # If the document has at least one page, iterate through the pages and extract content
        if len(pages) >= 1:
            for page in pages:
                current_page_content = page.page_content
                if contains_non_special_characters(current_page_content):
                    content += current_page_content + "\n"  # Append the content of the current page
                else:
                    blank_pages += 1  # Count blank pages
        print("Number of pages ", no_pages, blank_pages)
        # If some of pages are blank and document is PDF, attempt OCR processing
        if blank_pages > 0 and ext == "pdf":
            try:
                if global_debug >= 1:
                    print(f"-- pdf2text() -- processing PDF file {filepath} as OCR")
                content, ok_status = ocr2text(filepath)  # Attempt OCR to extract content
            except Exception as exp:  # pylint: disable=broad-exception-caught
                print(f"-- pdf2text() -- failed processing OCR {filepath} with exception {str(exp)}.")
                ok_status = False
        else:
            ok_status = True  # Set status to True if all pages were processed successfully

    return content, ok_status, no_pages


def process_document(dirpath: str, filename: str) -> Tuple[str, int, bool, int]:
    """
    Main function to process the given file. Saves content as a text file if successful.
    So far works only on PDF files.

    Steps:
    - Skips the file if already processed.
    - Checks the file type and sends it to the appropriate function.
    - Reports if the file type is not supported.
    - Saves file content to a _text.txt file.
    - Always returns file content as a string, or an empty string if the file can't be read.

    Parameters:
    dirpath (str): Path to the directory containing the file.
    filename (str): Name of the file to process.

    Returns:
    Tuple[str, int, bool, int]: A tuple containing:
        - text (str): The processed content of the file.
        - file_length (int): The length of the processed text.
        - ok_status (bool): Whether the file was processed successfully.
        - no_pages (int): The number of pages in the document.
    """

    # Validate input types
    if type(dirpath) not in [str]:
        raise TypeError("-- process_document() -- dirpath = %s should be a string type" % dirpath)

    if type(filename) not in [str]:
        raise TypeError("-- process_document() -- filename = %s should be a string type" % filename)

    # Create the full file path and extract the file extension
    filepath = os.path.join(dirpath, filename)
    ext = os.path.splitext(filepath)[-1][1:].lower()

    # Initialize variables
    ok_status = False  # Whether the file was successfully processed
    text = ""  # Text content of the document
    no_pages = 0  # Number of pages

    # Process supported file types
    if ext in supported_file_types:
        try:
            # Do not process the files that might be the output of previous processing
            # So they have a name "*_text.txt"
            if os.path.exists(filepath[:-len("_text.txt")] + "_text.txt"):
                print('-- process_document() -- file %s has been skipped.' % filepath)
                ok_status = False
                return text, 0, ok_status, no_pages

            text, ok_status, no_pages = file2text(filepath, ext)

        except Exception as exp:  # pylint: disable=broad-exception-caught
            print("-- process_document() -- failed processing PDF %s with exception %s." % (filepath, str(exp)))
    else:
        print("-- process_document() -- %s is not supported type" % filepath)

    # If flag_text_file_save is set (in globals.py), then save the text content to a separate file
    # but only if text was extracted and status is OK.
    if text != "" and ok_status and flag_text_file_save:
        fileout = filepath + "_text.txt"

        with open(fileout, 'w', encoding="utf-8") as file_object:
            file_object.write(text)
            file_object.close()

    # Calculate the length of the processed text
    file_length = get_length_of_text(text)

    # Return the processed text, its length, the status, and the number of pages
    return text, file_length, ok_status, no_pages


def read_files_in_folder():  # pylint: disable=too-many-locals
    """
    Reads and processes files in a selected folder.
    Tracks the number of files, pages processed, and processing time.
    :return: output_file_content_list

        List with text content of the files in the following format:
        [
        {"filename": "document_01.docx", "content":"Lorem ipusum dolorem..."},
        {"filename": "document_02.pdf", "content":"dolorem est..."},
        {"filename": "document_03.rtf", "content":"Lorem Lorem Lorem..."},
        ]
    """

    output_file_content_list = []

    start_global = timer()  # Start the global timer to measure total processing time
    no_processed = 0  # Counter for successfully processed files
    no_files = 0  # Counter for total number of files processed
    no_pages = 0  # Counter for total number of pages processed

    # Traverse directory tree starting from the folder selected by the user
    for (dir_path, dir_names, file_names) in (  # pylint: disable=unused-variable
            os.walk(input('Select folder with documents: '))):
        for file in file_names:
            start = timer()  # Start the timer for processing a single file
            if global_debug >= 0:
                print("//----------------------------------//\n")
                print("Processing file %s ... " % file)

            # Process the current file
            output, length, ok, pages = process_document(dir_path, file)
            no_files += 1  # Increment the file counter
            no_pages += pages  # Add the number of pages in the current file
            if ok:
                no_processed += 1  # Increment processed files counter if processing was successful
                output_file_content_list.append({"filename": file, "content": output})
            end = timer()  # Stop the timer for the current file

            # Display processing time and file details if debugging is enabled
            if global_debug >= 0:
                print("\nLength of document %s is %d characters, processing time %.4f seconds" % (
                    file, length, end - start))
                if global_debug > 1:
                    print("\n//----------------------------------//\n")
                    print("File content: \n")
                    print(output)
                    print("\n//----------------------------------//\n")

    end_global = timer()  # Stop the global timer after processing all files

    # If debugging is enabled, display the overall processing statistics
    if global_debug >= 0:
        proc_time = end_global - start_global
        avg_proc_time = proc_time / no_files if no_files > 0 else 0  # Avoid division by zero
        avg_proc_time_page = proc_time / no_pages if no_pages > 0 else 0  # Avoid division by zero

        print("\n//----------------------------------//\n")
        print("Properly processed %d files out of %d (%.1f%%), %d pages in total" % (
            no_processed, no_files, float(no_processed / no_files * 100.), no_pages))
        print("Total processing time %.4f seconds, on average %.4f seconds per file, %.4f seconds per page" % (
            proc_time, avg_proc_time, avg_proc_time_page))
        print("\n//----------------------------------//\n")
    return output_file_content_list


if __name__ == "__main__":
    file_contents = read_files_in_folder()
    print(file_contents)
