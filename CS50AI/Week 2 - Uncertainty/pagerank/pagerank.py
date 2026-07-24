import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition = {}
    prob = 0
    links_to = corpus[page]
    # If page has no outgoing links
    if len(links_to) == 0:
        prob = 1 / len(corpus)
    else:
        prob = (1 - damping_factor) / len(corpus)

    prob = round(prob, 5)

    for i in corpus:
        transition[i] = prob
    
    if len(links_to) != 0:
        prob = damping_factor / len(links_to)
        prob = round(prob, 5)
        for i in links_to:
            transition[i] += prob
    return transition


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for i in corpus:
        pagerank[i] = 0

    page = random.choice(list(corpus.keys()))
    pagerank[i] += 1 / SAMPLES

    for _ in range(SAMPLES - 1):
        transition = transition_model(corpus, page, damping_factor)
        
        x = random.random()
        for i in transition:
            if transition[i] > x:
                page = i
                pagerank[i] += 1 / SAMPLES
                break
            x -= transition[i]
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    links_to = {}
    for i in corpus:
        pagerank[i] = 1 / len(corpus)

        if i not in links_to:
            links_to[i] = set()

        # Create a dict of pages linking to a page
        for link in corpus[i]:
            if link not in links_to:
                links_to[link] = set()
            links_to[link].add(i)

        # If page does not have any links, should be interpreted as having one link for every page (including itself)
        if len(corpus[i]) == 0:
            links_to[i].add(i)
            for link in links_to:
                links_to[link].add(i)

    def calc_pagerank(page):
        rank = (1 - damping_factor) / len(corpus)
        temp_rank = 0
        for link in links_to[page]:
            num_links = len(corpus[link])
            if num_links == 0:
                num_links = len(corpus)

            temp_rank += pagerank[link] / num_links
        rank += damping_factor * temp_rank
        return rank

    while True:
        counter = 0
        for page in corpus:
            new_rank = calc_pagerank(page)
            if abs(new_rank - pagerank[page]) <= 0.001:
                counter += 1
            pagerank[page] = new_rank

        if counter == len(corpus):
            return pagerank


if __name__ == "__main__":
    main()
