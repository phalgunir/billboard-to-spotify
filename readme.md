The program works like a 'Musical Time Machine' where the user is transported to a past date by listening to a playlist of songs played during that time.
It works by fetching the songs on Billboard Hot 100 list for a particular date and creating a Spotify playlist.

'BeautifulSoup' library is used to scrape the Billboard Hot 100 list.   
The Spotify Client ID and Secret are got by creating an app on - https://developer.spotify.com/dashboard/.  
Then the 'spotipy' library is used to easily authenticate with Spotify OAuth2. The user has to give permission for the app to access the spotify data.      

It asks for the user to input a date in the past. If a future date is entered, the current date, which is the latest, is considered.
The Billboard Hot 100 song names are then got by scraping the website 'https://www.billboard.com/charts/hot-100/' using BeautifulSoup. 
Once the song names are fetched, spotipy library is used to search for the songs' IDs on spotify. If a song is not found on spotify, it is skipped. 
A new playlist is then created with all the songs and the link to open the playlist is printed to the console.      
