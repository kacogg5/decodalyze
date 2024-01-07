# WIP - Language Analyzation Tool Suite

A suite of tools for comparing documents of 2 different languages, for the purpose of analyzing the grammatical structure and word-for-word translations.

## Why am I making this?
A brief history of how this came to be and what this is meant to be.

For a long time I've been fascinated by anime and more importantly, Japanese culture and language. I wanted to learn Japanese but was put off by traditional learning methods. I started copying anime song lyrics, both the romanized version and english translations and using Notepad++ to manually deduce the lyrics' meaning, word for word. As my text file grew with more and more songs, I implemented a simple command line tool in java for assisting in this process. While this method worked for a while, it did not account for alternate romanized spellings, and it still required having the text file open alongside the terminal.

My vision for this project would be an all-in-one interface where I can perform the document analyzation. The ideal application would include the following features (in order of decreasing importance):
  - A viewport showing a user-selected document, with lines from language A and language B paired together respectively.
  - A system of highlighting words or phrases indicating suredness of the term's meaning in the current context.
  - A system for selecting and linking terms from language A to language B.
  - When a term is selected in the document viewport, a viewport showing all related uses of the selected text. This would idealy catch and display alternate transliterations as well.
  - A dictionary where the user can make notes about words and their supposed meanings.
  - An easy method of uploading new documents and their translated versions.
