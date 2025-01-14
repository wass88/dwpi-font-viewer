[private]
@default: help

# show help message
@help:
    echo "Usage: just <recipe>"
    echo ""
    just --list

dict_xlsx := "DWPI明朝追加文字属性辞書（暫定版）.xlsx" 
@convert-csv:
    xlsx2csv "{{dict_xlsx}}" dwpi_dict.csv"

font_ttf := "dwpimin/DWPImin004.00/DWPIMincho.ttf"
@convert-woff2:
    npx ttf2woff "{{font_ttf}}" dist/DWPIMincho.woff2

@generate-index:
    python index.py

@deploy:
    npx gh-pages -d dist

@run: convert-csv convert-woff2 generate-index deploy
