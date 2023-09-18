# slfm.py - SetListForMoxfield
This script simplifies a portion of the process of importing Magic the Gathering (MtG) cards to a collection in Moxfield.

Details about adding cards via csv are documented at: https://www.moxfield.com/help/importing-collection

The script uses the provided MtG setcode to pull a list of all cards from the specified set from ScryFall. The data is output to a csv file containing the minimum field data required for import to Moxfield.

The user can then modify card counts (as well as condition, language, and foil detail as desired) in the file and import it to Moxfield.
