import pandas as pd
import mecsimcalc as msc
import matplotlib.pyplot as plt

def main(inputs):

    # get the input file
    input_file = inputs['file']

    # convert the input file to a dataframe
    df = msc.input_to_dataframe(input_file)
    # define the specific columns we want plotted
    cols = [0, 1]
    df = df[df.columns[cols]]
    # covert the dataframe to an HTML table and generate a download link
    html_table, download_link = msc.print_dataframe(df, download=True)

    x=df["Food"]
    y=df["Costco"]
    #plt.plot(x, y)
    plt.rcParams.update({'font.size': 5})
    plt.bar(x, y, width=0.3)
    # plt.bar(x, "Walmart", width=0.3)
    plt.xlabel("Food")
    plt.ylabel("Prices")
    plot_html = msc.print_plot(plt)

    return {
        # Return the HTML table
        "table": html_table,
        # Returns the HTML download link
        "download": download_link,"plot": plot_html
    }

"""    OUTPUTS

    Displaying Table and Plot of Food Prices
<!-- Output the HTML table -->

{{ outputs.table }}	{{ outputs.plot }}





Downloading Spreadsheet
<!-- Output the Download Link -->

{{ outputs.download }}



{{ outputs.plot }}"""
