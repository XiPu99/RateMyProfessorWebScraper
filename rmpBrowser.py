import requests, sys, webbrowser

# check if user has entered a valid ID number
def checkIfValid(id, allIDs):
    return len(id) != 0 and int(id) in allIDs

# check if users have entered more than one command line arguments
if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
    url = 'http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=20&q={0}+AND+schoolid_s%3A1350&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='.format(name)

    r = requests.get(url)
    r.raise_for_status()

    # attempt to decode JSON we get from
    try:
        data = r.json()
    except ValueError:
        print('Attempt to decode JSON has failed')

    responseObj = data['response']
    numFound = responseObj['numFound']

    if numFound == 0:
        print('No results found.')

    # exactly one result is found
    elif numFound == 1:
        id = responseObj['docs'][0]['pk_id']
        url = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid={0}&showMyProfs=true'.format(id)
        webbrowser.open(url)

    # more than one result are found
    else:
        print(str(numFound) + ' results found:')
        results = responseObj['docs']
        ids = []

        # print all search results
        for prof in results:
            print(prof['teacherfirstname_t'] + ' ' + prof['teacherlastname_t'] + ' ID: ' + str(prof['pk_id']))
            ids.append(prof['pk_id'])

        targetID = input('Which professor are you looking for? Enter the ID: ')
        while targetID!='q':
            if checkIfValid(targetID, ids):
                url = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid={0}&showMyProfs=true'.format(targetID)
                webbrowser.open(url)
                break
            else:
                print('Invalid ID number. Enter \'q\' to quit the program or one of the following ID numbers: ')
                print(ids)
                targetID = input('Enter your command or ID now: ')

# no command line argument is entered
else:
    print('Please enter something in the command line argument.')
