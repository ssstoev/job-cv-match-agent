from unstructured.partition.pdf import partition_pdf

def extract_elements_from_pdf(path: str):
    elements = partition_pdf(filename=path)
    content = []
    for el in elements: 
        content.append(el.text) # put the entire resume text in a list
    return content

# elements = extract_elements_from_pdf('CV_Stefan_Stoev.pdf')
# print(elements)

# for el in elements:
#     print(f"[{el.category}] {el.text}")
