import os
import pandas as pd


def get_ivs_code(char):
    """
    Get the IVS (Ideographic Variation Sequence) code for a given character.

    Parameters:
        char (str): A single character.

    Returns:
        tuple: (Main Unicode codepoint, IVS code) where IVS code is empty if not applicable.
    """
    if len(char) == 1:
        return (f"U+{ord(char):X}", "")
    elif len(char) == 2:
        return (f"U+{ord(char[0]):X}", f"U+{ord(char[1]):X}")
    return ("", "")


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

    grouped = df.groupby('関連文字')

    # HTML header with embedded WOFF2 font
    html_header = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>非公式行政事務標準当用明朝フォントビューア</title>
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
                padding: 10px 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 48px;
                line-height: 1;
            }}
            .main-code, .ivs-code, .gj-code, .seiji-code {{
                font-size: 12px;
                color: #777;
                margin-top: 5px;
                display: block;
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
        <h1>非公式行政事務標準当用明朝フォントビューア</h1>
        <div class="links">
            <p><a href="https://www.digitalwidearea.org/dwpi_mincho" target="_blank">DWPI Mincho</a></p>
            <p><a href="https://drive.google.com/file/d/1DZCewoIPi9hccEMAC1PeXFRfx4HMhBMX/view" target="_blank">フォントライセンス</a></p>
            <p>これは非公式のビューアです。一切の保証をするものではありません。</p>
        </div>
        <div class="grid">
    """

    # Generate grouped HTML blocks
    grouped_html = ""
    for related, group in grouped:
        main_code, ivs_code = get_ivs_code(related)
        grouped_html += f'<div class="grid-item related-item">'
        if main_code:
            grouped_html += f'<span class="main-code">{main_code}</span>'
        grouped_html += related
        if ivs_code:
            grouped_html += f'<span class="ivs-code">{ivs_code}</span>'
        else:
            grouped_html += f'<span class="ivs-code">.</span>'

        grouped_html += '</div>'
        grid_items = "\n".join(
            [
                f'<div class="grid-item"><span class="gj-code">{
                    row.MJ文字図形}</span>{row.DWPI明朝文字}'
                f'{f"<span class=\"seiji-code\">{
                    row.正字1CD}</span>" if pd.notna(row.正字1CD) else ""}</div>'
                for _, row in group.iterrows()
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
    output_html = "dist/index.html"  # Path to save the generated HTML

    csv_to_html_grouped(csv_path, woff2_font_path, output_html)
