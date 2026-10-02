from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import os

def main():
    pdf = MarkdownPdf(toc_level=2)
    
    with open('crypto_project_documentation.md', 'r', encoding='utf-8') as f:
        text = f.read()
        
    pdf.add_section(Section(text))
    pdf.meta["title"] = "Cryptanalysis Project Documentation"
    pdf.meta["author"] = "Project Team"
    
    pdf.save('Crypto_Analysis_Project_Documentation.pdf')
    print("PDF generated successfully at Crypto_Analysis_Project_Documentation.pdf")

if __name__ == '__main__':
    main()
