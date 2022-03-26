import sys
import os
import json


def make_pdf(targets: list):
    output_file_basename = "计算方法实验" + ("" if len(targets) == 0 else ("(" + "-".join(targets) + ")"))
    files = [file for file in os.listdir("notebooks") if file.endswith("ipynb") and ((sum([t in file for t in targets])) > 0 if len(targets) > 0 else True)]
    list.sort(files)
    with open("notebooks/templates/lab-wrapper.ipynb", "rb") as f:
        template = json.load(f)
        cells = []
        for file in files:
            with open(os.path.join("notebooks", file), "rb") as f2:
                lab_data = json.load(f2)
                cells.extend(lab_data['cells'])
        template['cells'].extend(cells)
        with open(os.path.join("output", output_file_basename + '.ipynb'), "w") as f2:
            json.dump(template, f2)
    
    os.system(f"jupyter nbconvert --to latex {os.path.join('output', output_file_basename + '.ipynb')}")
    tex_text = ""
    with open(os.path.join("output", output_file_basename + '.tex'), "r", encoding="utf8") as f:
        tex_text = f.read()
        insert_at = tex_text.find('\n')
        insert_text = """
    \\usepackage{fontspec, xunicode, xltxtra}
    \\setmainfont{Microsoft YaHei}
    \\usepackage{ctex}
"""
        tex_text = ''.join([tex_text[:insert_at], insert_text, tex_text[insert_at:]])
    
    with open(os.path.join("output", output_file_basename + '.tex'), "w", encoding="utf8") as f:
        f.write(tex_text)
        
    dir_now = os.path.abspath(".")
    os.chdir("output")
    os.system(f"xelatex {output_file_basename + '.tex'}")
    os.chdir(dir_now)


if __name__ == '__main__':
    make_pdf(sys.argv[1:])
