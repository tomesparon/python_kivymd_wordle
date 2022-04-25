# Wordle KivyMD

- Game of Wordle

Original code that this fork is based on is found here: 
[https://github.com/tech-boost-nakanishi/python_kivy_wordle](https://github.com/tech-boost-nakanishi/python_kivy_wordle)

Changes from Original
- [x] Uses English
- [ ] Uses KivyMD widgets and navbar
- [x] Light/Dark Theming
- [x] Added different wordlist of 5000
- [x] Bugfix: Repeated characters are marked as amber when not in secret word
[^1]






[^1]: For example, if the guess is HELLO and the secret is APPLE, then the previous behavior causes the first occurrence of the L to be yellow (because it does appear in the word), but then the second L will be green (because it is in the right position).

On a letter-by-letter basis, this behavior appears fine. But when the entire word is considered, that first L shouldn't appear yellow. Instead, it should appear grey. That's because there is already another L in the guess that 'claims' the occurrence of the L in the secret.
This was changed in main.py





## Requirements
(see requirements.txt)
- Python 3.9.1
- Kivy 2.1.0
- kivymd 0.104.2