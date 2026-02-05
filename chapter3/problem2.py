name = "manasvi"
date = "10-07-2005"
letter =('''Dear <|name|>,
      You are selected 
      <|date|>''')
print(letter.replace('<|name|>', name).replace('<|date|>', date))