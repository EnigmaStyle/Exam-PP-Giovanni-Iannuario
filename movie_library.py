import os # Importazione del modulo os per la gestione dei file
import json # Importazione del modulo json per la gestione dei file JSON

# Creazione della classe MovieLibrary
class MovieLibrary:
    
    # 18. Creazione della classe MovieNotFoundError con eccezione per film non trovato
    class MovieNotFoundError(Exception):
        pass

    # 17. Costruttore che solleva FileNotFoundError se il file json non esiste
    def __init__(self, json_file):
        self.json_file = json_file

        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File not found: {self.json_file}")

        with open(json_file, 'r', encoding="utf-8") as f:
            try:
                self.movies = json.load(f)
                if not isinstance(self.movies, list):
                    raise ValueError("Il file JSON deve contenere una lista di film!")
            except json.JSONDecodeError as e:
                raise ValueError(f"Errore nel file JSON: {e}")

    # Metodo __update_json_file privato per aggiornare il file json
    def __update_json_file(self):
        with open(self.json_file, 'w', encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4)

    # 1. Metodo get_movies che restituisce l’intera collezione di film
    def get_movies(self):
        return self.movies

    # 2. Metodo add_movie che aggiunge un nuovo film alla collezione e aggiorna il file json
    def add_movie(self, title, director, year, genres):
        # Verifica che i parametri siano del tipo corretto
        if not isinstance(title, str):
            raise TypeError("Il parametro 'title' deve essere una stringa!")
        if not isinstance(director, str):
            raise TypeError("Il parametro 'director' deve essere una stringa!")
        if not isinstance(year, int):
            raise TypeError("Il parametro 'year' deve essere un numero intero!")
        if not isinstance(genres, list) or not all(isinstance(genre, str) for genre in genres):
            raise TypeError("Il parametro 'genres' deve essere una lista di stringhe!")

        # Controlla se il film esiste già nella collezione
        for movie in self.movies:
            if movie['title'].lower() == title.lower() and movie['year'] == year:
                raise ValueError(f"Il film '{title}' del {year} esiste già!")

        # Crea un dizionario per il nuovo film
        new_movie = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }

        # Aggiunge il nuovo film alla lista dei film
        self.movies.append(new_movie)

        # Aggiorna il file json con la nuova lista di film
        self.__update_json_file()

    # 3. Metodo remove_movie che rimuove un film dalla collezione
    def remove_movie(self, title):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                self.movies.remove(movie)
                self.__update_json_file()
                return movie
        # Solleva l'eccezione dichiarata all'inizio se il film non viene trovato
        raise self.MovieNotFoundError("il film non è stato trovato")

    # 4. Metodo update_movie che modifica i dettagli di un film
    def update_movie(self, title, director=None, year=None, genres=None):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                # Aggiorna i campi se i parametri non sono None
                if director is not None:
                    if not isinstance(director, str):
                        raise TypeError("'director' deve essere una stringa!")
                    movie["director"] = director
                if year is not None:
                    if not isinstance(year, int):
                        raise TypeError("'year' deve essere un numero intero!")
                    movie["year"] = year
                if genres is not None:
                    if not isinstance(genres, list) or not all(isinstance(genre, str) for genre in genres):
                        raise TypeError("'genres' deve essere una lista di stringhe!")
                    movie["genres"] = genres
                # Aggiorna il file JSON dopo le modifiche
                self.__update_json_file()
                return movie
        # Solleva l'eccezione personalizzata se il film non viene trovato
        raise self.MovieNotFoundError("il film non è stato trovato")

    # 5. Metodo get_movie_titles che restituisce una lista di tutti i titoli dei film
    def get_movie_titles(self):
        return [movie["title"] for movie in self.movies]

    # 6. Metodo count_movies che restituisce il numero totale dei film nella collezione
    def count_movies(self):
        return len(self.movies)

    # 7. Metodo get_movie_by_title che restituisce un film in base al titolo
    def get_movie_by_title(self, title):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                return movie
        # Solleva l'eccezione personalizzata se il film non viene trovato
        raise self.MovieNotFoundError("Il film che stai cercando non è stato trovato")

    # 8. Metodo get_movies_by_title_substring che restituisce una lista di film basati su una sottostringa del titolo (case sensitive)
    def get_movies_by_title_substring(self, substring):
        matched_movies = [movie for movie in self.movies if substring in movie["title"]]
        if not matched_movies:
            raise self.MovieNotFoundError(f"No movies found containing the substring: '{substring}'")
        return matched_movies

    # 9. Metodo get_movies_by_year che restituisce una lista di film in base all'anno
    def get_movies_by_year(self, year):
        if not isinstance(year, int):
            raise TypeError("'year' deve essere un numero intero!")
        matched_movies = [movie for movie in self.movies if movie["year"] == year]
        if not matched_movies:
            raise self.MovieNotFoundError(f"Nessun film trovato per anno!: {year}")
        return matched_movies

    # 10. Metodo count_movies_by_director che conta quanti film di un regista sono presenti nella collezione (non case sensitive)
    def count_movies_by_director(self, director):
        if not isinstance(director, str):
            raise TypeError("Il parametro 'director' deve essere una stringa!")
        count = sum(1 for movie in self.movies if movie["director"].lower() == director.lower())
        return count

    # 11. Metodo get_movies_by_genre che restituisce una lista di film in base al genere (non case sensitive)
    def get_movies_by_genre(self, genre):
        if not isinstance(genre, str):
            raise TypeError("Il parametro 'genre' deve essere una stringa!")
        matched_movies = [
            movie for movie in self.movies
            if any(g.lower() == genre.lower() for g in movie.get("genres", []))
        ]
        if not matched_movies:
            raise self.MovieNotFoundError(f"Nessun film trovato per questo genere!: '{genre}'")
        return matched_movies

    # 12. Metodo get_oldest_movie_title che restituisce il titolo del film più vecchio
    def get_oldest_movie_title(self):
        if not self.movies:
            return None
        oldest_movie = min(self.movies, key=lambda m: m["year"])
        return oldest_movie["title"]

    # 13. Metodo get_average_release_year che restituisce la media degli anni di pubblicazione dei film
    def get_average_release_year(self):
        if not self.movies:
            return 0.0
        total_years = sum(movie["year"] for movie in self.movies)
        average = total_years / len(self.movies)
        return average

    # 14. Metodo get_longest_title che restituisce il titolo più lungo
    def get_longest_title(self):
        if not self.movies:
            return None
        longest_title_movie = max(self.movies, key=lambda m: len(m["title"]))
        return longest_title_movie["title"]
      
    # 15. Metodo get_titles_between_years che restituisce una lista di titoli di film pubblicati tra start_year e end_year (estremi inclusi)
    def get_titles_between_years(self, start_year, end_year):
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            raise TypeError("'start_year' e 'end_year' devono essere numeri interi!")
        titles_in_range = [
            movie["title"] for movie in self.movies
            if start_year <= movie["year"] <= end_year
        ]
        return titles_in_range
    
    # 16. Metodo get_most_common_year che restituisce l'anno che si ripete spesso tra i film
    def get_most_common_year(self):
        if not self.movies:
            return None
        year_frequency = {}
        for movie in self.movies:
            year = movie["year"]
            year_frequency[year] = year_frequency.get(year, 0) + 1
        # Trova l'anno che si ripete spesso
        most_common_year = max(year_frequency, key=year_frequency.get)
        return most_common_year