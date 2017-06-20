from flask import Flask, render_template, jsonify, request
import random
import os
import subprocess
import sys
import PyPDF2

app = Flask(__name__)

process = []
glob_file_loc = ''
adobe_loc = ''
pdf_files = []
current_notes = []
not_valid = []
current_file = []
current_page = []


def get_random_list():
    r = random.randint(0, len(current_notes) - 1)
    r = current_notes[r]
    return r


@app.route('/')
def hello_world():
    not_valid.clear()
    for file_x in pdf_files:
        not_valid.append(file_x.replace(".pdf", ""))
    return render_template('app.html', names_pdf=not_valid)


@app.route('/next/')
def next_pdf():
    global rand_page
    if not (len(process) == 0):
        process[0].kill()
        process.clear()

    if len(current_notes) == 0:
        return "Nothing in the selection, please add some modules."

    req = get_random_list()
    file_to_use = req + ".pdf"
    path_string = glob_file_loc + '\\\\' + file_to_use
    path_to_pdf = os.path.abspath(path_string)
    path_to_acrobat = os.path.abspath(adobe_loc)
    not_found = True
    file = open(glob_file_loc + '/meta/' + req + '.txt', 'r')
    reader = PyPDF2.PdfFileReader(open(path_string, 'rb'))
    max_pages = reader.getNumPages()

    while not_found:
        not_found = False
        rand_page = random.randint(1, max_pages)
        for line in file:
            if int(line) == rand_page:
                not_found = True
                break

    file.close()
    page_string = 'page=' + str(rand_page)
    current_file.append(req)
    current_page.append(rand_page)

    process.append(
        subprocess.Popen([path_to_acrobat, '/A', page_string, path_to_pdf], shell=False, stdout=subprocess.PIPE))
    return current_file[0] + ' - Page: ' + str(current_page[0])


@app.route('/know/')
def move_on():
    if not (len(process) == 0):
        process[0].kill()
        process.clear()
        meta_file = glob_file_loc + '/meta/' + current_file[0] + '.txt'
        with open(meta_file, "a") as f:
            f.write(str(current_page[0]) + '\n')
        current_page.clear()
        current_file.clear()
        return 'Page added to stop list.'
    return 'No process currently open!'


@app.route('/exit/')
def exit_process():
    if not (len(process) == 0):
        process[0].kill()
        process.clear()
        current_page.clear()
        current_file.clear()
        return 'Process exited.'
    return 'No process to terminate!'


@app.route('/update/', methods=["POST"])
def change_list():
    req = request.json
    if req['class'] == 'border-items-off':
        current_notes.append(req['id'])
        not_valid.remove(req['id'])
    else:
        not_valid.append(req['id'])
        current_notes.remove(req['id'])
    return "success"


@app.route('/colourGrid/')
def update_notes_selection():
    return jsonify(on=current_notes, off=not_valid)


def set_notes():
    for poss_file in os.listdir(glob_file_loc):
        if poss_file.endswith(".pdf"):
            pdf_files.append(poss_file)
    if 'meta' not in os.listdir(glob_file_loc):
        new_folder = glob_file_loc + '\meta'
        os.makedirs(new_folder)
        for f_meta in pdf_files:
            f = open(glob_file_loc + '\meta\\' + f_meta.replace(".pdf", ".txt"), "w+")
            f.close()


if __name__ == '__main__':
    # obtain the folder location of all of the slides
    if len(sys.argv) == 3:
        glob_file_loc = str(sys.argv[1])
        adobe_loc = str(sys.argv[2])
        set_notes()
        app.run()
    else:
        print('usage: folder_location_pdf_files file_location_AcroRd32.exe')
