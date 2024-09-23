import sys,os,workflow

def html_header():
    filename=os.getcwd() + "/my_style.css"
    file=open(filename,'r')
    style=file.read()
    file.close() 
    return "<!DOCTYPE html>\n<html>\n<body>\n<head>\n<style>\n"\
            + style + "</style>\n</head>\n\n<table>\n\n"

def html_footer():
    return "</table>\n</html>\n</body>\n"

def html_title(title):
    return "<tr><td class=\"title_cell\">" + title + "</td><td class=\"title_cell\"> &nbsp; </td></tr></table><table>\n"

def html_line(entry, position):
    if position == "1":
        part="<tr><td class=\"column"+position+"\">" + entry + "</td>\n"
    else:
        part="<td class=\"column"+position+"\">" + entry + "</td>\n</tr>"
    return part


def html_section(entry, col):
    part=""
    # Adds the section title
    part += "<tr><td class=\"column"+col+"\"><div class=\"section\">" + entry + "</div></td> <td class=\"column"+col+"\"> &nbsp; </td></tr>\n"
    
    return part
    
def standard_entry(command,comment,position):
    comment_html=comment.encode('ascii','xmlcharrefreplace').decode('utf-8')
    command_html=command.encode('ascii','xmlcharrefreplace').decode('utf-8')
    return html_line("<div class=\"comment\">"+comment_html \
                                    +"</div>\n<div class=\"command\">"+command_html+"</div>",position)
    
def create_html(entries):
    html_page_list=[]
    line=entries.pop(0)
    type=line.get("type")
    if type=="title":
        html_page_list.append(html_title(line.get("command")))

    col=1 # 0 = left column / 1 = right column
    totentries = int(len(entries) // 2)  # This will automatically floor the result to an integer
    addextra = False

    # Check if the length of entries is odd
    if len(entries) % 2 != 0:
        addextra = True

    for x in range(totentries):
        html_page_list.append(html_line(entries[x],"1"))
        html_page_list.append(html_line(entries[x+totentries],"2"))

    if addextra:
        html_page_list.append(html_line(entries[totentries+1],"1"))
        html_page_list.append(html_line("","2"))

    html_page= html_header() + "\n".join(html_page_list) + html_footer()
    return html_page


def create_html_global_search(entries,keyword,sheetName):
    html_page_list=[]
    if sheetName==None:
        html_page_list.append(html_title("Global search term: " + keyword))
    else:
        html_page_list.append(html_title("Local search of term \'" + keyword +"\' in \'"+ sheetName + "\'"))

    col=0
    totentries = len(entries) / 2 

# Finally write the html page
    html_page= html_header() + "\n".join(html_page_list) + html_footer()
    return html_page

