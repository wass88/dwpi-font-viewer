import os
import pandas as pd


def csv_to_html_grouped(csv_path, woff2_font_path, output_html):
    """
    Converts a CSV file to an HTML grouped view using a specified WOFF2 font.

    Parameters:
        csv_path (str): Path to the input CSV file.
        woff2_font_path (str): Path to the WOFF2 font file.
        output_html (str): Path to save the generated HTML file.

    Returns:
        None
    """
    # Load the CSV data
    df = pd.read_csv(csv_path)

    # Group by '関連文字' and sort by '総画数'
    grouped = df.sort_values('総画数').groupby('関連文字')

    # HTML header with embedded WOFF2 font
    html_header = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>行政事務標準当用明朝フォントビューア</title>
        <style>
            @font-face {{
                font-family: 'DWPIMincho';
                src: url('{woff2_font_path}') format('woff2');
                font-weight: normal;
                font-style: normal;
            }}
            body {{
                font-family: 'DWPIMincho', sans-serif;
                margin: 20px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
                gap: 10px;
            }}
            .grid-item {{
                text-align: center;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 48px;
            }}
            .related-item {{
                font-weight: bold;
                color: #FF6347;
            }}
            .block {{
                display: contents;
            }}
            .links {{
                margin-top: 20px;
                font-size: 16px;
            }}
            .links a {{
                color: #1E90FF;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <h1>行政事務標準当用明朝フォントビューア</h1>
        <div class="links">
            <p><a href="https://www.digitalwidearea.org/dwpi_mincho" target="_blank">DWPI Mincho</a></p>
            <p><a href="https://drive.google.com/file/d/1DZCewoIPi9hccEMAC1PeXFRfx4HMhBMX/view" target="_blank">フォントライセンス</a></p>
        </div>
        <div class="grid">
    """

    # Generate grouped HTML blocks
    grouped_html = ""
    for related, group in grouped:
        grid_items = "\n".join(
            [
                f'<div class="grid-item related-item">{
                    related}</div>' if idx == 0 else f'<div class="grid-item">{row.DWPI明朝文字}</div>'
                for idx, row in enumerate(group.itertuples())
            ]
        )
        grouped_html += f"<div class='block'>{grid_items}</div>"

    # HTML footer
    html_footer = """
        </div>
    </body>
    </html>
    """

    # Combine and save the HTML
    with open(output_html, "w", encoding="utf-8") as html_file:
        html_file.write(html_header + grouped_html + html_footer)


if __name__ == "__main__":
    csv_path = "dwpi_dict.csv"  # Input CSV file
    woff2_font_path = "DWPIMincho.woff2"  # Path to the WOFF2 font
    output_html = "output.html"  # Path to save the generated HTML

    csv_to_html_grouped(csv_path, woff2_font_path, output_html)
