import os.path
import sys

def personal_info_from_md_line(txt):
    """Return personal info for lines with links
    
    e.g.
    input:  "`email`    [abc@example.com](mailto:abc@example.com)"
    output: "abc@example.com"
    """

    txt = txt.split("[")[1]
    txt = txt.split("]")[0]
    return txt

def split_cv_line(txt):
    """Return a tuple of the side bar text and title
    
    e.g.
    input:  "*Gen 2000 -- Dec 2020* Example GmbH -- Intern"
    output: ("Gen 2000 -- Dec 2020", "Example GmbH -- Intern")
    """

    if "*" not in txt:
        return "", txt

    txt = txt.split("*", 1)[1]
    txt = txt.split("*")
    side_text = txt[0].strip()
    title = txt[1].strip()
    return side_text, title

class CvBibliography():

    def __init__(self, title):
        self.title = title
        self.style = "plainurl"
        self.add_articles="\\printbibliography[title=Articles, type=article]"
        self.add_acknowledgments="\\printbibliography[title=Acknowledged, type=misc]"
        self.add_books="\\printbibliography[title=Books, type=books]"
        self.add_conferences="\\printbibliography[title=Conference Papers, type=inproceedings]"

    def to_tex(self):
        return "\\renewcommand{{\\refname}}{{{}}}\n\\nocite{{*}}\n{}\n{}\n{}\n{}\n".format(self.title,self.add_articles,self.add_acknowledgments,self.add_books,self.add_conferences)
        #return "\\renewcommand{{\\refname}}{{{}}}\n\\nocite{{*}}\n\\bibliographystyle{{{}}}\n\\bibliography{{{}}}".format(self.title,self.style,"publications.bib")


class CvSection():

    def __init__(self, title):
        self.title = title

    def to_tex(self):
        return "\\section{{{}}}".format(self.title)

class CvEntry():

    def __init__(self, side_txt, title):
        self.side_txt = side_txt
        self.title = title

    def to_tex(self):
        return "\\cventry{{{}}}{{{}}}{{}}{{}}{{}}{{}}".format(self.side_txt, self.title)

class CvItem():

    def __init__(self, side_txt, title):
        self.side_txt = side_txt
        self.title = title

    def to_tex(self):
        title = self.title
        if title.startswith("-"):
            title = "\\( \\circ \\)" + title[1:]
        return "\\cvitem{{{}}}{{{}}}".format(self.side_txt, title)

class CurriculumVitae():

    def __init__(self, language=None):
        if language is None:
            language = "english"
        self.language = language
        self.name = ("John", "Doe")
        self.title = None
        self.content = None

    def from_markdown(self, markdown_src):
        self.content = []
        lines = markdown_src.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("# "):
                line = line.removeprefix("# ")
                self.name = line.split(" ", 1)
                i += 1
                # The first non-empty line after the name is the title
                while lines[i] == "":
                    i += 1
                self.title = lines[i]
                i += 1
                continue
            
            if line.startswith("![]"):
                self.photo = line.split("(")[1].split(")")[0]
                i += 1
                continue

            if line.startswith("`email`"):
                self.email = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`homepage`"):
                self.homepage = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`linkedin`"):
                self.linkedin = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`github`"):
                self.github = personal_info_from_md_line(line)
                i += 1
                continue
            
            if line.startswith("## "):
                section_name=line.removeprefix("## ")
                self.content.append(CvSection(section_name))
                i += 1
                continue

            if line.startswith("### "):
                txt = line.removeprefix("### ")
                side_text, title = split_cv_line(txt)
                self.content.append(CvEntry(side_text, title))
                i += 1
                continue
            
            if line.strip() != "":
                side_text, title = split_cv_line(line)
                self.content.append(CvItem(side_text, title))
                i += 1
                continue

            i += 1

    def add_publications_to_content(self):
        #hacky way to include bibtex file if section is "Publications"
        self.content.append(CvBibliography('Publications'))

    def personal_data_to_tex(self):
        tex_out = []
        tex_out.append("\\name {{{}}}{{{}}}".format(self.name[0], self.name[1]))
        if self.title is not None:
            tex_out.append("\\title{{{}}}".format(self.title))
        if self.photo is not None:
            tex_out.append("\\photo[80pt][0pt]{{{}}}".format(self.photo))
        if self.email is not None:
             tex_out.append("\\email{{{}}}".format(self.email))
        #if self.homepage is not None:
        if self.homepage:
             #skip if string is empty
             print(self.homepage)
             tex_out.append("\\homepage{{{}}}".format(self.homepage))
        if self.linkedin is not None:
             tex_out.append("\\social[linkedin]{{{}}}".format(self.linkedin))
        if self.github is not None:
             tex_out.append("\\social[github]{{{}}}".format(self.github))
        
        tex_out = "\n".join(tex_out)
        return tex_out

    def content_to_tex(self):
        content_lines = [item.to_tex() for item in self.content]
        return "\n".join(content_lines)
    
    def publications_to_tex(self):
        publications_lines = [item.to_tex() for item in self.publications]
        return "\n".join(publications_lines)

    def to_tex(self):
        tex_template = open("cv_template.tex", "rt").read()
        tex_template = tex_template.replace("$language", self.language)
        tex_template = tex_template.replace("$personal_data", self.personal_data_to_tex())
        tex_template = tex_template.replace("$content", self.content_to_tex())
        return tex_template


if __name__ == "__main__":
    src_filename = sys.argv[1]
    if len(sys.argv) > 2:
        language = sys.argv[2]
    else:
        language = None
    cv = CurriculumVitae(language)
    cv.from_markdown(open(src_filename, "rt").read())
    #cv.add_publications_to_content()
    open(os.path.splitext(src_filename)[0] + ".tex", "wt").write(cv.to_tex())
