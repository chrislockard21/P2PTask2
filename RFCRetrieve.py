# from urllib.request import urlopen

# def downloadRFC(args):
#     # for arg in args:
#     data = urlopen("http://www.rfc-editor.org/rfc/rfc" + str(args) + ".txt")
#     with open('RFC' + str(args), 'w') as f:
#         for line in data:
#             if line.decode().find('Title') > 0:
#                 f.write(line.decode())

# import threading

# RFCs = [1,2,3,4,5]

# for r in RFCs:
#     new = threading.Thread(target=downloadRFC, args=(r,))
#     new.start()

test_string = 'PQUERY P0\nHOST localhost\nPORT 9999\nPIERS\nP0-localhost-9999\nP0-localhost-9999'

string_parsed = test_string.split()

if string_parsed[7] != 'No-piers-active':
    i = 7
    while i < len(string_parsed):
        print(string_parsed[i].split('-'))
        i += 1