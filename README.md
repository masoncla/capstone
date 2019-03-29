## General Outiline
* Use Google's Universal Sentence Encoder to find semantic similarity between sentences in the posts
* Use clustering or KNN to find groups of similar sentences
    * The number of groups will be the final number of desired sentences in the summary. (need to figure out that number)
* The sentences chosen will be those closest to the center of their cluster
* Return a string of the summary, those central sentences, in a coherent order
