# PythonSearchEngine

It is a simple search engine coded in python capable of answering single-word search queries efficiently.

The user needs to give a seed page url as input. The seed page can be any valid url which is used by the program to crawl the web.
A good seed page is the one with many links embedded in it as it helps to crawl the web quite efficiently.

Given the seed page url, the program takes a coule of minutes (usually 15-20 min) depending upon the seed page ,to fetch and preprocess the data crawled.

On calculating all the results, user can make infinite number of single-word queries and the program displays the top results based on the search.

The heart of the program lies in the algorthm used to fetch data and calculate results. The very famous Page Rank algorithm has been used in the program which was used by Google in its initial days. The results are sorted in decreasing order of their ranks calculated with their ranks displayed alongside.
