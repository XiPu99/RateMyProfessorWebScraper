import requests

url = 'http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=20&q={0}+AND+schoolid_s%3A1350&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='.format('Owen Astr')

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

elif numFound == 1:
    id = responseObj['docs'][0]['pk_id']
    pageNum = 1
    url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid={0}&page={1}&max=20&cache=false'.format(id, pageNum)
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    ratings = data['ratings']
    for rating in ratings:
        print(rating['rComments'])
        print()

else:
    print(str(numFound) + ' results found:')

    results = responseObj['docs']
    for prof in results:
        print(prof['teacherfirstname_t'] + ' ' + prof['teacherlastname_t'])
