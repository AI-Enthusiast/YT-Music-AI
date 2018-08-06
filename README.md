# YT Music AI

Scraps music from YT as MP3 and stores data about music on CSV. Music is given a general score based on how well it performs on YT. It then analyzes the MP3 files and learns the characteristics of high performing music. Model is then trained to predict high performing songs, selects underrated music from downloaded music for YT upload.

## Dependencies

* glob - For file parsing.
* os - Deals with path and file changes.
* googleapiclient - For using the yt-data api and downloading videos as mp3.
* oauth2client - Authentication client for googleapiclient.
* csv - For storing data about the music long term for minimal storage space.
* beautifulSoup - For parsing the raw html of web pages.
* urllib - For connecting and decoding web page for beautifulSoup.

## Running the Tests
Testing is done through unitTests for HashTable, MusicHashTable, and YT_Bot 

Run testing from 'main.py'
1. Run main.py
2. Type your path to 'main.py' at the '>>' prompt
3. Type 'test'
or
1. Run UnitTests.py directly

Hopefully it looks like this:
```
>>test
>COMMENCE TESTING...
>TEST readData():				PASS
>TEST saveHeader():				PASS
>TEST saveData():				PASS
>TEST appendData():				PASS
>TEST getStats():				PASS
>TEST clear():					PASS
>TEST toCurrent():				PASS
>TEST updateCSV():				PASS
```
If not create an error report or investigate yourself

### Test Breakdown

* TEST readData():	Reads the csv and returns as a list.
* TEST saveHeader():	Saves a string as a header to csv.
* TEST saveData():	Saves a dic to csv.
* TEST appendData():	Appends data entry to bottom of csv.
* TEST getStats():	Gets likes, dislikes, and views by parsing with beautifulSoup.
* TEST clear():		Clears csv. Also used to create csv when one does not exist.
* TEST toCurrent():	Moves *.mp3's in the main path to /Music/New/ before processing
* TEST updateCSV():	Updates csv with music in /Music/New/ then moves them to /Music/Current

## Built With

 [PyCharm](httpswww.jetbrains.com/pycharm/) - Python IDE 
 
## Contributing

Please read [CONTRIBUTING.md](httpsgist.github.comPurpleBoothb24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

 * Cormac Dacker - Author - [AI-Enthusiast](httpsgithub.comAI-Enthusiast)
 * Marilyn Groppe - Co Author - [MJGroppe](httpsgithub.commjgroppe)


## Acknowledgments

 No copyright infringement intended, please contact the authors before seeking legal settlement
