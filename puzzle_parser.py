import puz
# import json 

def parse_puz_file(filepath):
    print("Starting puzzle parsing.")
    p = puz.read(filepath)

    width, height = p.width, p.height
    numbering = p.clue_numbering()

    #build empty grid and start filling
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            index = r*width + c
            is_black = p.solution[index] == "."

            row.append({
                "row": r,
                "col": c,
                "is_black": is_black, 
                "number": None,
                "solution": "" if is_black else p.solution[index]
            })
        grid.append(row)

    for item in numbering.across:
        r = item["cell"]//width
        c = item["cell"]%width
        grid[r][c]["number"] = item["num"]

    for item in numbering.down:
        r = item["cell"]//width
        c = item["cell"]%width
        grid[r][c]["number"] = item["num"]

    clues = {
        "across": [
            {"number": item["num"], "clue": item["clue"]}
            for item in numbering.across
        ],
        "down": [
            {"number": item["num"], "clue": item["clue"]}
            for item in numbering.down
        ]
    }

    return {
        "title": p.title,
        "author": p.author,
        "copyright": p.copyright,
        "width": width,
        "height": height,
        "grid": grid,
        "clues": clues
    }

if __name__ == "__main__":
    try: 
        filepath = "C:/Users/tilly/NYTcrossword/NYTpuzzle_example.puz"
        data = parse_puz_file(filepath)
        print("Loaded puzzle: ", filepath)

    except FileNotFoundError: 
        print("Couldn't find filepath: ", filepath)
