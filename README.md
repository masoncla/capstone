# Summarizing body of recipe blog posts
If you've ever looked for recipes online you might've come across blogs where you had to scroll through lengthy anecdotes before getting to the good stuff. My goal is to create an algorithm that will analyze all that text and return only the information that is relevant to the recipe. 

### Steps
1. I scraped blog posts from a few of the most popular recipe based blogs in English to get both the body of the recipe post, and the instructions from the recipe card at the bottom.

2. I then used Google's Universal Sentence Encoder to create a vector representation of each sentence in the body and instuctions of each post.

3. I then created a similarity matrix, using cosine similarity, to compare the body to the instructions. I assigned the max value of each row to its corresponding body sentence as the "correlation score". 
![heatmap](https://github.com/masoncla/capstone/blob/master/heatmap.png)
4. Right now I've classified anything with a correlation over 0.75 as relevant and using classification. I've found this to be accurate.
4. My current model uses K Nearest Neighbors to predict whether a new sentence is relevant of not. Thus far I'm still getting a lot of false positives, about the same as true positives, but my false negative rate is pretty low.
5. The end product would take a new post body in and return only those sentences predicted to be useful. This could be extended to comments but would most likely require a new target engineered or a the least a thorough investigation of the current system. 'Action words' could be an important distinction between a useful comment and one that's not.