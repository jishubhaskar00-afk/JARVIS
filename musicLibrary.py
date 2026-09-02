import urllib.parse
import webbrowser

music = {
    "skyfall": "https://www.youtube.com/watch?v=sZrTJetgRlU",
    "stealth": "https://www.youtube.com/watch?v=U47Tr9BB_wE",
    "march": "https://www.youtube.com/watch?v=Xqeq4b5u_Xw",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "let me love you": "https://www.youtube.com/watch?v=euCqAq6BRa4",
    "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    "night changes": "https://www.youtube.com/watch?v=syFZfO_wfMQ",
    "mockingbird": "https://www.youtube.com/watch?v=S9bCLPwzSC0",
    "starboy": "https://www.youtube.com/watch?v=34Na4j8AVgA"
}

def play_song(song_name: str) -> bool:
    """
    Plays from preset library if matched, or searches YouTube directly.
    """
    song_name = song_name.lower().strip()
    if not song_name:
        return False
    
    # 1. Exact match
    if song_name in music:
        webbrowser.open(music[song_name])
        return True
    
    # 2. Substring match
    for key, url in music.items():
        if key in song_name or song_name in key:
            webbrowser.open(url)
            return True
            
    # 3. YouTube Fallback (plays ANY song)
    encoded_query = urllib.parse.quote(song_name)
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(youtube_search_url)
    return False