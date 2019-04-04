# Summarizing body of recipe blog posts
If you've ever looked for recipes online you might've come across blogs where you had to scroll through lengthy anecdotes before getting to the good stuff. My goal is to create an algorithm that will analyze all that text and return only the information that is relevant to the recipe. 

## Outline
1. The Data
    - What is it? 
    - Where did it come from?

2. Making it usable
    - Google Universal Sentence Encoder
    - Label Engineering for training

3. Modeling
    - What didn't work and why
    - What did work and why

4. Results
    - Examples of succesful blog post conversion
    - Recreating this project

5. Further Steps
    - Web app / plugin
    - ??? Profit

## The Data
The data needed for this project doesn't exist anywhere neatly so I needed to scrape a bunch of recipe blog poast from the general web. I got blog posts from some of the most popular food blogs, that are written in English. From these post I grabbed the text that made up the body of the post as well as the instructions from the recipe card at the bottom. This took some time as every blog is formatted in a slightly different way. The raw scraped data ended up looking like this:
SAMPLE DATA IMAGE
Each sentence has a corresponding arbitray post label so the body sentences and instruction sentences from the same posts can be kept together. I kept data from unique blogs in seperate files to aid in train/test splitting my data later.

## Making it usable
I used Google's Universal Sentence Encoder(GUSE) to create vectorizations of every sentence. I want to capture the whole sentence rather than the words within. I tried using TFIDF vectorizations, based on inverse word frequency, but it created huge vector with less information than GUSE. GUSE also produces vectors of length 512 which is more managable than the length of vectors produced by other sentence encoders, like Skip-Thoughts.
Once I had the vectors for both the bodies and the sentences I could use cosine similarity to generate labels for the body sentences, relevant or not. In this way I defined relevance as similarity to the final recipe. 

![heatmap](https://github.com/masoncla/capstone/blob/master/heatmap.png)