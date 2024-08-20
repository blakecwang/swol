#!/usr/bin/env python
import sys
from openai import OpenAI


client = OpenAI()

english_to_spanish = sys.argv[1] == "es"
words = " ".join(sys.argv[2:])

if english_to_spanish:
    messages=[
        {
            "role": "system",
            "content": """
            You are a 21-year old natural-born Colombian man living in Bogotá, Colombia.
            The way you talk is concise, direct, and very respectful but also utilizes current slang.
            You love to surf and sometimes talk like a Colombian surfer.
            """,
        },
        {
            "role": "user",
            "content": f"""
            Translate the following English into natural Colombian Spanish
            the way a natural-born Colombian speaker would say it, preserving intent
            and tone and not worrying about direct word-for-word translation: {words}
            """,
        },
    ]

else:
    messages=[
        {
            "role": "system",
            "content": """
            You are a 35-year old English-speaking man living in San Diego, CA.
            Your interests are surfing and software programming. You speak in a concise,
            direct, and very respectful manner.
            """,
        },
        {
            "role": "user",
            "content": f"""
            Translate the following Spanish into natural Californian English
            the way a fluent native-born California would speak, preserving the intent
            and tone and not worrying about word-for-word translation: {words}
            """,
        },
    ]

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
)

content = completion.choices[0].message.content
if content.startswith('"'):
    content = content[1:]
if content.endswith('"'):
    content = content[:-1]
print(content)
