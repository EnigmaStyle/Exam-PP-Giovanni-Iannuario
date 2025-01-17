import os 
from movie_library import MovieLibrary #Importa la classe MovieLibrary dal modulo movie_library

def main():
    # File json
    json_file = 'movies (1).json'  
    json_path = os.path.abspath(json_file)

    # Verifica se il file esiste
    if not os.path.isfile(json_path):
        print(f"Il file '{json_file}' non esiste nel percorso specificato.")
        return

    # Inizializza la libreria con il file JSON
    try:
        library = MovieLibrary(json_path)
        print("Libreria caricata con successo.")
    except FileNotFoundError:
        print(f"File '{json_file}' non trovato.")
        return
    except ValueError as ve:
        print(f"Errore nel file JSON: {ve}")
        return
    except Exception as e:
        print(f"Errore inaspettato: {e}")
        return

    while True:
        # Menù opzioni aggiornato
        print("\n--- Menù ---")
        print("1. Visualizza tutti i film")
        print("2. Aggiungi un nuovo film")
        print("3. Rimuovi un film")
        print("4. Aggiorna un film")
        print("5. Visualizza tutti i titoli dei film")
        print("6. Conta il numero totale di film")
        print("7. Visualizza il film per titolo")
        print("8. Cerca il film per sottostringa nel titolo")
        print("9. Cerca il film per anno")
        print("10. Conta il film per regista")
        print("11. Cerca il film per genere")
        print("12. Visualizza il film più vecchio")
        print("13. Calcola la media degli anni di uscita")
        print("14. Visualizza il titolo più lungo")
        print("15. Visualizza titoli tra inizio anno e fine anno")
        print("16. Visualizza l'anno che si ripete")
        print("0. Esci")

        # Richiesta opzione
        choice = input("Scegli un'opzione: ").strip()

        if choice == '1':
            # Visualizza tutti i film
            movies = library.get_movies()
            if not movies:
                print("Nessun film nella libreria.")
            else:
                print("\n--- Tutti i Film ---")
                for idx, movie in enumerate(movies, start=1):
                    genres = ', '.join(movie['genres'])
                    print(f"{idx}. Titolo: {movie['title']}, Regista: {movie['director']}, Anno: {movie['year']}, Generi: {genres}")

        elif choice == '2':
            # Aggiungi un nuovo film
            title = input("Inserisci il titolo del film: ").strip()
            director = input("Inserisci il regista del film: ").strip()
            year_input = input("Inserisci l'anno di uscita del film: ").strip()
            genres_input = input("Inserisci i generi del film (separati da virgole): ").strip()

            # Verifica che l'anno sia un numero
            if not year_input.isdigit():
                print("L'anno deve essere un numero intero.")
                continue
            year = int(year_input)

            # Crea una lista di generi
            genres = [genre.strip() for genre in genres_input.split(',') if genre.strip()]
            if not genres:
                print("Devi inserire almeno un genere.")
                continue

            try:
                # Aggiungi il film alla libreria
                library.add_movie(title, director, year, genres)
                print(f"Film '{title}' aggiunto con successo.")
            except ValueError as ve:
                print(ve)
            except TypeError as te:
                print(te)

        elif choice == '3':
            # Rimuovi un film
            title = input("Inserisci il titolo del film da rimuovere: ").strip()
            try:
                removed_movie = library.remove_movie(title)
                print(f"Film '{removed_movie['title']}' rimosso con successo.")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)

        elif choice == '4':
            # Aggiorna un film
            title = input("Inserisci il titolo del film da aggiornare: ").strip()
            print("Lascia vuoto se non vuoi aggiornare un campo.")
            director = input("Nuovo regista: ").strip()
            year_input = input("Nuovo anno: ").strip()
            genres_input = input("Nuovi generi (separati da virgole): ").strip()

            # Elaborazione dei parametri
            director = director if director else None
            year = int(year_input) if year_input.isdigit() else None
            genres = [genre.strip() for genre in genres_input.split(',') if genre.strip()] if genres_input else None

            try:
                updated_movie = library.update_movie(title, director, year, genres)
                print(f"Film '{updated_movie['title']}' aggiornato con successo.")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)
            except TypeError as te:
                print(te)

        elif choice == '5':
            # Visualizza tutti i titoli dei film
            titles = library.get_movie_titles()
            if not titles:
                print("Nessun titolo nella libreria.")
            else:
                print("\n--- Titoli dei Film ---")
                for idx, title in enumerate(titles, start=1):
                    print(f"{idx}. {title}")

        elif choice == '6':
            # Conta il numero totale di film
            count = library.count_movies()
            print(f"Numero totale di film nella libreria: {count}")

        elif choice == '7':
            # Visualizza un film per titolo
            title = input("Inserisci il titolo del film da cercare: ").strip()
            try:
                movie = library.get_movie_by_title(title)
                genres = ', '.join(movie['genres'])
                print(f"\n--- Dettagli del Film ---")
                print(f"Titolo: {movie['title']}")
                print(f"Regista: {movie['director']}")
                print(f"Anno: {movie['year']}")
                print(f"Generi: {genres}")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)

        elif choice == '8':
            # Cerca film per sottostringa nel titolo
            substring = input("Inserisci la sottostringa da cercare nel titolo: ").strip()
            try:
                matched_movies = library.get_movies_by_title_substring(substring)
                print(f"\n--- Film contenenti '{substring}' nel titolo ---")
                for idx, movie in enumerate(matched_movies, start=1):
                    genres = ', '.join(movie['genres'])
                    print(f"{idx}. Titolo: {movie['title']}, Regista: {movie['director']}, Anno: {movie['year']}, Generi: {genres}")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)

        elif choice == '9':
            # Cerca film per anno
            year_input = input("Inserisci l'anno da cercare: ").strip()
            if not year_input.isdigit():
                print("L'anno deve essere un numero intero.")
                continue
            year = int(year_input)
            try:
                matched_movies = library.get_movies_by_year(year)
                print(f"\n--- Film del {year} ---")
                for idx, movie in enumerate(matched_movies, start=1):
                    genres = ', '.join(movie['genres'])
                    print(f"{idx}. Titolo: {movie['title']}, Regista: {movie['director']}, Generi: {genres}")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)
            except TypeError as te:
                print(te)

        elif choice == '10':
            # Conta film per regista
            director = input("Inserisci il nome del regista: ").strip()
            if not director:
                print("Devi inserire un nome di regista.")
                continue
            try:
                count = library.count_movies_by_director(director)
                print(f"Numero di film diretti da '{director}': {count}")
            except TypeError as te:
                print(te)

        elif choice == '11':
            # Cerca film per genere
            genre = input("Inserisci il genere da cercare: ").strip()
            if not genre:
                print("Devi inserire un genere.")
                continue
            try:
                matched_movies = library.get_movies_by_genre(genre)
                print(f"\n--- Film del genere '{genre}' ---")
                for idx, movie in enumerate(matched_movies, start=1):
                    genres = ', '.join(movie['genres'])
                    print(f"{idx}. Titolo: {movie['title']}, Regista: {movie['director']}, Anno: {movie['year']}, Generi: {genres}")
            except MovieLibrary.MovieNotFoundError as e:
                print(e)
            except TypeError as te:
                print(te)

        elif choice == '12':
            # Visualizza il film più vecchio
            oldest_title = library.get_oldest_movie_title()
            if oldest_title:
                print(f"Il film più vecchio nella libreria è: '{oldest_title}'")
            else:
                print("La libreria è vuota.")

        elif choice == '13':
            # Calcola la media degli anni di uscita
            average_year = library.get_average_release_year()
            if average_year > 0:
                print(f"La media degli anni di pubblicazione dei film è: {average_year:.2f}")
            else:
                print("La libreria è vuota.")

        elif choice == '14':
            # Visualizza il titolo più lungo
            longest_title = library.get_longest_title()
            if longest_title:
                print(f"Il titolo più lungo nella libreria è: '{longest_title}'")
            else:
                print("La libreria è vuota.")

        elif choice == '15':
            # Visualizza titoli tra due anni
            start_year_input = input("Inserisci l'anno di inizio: ").strip()
            end_year_input = input("Inserisci l'anno di fine: ").strip()
            if not (start_year_input.isdigit() and end_year_input.isdigit()):
                print("Gli anni devono essere numeri interi!")
                continue
            start_year = int(start_year_input)
            end_year = int(end_year_input)
            try:
                titles_in_range = library.get_titles_between_years(start_year, end_year)
                if titles_in_range:
                    print(f"\n--- Titoli di film pubblicati tra {start_year} e {end_year} ---")
                    for idx, title in enumerate(titles_in_range, start=1):
                        print(f"{idx}. {title}")
                else:
                    print(f"Nessun film trovato tra {start_year} e {end_year}.")
            except TypeError as te:
                print(te)

        elif choice == '16':
            # Visualizza l'anno più comune
            most_common_year = library.get_most_common_year()
            if most_common_year:
                print(f"L'anno più comune tra i film della libreria è: {most_common_year}")
            else:
                print("La libreria è vuota.")

        elif choice == '0':
            # Esci dal programma
            print("Arrivederci!")
            break

        else:
            print("Scelta non valida! Per favore, seleziona un'opzione dal menu!")

if __name__ == "__main__":
    main()