"""Projektbeschreibung: SmartStorage – Lagerverwaltungssystem

1. Projektübersicht
Projekt SmartStorage ist eine Python-Anwendung zur effizienten Verwaltung von Warenbeständen. Es ermöglicht Unternehmen oder Einzelhändlern, ihre Produkte digital zu erfassen, Bestände zu kontrollieren und Verkäufe in Echtzeit zu verbuchen. Die Daten werden dauerhaft gespeichert, sodass keine Informationen beim Beenden des Programms verloren gehen.

2. Die Architektur (Klassenstruktur)
System ist nach dem Prinzip der objektorientierten Programmierung (OOP) aufgebaut:
Klasse Product: Dies ist der digitale "Steckbrief" für jeden Artikel. Er speichert den Namen, den Einzelpreis, die verfügbare Menge und die Kategorie. Zudem verfügt die Klasse über Methoden, um sich selbst in ein speicherbares Format zu übersetzen.
Klasse Warehouse: Diese Klasse fungiert als das "Gehirn" des Lagers. Sie verwaltet die Liste aller Produkte und enthält die Logik für das Hinzufügen von Beständen, das Speichern der Daten und das Abwickeln von Transaktionen.

3. Zentrale Funktionen
System bietet vier Hauptfunktionen:
Inventarliste (list_all): Eine übersichtliche Darstellung aller gelagerten Artikel inklusive ihrer Kategorie, ihres Preises und des aktuellen Bestands.
Bestandsmanagement (add_product): Neue Produkte können ins System aufgenommen werden. Falls ein Produkt bereits existiert, erkennt das System dies automatisch und erhöht lediglich die vorhandene Menge.
Verkaufsabwicklung (sell_product): Beim Verkauf wird geprüft, ob genügend Ware auf Lager ist. Ist dies der Fall, wird der Bestand reduziert und der erzielte Umsatz sofort berechnet und angezeigt.
Datenpersistenz: Durch die Anbindung an eine JSON-Datenbank (inventory.json) wird jeder Vorgang sofort sicher auf der Festplatte gespeichert.

4. Besonderheiten der Programmierlogik
Fehlertoleranz: Bei Verkäufen wird strikt geprüft, ob die angeforderte Menge überhaupt vorhanden ist. Ein "negativer Lagerbestand" wird so verhindert.
Benutzerfreundlichkeit: Die Eingabe von Produktnamen ignoriert Groß- und Kleinschreibung (Case-Insensitive), was die Suche nach Artikeln im Alltag erleichtert.
Automatisierung: Beim Starten der Anwendung werden alle Daten aus der letzten Sitzung automatisch geladen, sodass nahtloses Arbeiten möglich ist.

5. Technische Highlights
Sprache: Python 3

Datenformat: JSON (für einfachen Datenaustausch und Lesbarkeit)

Konzept: CRUD (Create, Read, Update) Operationen für die Bestandsführung."""

import json
import os


class Product:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Product(**data)


class Warehouse:
    def __init__(self, file_name="inventory.json"):
        self.file_name = file_name
        self.products = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data]

    def save_data(self):
        with open(self.file_name, "w") as f:
            json.dump([p.to_dict() for p in self.products], f, indent=4)

    def add_product(self, name, price, quantity, category):
        # Prüfen, ob Produkt schon existiert
        for p in self.products:
            if p.name.lower() == name.lower():
                p.quantity += quantity
                self.save_data()
                print(f"Menge für {name} aktualisiert.")
                return

        new_product = Product(name, price, quantity, category)
        self.products.append(new_product)
        self.save_data()
        print(f"Produkt {name} neu angelegt.")

    def list_all(self):
        print("\n--- AKTUELLER LAGERBESTAND ---")
        for p in self.products:
            print(f"[{p.category}] {p.name}: {p.price}€ | Menge: {p.quantity}")

    def sell_product(self, name, amount):
        for p in self.products:
            if p.name.lower() == name.lower():
                if p.quantity >= amount:
                    p.quantity -= amount
                    self.save_data()
                    print(f"{amount}x {name} verkauft. Umsatz: {amount * p.price}€")
                    return
                else:
                    print("Nicht genug Bestand!")
                    return
        print("Produkt nicht gefunden.")


def main():
    store = Warehouse()

    while True:
        print("\n1. Bestand zeigen | 2. Produkt hinzufügen | 3. Verkauf buchen | 4. Ende")
        choice = input("Wähle: ")

        if choice == "1":
            store.list_all()
        elif choice == "2":
            n = input("Name: ")
            p = float(input("Preis: "))
            q = int(input("Menge: "))
            c = input("Kategorie: ")
            store.add_product(n, p, q, c)
        elif choice == "3":
            n = input("Was wurde verkauft? ")
            q = int(input("Wie viele? "))
            store.sell_product(n, q)
        elif choice == "4":
            break


if __name__ == "__main__":
    main()