import requests
import json

uprompt= """

[h1]DOWNLOAD THE NVIDIA GAME READY DRIVERS FOR THE LOVE OF GOD[/h1]
I crashed like twice but didn't have a problem after I got the new game ready drivers. I'm literally making this review as a reminder. Had a blast so far but jesus guys, update your nvidia drivers.

ULTRA EDIT:
[h1]A Flawed but Fun Experience[/h1]

I might as well actually review this game in its current state considering the attention this got, while I have not finished it I feel I have experienced enough of the core mechanics to formulate an accurate opinion at least on the gameplay. 

It is a Witcher 3 reskin with a cyberpunk setting, considering that Witcher 3 was amazing (and I still have yet to get through it entirely) it does translate. Narratively this game excels, the dialogue is well written and acted and the characters are hard to not fall in love with. Walking around the world is exhilarating although unengaging, it is lacking interactivity. That being said the gameplay itself is a lot of fun. The guns pack a huge punch, very satisfying to use. The melee with katanas specifically is fun but broken, I did a body and reflex melee build and was able to behead TONS of foes before they even had time to react. The game is unfortunately plagued with bugs, less severe bugs especially after the recent hotfix but there are a myriad of small immersion raping bugs that pop up here and there Bethesda style. 

Ultimately I invest in player agency/good writing and fun gameplay at the end of the day, the graphics are important but less so. The decision-making of Witcher is here and that's really what I like the most HOWEVER this game was clearly not ready and considering recent events with the dev I will be hard pressed to trust them again. This is an incredibly bad launch. 

All of that being said, if you're the type that is a fan of Deus Ex, Dishonored, or Fallout: New Vegas you will love this game warts and all just for the godlike quest design those and this game offer. Plenty of skill check dialogue to be found. Suffice to say that I have had a good amount of "That actually worked?!?" moments so far which is a really hard feeling to nail down with games like this, you usually only get that out of CRPGs like Age of Decadence or Divinity, etc. At the same time I do not judge anyone that refunds this game or waits for a more stable version to come out because CD PROJEKT RED really dropped the ball and should not have released the game in this state. 

In conclusion, this game is mostly what I expected it to be and it is a shame that people expected this game to be the second coming of Jesus. I was banking on the decision making and quest design and this game delivers on those fronts. Everything else though, it does fail here and there but, in my opinion, not enough to make the game genuinely bad. If I had to give it a score out of ten it would be a solid 8/10. Hopefully CD PROJEKT RED can iron out all of these problems in a timely manner and elevate its standing.

Also driving anything is just plain awful, it depends on what you're driving but in my opinion it should just be the same for whatever you're driving but I'm just talking out of my ass at this point.

---absareview---

Pros:
- BEAUTIFUL game and runs surprisingly well for the graphics quality
- The enemies are a lot of fun to engage with and the combat is as fun as the last game
- New base building/crafting feels more immersive.. though it needs some slight improvements
- Kelvin and Virginia were a really nice addition to the team
- Thank god for the GPS

Cons:
- The story was a huge let down... and this part hurts because it is why I loved the first game so much. The story makes absolutely no sense.. you get all of these interesting clues along the way to have the ending be SUPER rushed and a totally incoherent. Releasing this game in early access was a mistake and it was dishonest.
- The new crafting system is immersive but it takes forever to build because each placement has a mini animation. A mix of the new crafting with the old blueprint system would be awesome.
- The game is way too easy. Getting all the map markers for every single cave and point of interest at the start of the game is a massive mistake. This combined with being able to quick save with the tarp makes the game a cheese and totally eliminates the need for a base. Progression needs to be done in stages
- No boss fight

---absareview---

The open world feels lifeless because of lackluster NPC behavior and plays like a first person GTA knockoff with not enough depth to your actions. Stealing vehicles? Only temporarily. Getting a house in your preferred corner of the world? Nah. Anything meaningful to do apart from story quests, side quests, and shopping? No. It really feels like a game where you get to create a character but don't get the ability to really do anything with them that portrays you, the player, as the character in this world.

This is especially true with the insignificant "branches" or "life paths" which, alongside choices throughout the game, are mostly inconsequential. The game really feels like it wants to cover as much of the "killer features" that people like seeing like custom guns and gear, skill trees, lots of options to tackle combat, driving, etc. but at the cost of any significant depth to those mechanics in order to make the game feel like an RPG instead of a looter-shooter with GTA elements and some differing gameplay depending on your choices every blue moon.
"""

sprompt = """
you are ai assistant to help me analyze video games review with Aspect Based Sentiment Analysis appraoch, your task is :  Analyze the following review and identify the mentioned aspects. For each aspect, classify the sentiment as positive, negative, neutral, or not mentioned, and provide a reason.

there will be multiple review seperated by ---absareview---, make sure to include every aspects for every review even for not mentioned aspect

Aspects to Analyze:
- Gameplay : user comments on gameplay (including but not limited to : gameplay, mechanics, skill tree, etc)
- Graphics fidelity : user comments on fidelity of the graphics (including but not limited to : realism, artstyle, etc), make sure anything related to graphical bugs goes to technical aspect rather than this
- Story : user comments on the story (including but not limited to : story, quest, dialogues, characters story)
- Technical : user comments on the technical sides of the game (including but not limited to : bugs, crash, performance)
- World : user comments on the world building of the game (including but not limited to : city design, environtment)
- Multiplayer : user comments on the multiplayer aspect (including but not limited to : social feature, matchmaking, co-op)
""" 
api = "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"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
  "Authorization": f"Bearer {api}",
  "Content-Type": "application/json"
}

payload = {
  "model": "deepseek/deepseek-chat:free",
  "messages": [
  {
    "role": "system",
    "content": f"{sprompt}"
  },
  {
    "role": "user",
    "content": f"{uprompt}"
  }
],
  "stream": True
}

buffer = ""
with requests.post(url, headers=headers, json=payload, stream=True) as r:
  for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
    buffer += chunk
    while True:
      try:
        # Find the next complete SSE line
        line_end = buffer.find('\n')
        if line_end == -1:
          break

        line = buffer[:line_end].strip()
        buffer = buffer[line_end + 1:]

        if line.startswith('data: '):
          data = line[6:]
          if data == '[DONE]':
            break

          try:
            data_obj = json.loads(data)
            content = data_obj["choices"][0]["delta"].get("content")
            if content:
              print(content, end="", flush=True)
          except json.JSONDecodeError:
            pass
      except Exception:
        break
