import os
import glob
import yaml
import pandas as pd
import tabulate # requierd to use to_markdown()

# Read all YAML files in the **CURRENT** directory
def read_yaml():
    regs = []
    for filename in glob.glob(os.path.join(os.path.dirname(__file__), "../countries/*.yaml")):
        with open(filename, "r", encoding="utf-8") as f:
            r = yaml.safe_load(f)
            df = pd.DataFrame(pd.json_normalize(r))

        regs.append(df)

    try:
        return pd.concat(regs)

    except:
        print("Directory countries not found or without any YAML file in it")
        exit()


# Create the panorama for Markdown export
# The panorama DataFrame will be transposed before writing to Markdown
def create_panorama(df):
    
    # Subset of useful information
    panorama = df.filter(["regulation",
                          "shortname",
                          "author",
                          "URL",
                          "date-of-issue",
                          "is-inforce",
                          "scope",
                          "target",
                          "application",
                          "certification",
                          "baseline",
                          "additional-requirements",
                          "assurance-levels",
                          "is-ETSI-required",
                          "can-ETSI-comply",
                          "is-other-reference"], axis=1)

    # Human-readable titles for each line of the final table (remember: the result will be transposed)
    panorama.columns = ["Regulation",
                        "Shortname",
                        "Author",
                        "URL",
                        "Date of issue",
                        "Is the regulation in force?",
                        "Scope",
                        "Target actors",
                        "Mandatory or voluntary?",
                        "Is there a label or certification?",
                        "Does the regulation mandate baseline security requirements?",
                        "Are there additional requirements to the baseline security?",
                        "Does the regulation contains assurance levels?",
                        "Is compliance with ETSI EN 303 645 a requirement?",
                        "Can ETSI EN 303 645 be used to comply with the regulation?",
                        "Are other standards or guidance referenced? (cf. regulation)"]

    return panorama

# Adapt header and URLs to Markdown
def create_markdown_table(panorama):
    # Header will be country code + id (country name)
    panorama.index = df["country-code"] + " " + df["id"]

    # Replace Markdown URLs for readability (where URL starts with http)
    panorama["URL"][panorama.URL.str.contains("http")] = "[Source](" + panorama["URL"] + ")"

    # And write the transposed panorama to file
    with open("table.md", "w", encoding="utf-8") as fw:
        fw.write(panorama.transpose().to_markdown())
    
    return 1


# Adapt header and URLs to HTML
def create_HTML_table(panorama):
    # Header will be country flag (image) + id (country name)
    panorama.index = '''<img src="''' + df["country-flag"] + '''" height="16"> ''' + df["id"]

    # Replace URLs for readability (where URL starts with http)
    panorama["URL"][panorama.URL.str.contains("http")] = '<a href="' + panorama["URL"] + '">Source</a>'


    # And write the transposed panorama to file
    with open("table.html", "w", encoding="utf-8") as fw:
        fw.write(panorama.transpose().to_html().replace("&lt;", "<").replace("&gt;", ">")) # remove the URL encoding for images
    
    return 2


if __name__ == "__main__":

    df = read_yaml()
    panorama = create_panorama(df)

    try:
        create_markdown_table(panorama.copy(deep=True))

    except:
        print("Error: cannot create Markdown table.")
        exit()

    print("Successfully created Markdown table in: " + os.path.join(os.getcwd(), "table.md"))


    try:
        create_HTML_table(panorama.copy(deep=True))

    except:
        print("Error: cannot create HTML table.")
        exit()
    
    print("Successfully created HTML table in: " + os.path.join(os.getcwd(), "table.html"))