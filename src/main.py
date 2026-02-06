import textnode
import os, io, sys
import shutil
from blocknode import markdown_to_html_node, extract_title

PATH_INPUT = "static"
#PATH_OUTPUT = "public"
PATH_OUTPUT = "docs"
PATH_TO_LOGGER = "logger.txt"
VERBOSE = False
BASENAME = "/"

def logger(text):
    if VERBOSE:
        with open(PATH_TO_LOGGER,"a") as file:
            file.write(text + "\n")
    #print(text)

def copy_file(path_input, path_output, logger_fun ):
    if os.path.isfile(path_input):
        shutil.copy(path_input, path_output)
        return
    for item in os.listdir(path_input):
        full_path = os.path.join(path_input,item)
        full_path_output = os.path.join(path_output,item)
        if os.path.isfile(full_path):
            shutil.copy(full_path, path_output)
            logger_fun("Copied {} to {}".format(full_path,full_path_output))
            continue
        os.mkdir(full_path_output)
        logger_fun("Copied folder {} to {}".format(full_path,full_path_output))
        copy_file(full_path, full_path_output, logger_fun)
    return
        
def copy_static_to_public(path_input, path_output, logger_fun):
    if not os.path.exists(path_input):
        logger_fun("Input parh doesnt exist: {}".format(path_input))
        raise ValueError("Input parh doesnt exist: {}".format(path_input))
    if not os.path.exists(path_output):
        os.mkdir(path_output)
        logger_fun("Folder {} created".format(path_output))
    output_file_list = os.listdir(path_output)
    if output_file_list != None:
        shutil.rmtree(path_output)
        os.mkdir(path_output)
        logger_fun("Folder {} was emptied".format(path_output)) 
    input_file_list = os.listdir(path_input)
    copy_file(path_input, path_output, logger)

def generate_page(from_path, templete_path, dest_path):
    print("Generating page from {} to {} using {}".format(from_path, templete_path, dest_path))
    md_content = ""
    templete_html = ""
    with open(from_path, 'r') as file:
        md_content = file.read()
    with open(templete_path, 'r') as file:
        templete_html = file.read()
    html_content = markdown_to_html_node(md_content)
    title = extract_title(md_content)
    templete_html = templete_html.replace("{{ Title }}", title).replace("{{ Content }}", html_content.to_html())
    templete_html = templete_html.replace("href=\"/","href=\"{}".format(BASENAME)).replace("src=\"/","src=\"{}".format(BASENAME))

    dir, _ = os.path.split(dest_path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(dest_path, 'w') as file:
         file.write(templete_html)

def generate_pages_recursive(from_path,templete_path, dest_path, logger_fun):
    if os.path.isfile(from_path):
        full_path_output = "{}.{}".format(os.path.join(dest_path, os.path.splitext(os.path.basename(from_path))[0]), "html")
        generate_page(from_path, templete_path, dest_path)
        return
    for item in os.listdir(from_path):
        full_path = os.path.join(from_path,item)
        if os.path.isfile(full_path):
            full_path_output = "{}.{}".format(os.path.join(dest_path, os.path.splitext(item)[0]), "html")
            generate_page(full_path, templete_path, full_path_output)
            logger_fun("Copied {} to {}".format(full_path,full_path_output))
            continue
        full_path_output = os.path.join(dest_path,item)
        os.mkdir(full_path_output)
        logger_fun("Copied folder {} to {}".format(full_path,full_path_output))
        generate_pages_recursive(full_path, templete_path, full_path_output, logger_fun)
    return
    
    
def main():
    global BASENAME
    basepath = ""
    if len(sys.argv) == 2:
        BASENAME = sys.argv[1]
    if VERBOSE:
        with open(PATH_TO_LOGGER,"w") as file:
            file.write("Copy all files from {} to {} started\n".format(PATH_INPUT, PATH_OUTPUT))
    path_input = os.path.join(basepath, PATH_INPUT)
    path_output = os.path.join(basepath, PATH_OUTPUT)
    copy_static_to_public(path_input, path_output, logger)
    content_path = os.path.join(basepath, "content")
    template_path = os.path.join(basepath, "template.html")
    public_path = os.path.join(basepath, PATH_OUTPUT)
    generate_pages_recursive(content_path, template_path, public_path, logger)

main()

