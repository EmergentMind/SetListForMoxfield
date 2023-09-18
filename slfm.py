# slfm.py - SetListForMoxfield

import csv
from pathlib import Path
import requests
import sys
import time
import unicodedata

# gracefully handle cmdline args
if (args_count := len(sys.argv)) > 2:
    print(f"You can only provide one setcode at a time.")
    raise SystemExit(2)
elif args_count < 2:
    print(f"You must specify a setcode. Example: For Streets of New Capenna, the setcode is \'snc\'")
    raise SystemExit(2)
setcode = str(Path(sys.argv[1]))

# Endpoint details: https://scryfall.com/docs/api/sets/code
# Retrieve cardset object for the provided setcode
target_endpoint = 'https://api.scryfall.com/sets/' + setcode

# Load the cardset object and parse for card data uri so we can read card specific data.
cardset_data = requests.get(target_endpoint).json()
card_data_uri = cardset_data['search_uri']

# Create or open an exiting csv file for the set so that we can write to it
# If the file already exists, it will be overwritten
with open(setcode +'.csv', 'w', newline='') as csvfile:
    #define the csv column headers expected by Moxfield - https://www.moxfield.com/help/importing-collection
    columnheaders = ['Count', 'Name', 'Edition', 'Condition', 'Language', 'Foil', 'Collector Number']
    csvwriter = csv.DictWriter(csvfile, fieldnames = columnheaders)
    csvwriter.writeheader()

    # Scryfall's set search returns only 175 cards per page so we'll have to paginate through the set using their
    # 'has_more' key that is retuned in the uri response.
    has_more_data = True
    page_num = 0
    exceptions = []

    while has_more_data:
        # Prep the uri for the current page of results
        page_num += 1
        current_page_uri = card_data_uri + '&page=' + str(page_num)
        data = requests.get(current_page_uri).json()

        # Write the data we want from the response into the csv file
        for object in data['data']:
                try:
                    name = object['name']
                    #normalize accented characters that Moxfield will barf on
                    name = unicodedata.normalize('NFKC', name)
                    collector_num = object['collector_number']
                    csvwriter.writerow({'Count': '',
                                    'Name': name,
                                    'Edition': setcode,
                                    'Condition': 'NM',
                                    'Language': 'English',
                                    'Foil': '',
                                    'Collector Number': collector_num
                                    })
                except:
                    exceptions.append(collector_num)

        # Check if there is another page of data for the set.
        # Wait before a subsequent iteration so we don't overload the API. Scryfall specifics a wait time from 1 to 10ms between requests.
        has_more_data = data['has_more']
        if has_more_data:
            time.sleep(.2)

print(f"Processing completed. Results saved to " + setcode + ".csv")
if len(exceptions):
    print(f'Exceptions:')
    for exception in exceptions:
        print(f'Unable to process collector number ' + str(exception) + ' ; this card was skipped.')
    print(f'Total exceptions: ' + str(len(exceptions)) )
