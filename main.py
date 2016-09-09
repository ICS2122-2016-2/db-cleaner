import os

__author__ = "rpalmaotero"

N_POSICIONES = 12750
DB_PATH      = os.path.join(os.path.dirname(__file__), "./retail.dat")


class DatabaseCleaner:
    def __init__(self):
        self.ranking = {}
        self.target_skus = []

        self.get_top_skus()
        self.clean_db()

    def get_top_skus(self):
        with open(DB_PATH) as db_file:
            for receipt_line in db_file:
                skus = receipt_line.strip().split(" ")
                for sku in skus:
                    if sku not in self.ranking:
                        self.ranking[sku] = 1
                    else:
                        self.ranking[sku] += 1

        sorted_ranking = sorted(
            self.ranking.items(),
            key=lambda item: item[1],
            reverse=True
        )
        self.target_skus = list(map(
            lambda item: item[0],
            sorted_ranking[:N_POSICIONES]
        ))

    def clean_db(self):
        cleaned_lines = []
        with open(DB_PATH) as db_file:
            for dirty_line in db_file:
                cleaned_skus = list(filter(
                    lambda sku: sku in self.target_skus,
                    dirty_line.strip().split(" ")
                ))
                if len(cleaned_skus) > 0:
                    cleaned_lines.append(" ".join(cleaned_skus))

        cleaned_db_contents = "\n".join(cleaned_lines)
        with open("./cleaned_db.dat", "w") as cleaned_db_file:
            cleaned_db_file.write(cleaned_db_contents)

if __name__ == "__main__":
    DatabaseCleaner()


