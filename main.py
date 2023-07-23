from parse import parse
url = input('url: ')
count = input('count of videos:')
filename = input('spreadsheet filename: ')

if __name__ == "__main__":
    parse(url, count, filename)
