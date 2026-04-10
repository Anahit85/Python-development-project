# 🧠 1. Library Management System (OOP + File + Logic)
# 📌 Projektarbeit: Entwicklung eines digitalen Bibliotheksmanagements
# Zielsetzung
# Entwickeln Sie ein konsolenbasiertes Verwaltungssystem für eine Bibliothek unter Verwendung von Python. Das Ziel ist es, Bücher und Nutzer effizient zu verwalten und alle Daten dauerhaft in einer Datei zu speichern.
# 1. Struktur des Datenmodells (Klassen)
# Das System soll auf drei zentralen Klassen basieren:
# Klasse Book: Enthält die Eigenschaften Titel, Autor, Erscheinungsjahr und den Status is_available (Verfügbarkeit).
# Klasse User: Verwaltet den Namen des Nutzers und eine Liste der aktuell ausgeliehenen Bücher (borrowed_books).
# Klasse Library: Fungiert als Hauptinstanz und verwaltet zwei Listen: eine für alle Bücher und eine für alle registrierten Nutzer.
#
# 2. Funktionale Anforderungen
# Das Programm muss folgende Kernfunktionen unterstützen:
# Buchverwaltung: Neue Bücher zum Bestand hinzufügen.
# Nutzerverwaltung: Neue Nutzer im System registrieren.
# Leihvorgang: Einem Nutzer ermöglichen, ein Buch auszuleihen.
# Rückgabe: Ein Buch wieder für andere Nutzer freigeben.
# Inventur: Eine Übersicht aller aktuell verfügbaren Bücher anzeigen.
#
# 3. Logik und Validierung (Die "Herausforderungen")
# Um einen realistischen Ablauf zu gewährleisten, müssen folgende Regeln programmiert werden:
# Verfügbarkeitsprüfung: Ein Buch kann nicht ausgeliehen werden, wenn es bereits als "nicht verfügbar" markiert ist.
# Ausleihlimit: Ein einzelner Nutzer darf maximal 3 Bücher gleichzeitig in seinem Besitz haben.
# Zustandsverwaltung: Der Status eines Buches (is_available) muss sich bei jedem Leih- und Rückgabevorgang automatisch ändern.
#
# 4. Datenpersistenz
# Damit die Daten nach dem Schließen des Programms nicht verloren gehen, ist eine Anbindung an das JSON-Dateiformat erforderlich:
# Verwenden Sie das Python-Modul json.
# Speichern Sie den gesamten Zustand der Bibliothek beim Beenden oder nach jeder Änderung in einer Datei ab.
# Laden Sie die Daten beim Starten des Programms automatisch aus der Datei.


import json
import os


# 1. DAS BUCH: Legt fest, welche informaton ein Buch hat
class Book:
    def __init__(self, title, author, year, is_available=True):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = is_available  # Ist das Buch gerade da? (Standard: Ja)

    # Macht aus dem Buch-Objekt einen Text (Dictionary), damit man es speichern kann
    def to_json(self):
        return self.__dict__

    # Erstellt aus gespeicherten Daten wieder ein echtes Buch-Objekt
    @staticmethod
    def from_json(data):
        return Book(**data)


# 2. DER NUTZER: Wer leiht hier was aus?
class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []  # Liste der Titel, die der Nutzer gerade hat

    def to_json(self):
        return {
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }

    @staticmethod
    def from_json(data):
        user = User(data["name"])
        user.borrowed_books = data["borrowed_books"]
        return user


# 3. DIE BIBLIOTHEK: Die Zentrale, die alles verwaltet
class Library:
    def __init__(self, file_name="library.json"):
        self.file_name = file_name
        self.books = []  # Hier landen alle Bücher
        self.users = []  # Hier landen alle Nutzer
        self.load()  # Beim Start sofort alte Daten laden

    # DATEIEN LADEN: Schaut in die JSON-Datei
    def load(self):
        if not os.path.exists(self.file_name):
            return "Datei existiert nicht"
        with open(self.file_name, "r") as f:
            data = json.load(f)
        # Verwandelt den Text aus der Datei wieder in Buch- und Nutzer-Objekte
        self.books = [Book.from_json(book) for book in data.get("books", [])]
        self.users = [User.from_json(user) for user in data.get("users", [])]

    # DATEIEN SPEICHERN: Schreibt alles in die JSON-Datei
    def save(self):
        data = {
            "books": [book.to_json() for book in self.books],
            "users": [user.to_json() for user in self.users]
        }
        with open(self.file_name, "w") as f:
            json.dump(data, f)

    # NEUES BUCH hinzufügen
    def add_book(self, title, author, year):
        self.books.append(Book(title, author, year))
        self.save()  # Sofort speichern
        print("Buch hinzugefügt")

    # ALLE BÜCHER zeigen
    def show_books(self):
        for i, book in enumerate(self.books, 1):
            status = "Verfügbar" if book.is_available else "Ausgeliehen"
            print(f"{i}. {book.title} - {book.author} ({book.year}) - {status}")

    # NEUEN NUTZER anmelden
    def add_user(self, name):
        self.users.append(User(name))
        self.save()
        print("Nutzer hinzugefügt")

    # HELFER: Nutzer in der Liste finden
    def find_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

    # HELFER: Buch in der Liste finden
    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    # AUSLEIHEN: Die wichtigste Logik
    def borrow_book(self, user_name, book_title):
        book = self.find_book(book_title)
        user = self.find_user(user_name)

        # Prüfungen: Gibt es alles? Ist es frei? Hat der Nutzer zu viele?
        if not user:
            print("Nutzer nicht gefunden")
            return
        if not book:
            print("Buch nicht gefunden")
            return
        if not book.is_available:
            print("Buch ist bereits verliehen")
            return
        if len(user.borrowed_books) >= 3:
            print("Limit erreicht! (Max. 3 Bücher)")
            return

        # Wenn alles ok: Buch auf "belegt" setzen und dem Nutzer geben
        book.is_available = False
        user.borrowed_books.append(book_title)
        self.save()
        print("Erfolgreich ausgeliehen!")

    # ZURÜCKGEBEN
    def return_book(self, user_name, book_title):
        book = self.find_book(book_title)
        user = self.find_user(user_name)

        if not user or not book:
            print("Fehler bei Nutzer oder Buch")
            return
        if book.title not in user.borrowed_books:
            print("Nutzer hat dieses Buch gar nicht")
            return

        # Status wieder zurücksetzen
        book.is_available = True
        user.borrowed_books.remove(book_title)
        self.save()
        print("Erfolgreich zurückgegeben!")


# DAS HAUPTMENÜ: Was der Mensch vor dem Bildschirm sieht
def main():
    library = Library()
    while True:
        print("\n--- Bibliothek Menü ---")
        print("1. Buch hinzufügen | 2. Nutzer hinzufügen | 3. Bücher zeigen")
        print("4. Ausleihen | 5. Zurückgeben | 6. Beenden")

        choice = input("\nAuswahl (1-6): ")
        if choice == "1":
            t = input("Titel: ");
            a = input("Autor: ");
            y = input("Jahr: ")
            library.add_book(t, a, y)
        elif choice == "2":
            n = input("Name: ")
            library.add_user(n)
        elif choice == "3":
            library.show_books()
        elif choice == "4":
            n = input("Nutzername: ");
            t = input("Buchtitel: ")
            library.borrow_book(n, t)
        elif choice == "5":
            n = input("Nutzername: ");
            t = input("Buchtitel: ")
            library.return_book(n, t)
        elif choice == "6":
            break
        else:
            print("Ungültige Eingabe")


if __name__ == "__main__":
    main()