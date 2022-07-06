import getopt
import PyPDF2
import sys
from os import listdir, rename, path
from os.path import isfile, join, abspath, dirname
import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL, Label, Button, Entry, filedialog, StringVar, N, E, W, S
from tkinter.messagebox import showinfo, showerror

block_name = '# Adresat'
key_name_1 = 'Nazwa'
key_name_2 = 'Nazwa cd'
wild_card = 'Ulica Numer domu / numer lokalu'


def get_files_from_folder(folder_path):
    pdfs = []
    files_list = []
    for file in listdir(folder_path):
        if file.endswith('.pdf'):
            pdfs.append(join(folder_path, file))
    files_list = [abspath(join(folder_path, p)) for p in pdfs if isfile(join(folder_path, p))]
    return files_list


def read_name_from_pdf(file_path):
    # Get text
    pdf_file_object = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)
    page_object = pdf_reader.getPage(0)
    text = page_object.extractText()

    # Process text
    collection = text.split('\n')
    collection = list(filter(None, collection))
    file_name = collection[collection.index(key_name_1) + 1]
    if collection[collection.index(key_name_2) + 1] != wild_card:
        file_name += ' ' + collection[collection.index(key_name_2) + 1]

    pdf_file_object.close()

    return file_name


def rename_file(file_path, new_name):
    rename(file_path, dirname(file_path) + '/' + new_name + '.pdf')

def execute_all(folder_path):
    for file_path in get_files_from_folder(folder_path):
        new_name = read_name_from_pdf(file_path)
        rename_file(file_path, new_name)


class CMD:
    def __init__(self, argv):
        self.folder_path = ''
        self.argv = argv

        try:
            opts, args = getopt.getopt(self.argv, 'hp:', ['path='])
        except getopt.GetoptError:
            print('-p <path>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('-p <path>')
                sys.exit(0)
            elif opt in ('-p', '--path'):
                if not path.exists(self.folder_path.get()):
                    print('Ścieżka nie istnieje.')
                    sys.exit(1)
                elif not path.isdir(self.folder_path.get()):
                    print('Ścieżka nie jest folderem.')
                    sys.exit(1)
                else:
                    self.folder_path = arg

        execute_all(self.folder_path)


class App:
    def __init__(self, root):
        self.root = root
        self.folder_path = tk.StringVar()
        self.root.title('PDFRenamer')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.grid(row=1, column=0, sticky="nsew")
        horizontal_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane.add(Label(horizontal_pane, text="Ścieżka:"))
        horizontal_pane.add(Entry(horizontal_pane, textvariable=self.folder_path, width=60))
        horizontal_pane.add(Button(horizontal_pane, text='...', command=self.open_folder))
        vertical_pane.add(horizontal_pane)
        vertical_pane.add(Button(vertical_pane, text="Zmień nazwy", command=self.execute))
        vertical_pane.add(Label(vertical_pane, text="Autor: k4zz", anchor="e"))

    def open_folder(self):
        self.folder_path.set(filedialog.askdirectory(title="Wybierz folder", initialdir='~'))

    def execute(self):
        if not path.exists(self.folder_path.get()):
            showerror("ERROR", "Ścieżka nie istnieje.")
        elif not path.isdir(self.folder_path.get()):
            showerror("ERROR", "Ścieżka nie jest folderem.")
        else:
            execute_all(self.folder_path.get())
            showinfo("INFO", "Done!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        CMD(sys.argv[1:])
    else:
        root = tk.Tk()
        app = App(root)
        app.root.mainloop()

