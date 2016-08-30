import math


class ItemRecommender(object):
    """Item Recommendation engine.

    Attributes:
        items: A set of item IDs.
        user_prefs: A list of sets representing users' item ID preferences.
    """

    def __init__(self, items, user_prefs):
        """Initialise an item recommender with item IDs and user_prefs.

        Args:
            items: A set of all possible item IDs {1, 2, 3, 5, 6 ...}
            user_prefs: A list of sets of user ID preferences. For example:
                [{3, 4, 5}, {1, 2}, {3, 4, 5, 6}, {3, 2}]

            The first user [0] has expressed preference for items with IDs 3, 4
            and 5 in this example.
        """
        self.items = items
        self.user_prefs = user_prefs

    def recommend(self, query_ids, limit):
        """Recommend items based on similarity to the items in item_ids

        Calculate a score for every item not in query_ids and return the IDs
        with the highest scores. The score of an item is the sum of its
        similarity with each ID in query_ids. Items with the same score
        are tie-broken by their absolute popularities.

        Args:
            query_ids: A set of item IDs to make recommendations for.
            limit: The maximum number of recommendations to return.

        Returns:
            A list of the n most recommended items sorted in descending order of
            similarity where n is less than or equal to limit. For example:

            [4, 2, 3]
        """

        # Initialise a list to store (score, popularity, item_ID)
        # tuples that track item scores:
        scores = []

        # Calcuate and store the item scores and popularity:
        for item in [i for i in self.items if i not in query_ids]:
            score = sum([self.similarity(i, item) for i in query_ids])
            scores.append((score, self.popularity(item), item))

        # Return the n most similar IDs:
        return [x[-1] for x in sorted(scores, reverse=True)[:limit]]

    def similarity(self, a, b):
        """Calculate the cosine similarity between the preference vectors for
        items a and b. Each item's preference vector is a binary vector of
        dimension N where N is the total number of users. The element(i) in the
        vector is either 0 or 1 depending on whether user(i) has expressed
        preference for this item.

        For example, when user_prefs = [{1, 2}, {2, 3}, {3, 4}], the preference
        vector for item 2 is: (1, 1, 0).

        The theoretical definition of cosine_similarity for two vectors is
        stated here: https://en.wikipedia.org/wiki/Cosine_similarity#Definition

        However, as our vectors are binary, we can avoid transforming the
        user_prefs into ratings vectors and the calculation is simplified as
        follows:

        sim(a, b) = count(users like a AND b) /
                (sqrt(count(users like a)) * sqrt(count(users like b)))

        Args:
            a: An integer in self.items
            b: An integer in self.items

        Returns:
            A float representing the similarity of item a and b.
        """
        numerator = len([s for s in self.user_prefs if {a, b} <= s])
        denominator = math.sqrt(len([s for s in self.user_prefs if a in s])) * \
                      math.sqrt(len([s for s in self.user_prefs if b in s]))

        try:
            return numerator / denominator
        except ZeroDivisionError:
            # Cosine similarity is undefined if either of the operands is a zero
            # vector. This might happen if no user has expressed a preference
            # for a particular ID. In that case, just revert to zero.
            return 0.0

    def popularity(self, item_id):
        """Calculate the item popularity: the count of users that have expressed
        preference for this product id.

        Args:
            item_id: An integer in self.items

        Returns
            An integer representing the item's popularity.
        """
        return len([s for s in self.user_prefs if item_id in s])
