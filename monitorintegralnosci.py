import os
import hashlib
import json


def calculate_hash(filepath):
    # funkcja liczy hash pliku, zeby potem mozna bylo sprawdzic czy ktos go nie zmienil
    sha256 = hashlib.sha256()
    try:
        # czytam plik
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None


def create_baseline(directory, baseline_file):
    # zapisujemy sobie jak wygladaja pliki na ten moment
    baseline = {}
    print(f"skanowanie folderu: {directory}...")

    # petla zeby przejsc przez wszystkie pliki w folderze
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            if file_hash:
                baseline[filepath] = file_hash

    # zapisujemy wyniki do pliku json
    with open(baseline_file, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=4)
    print(f"zapisano dane dla {len(baseline)} plikow.")


def check_integrity(directory, baseline_file):
    # sprawdza czy pliki sie zgadzaja z tym co zapisalismy wczesniej
    if not os.path.exists(baseline_file):
        print("blad: nie ma pliku z danymi. najpierw zrob skanowanie (opcja 1).")
        return

    with open(baseline_file, 'r', encoding='utf-8') as f:
        baseline = json.load(f)

    current_files = set()
    alerts = 0
    print("\n--- sprawdzanie plikow ---")

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            current_files.add(filepath)

            current_hash = calculate_hash(filepath)

            # sprawdzanie co konkretnie sie zmienilo
            if filepath not in baseline:
                print(f"[nowy plik] ktos dodal: {filepath}")
                alerts += 1
            elif current_hash != baseline[filepath]:
                print(f"[zmiana] plik zmieniony: {filepath} (inny hash!)")
                alerts += 1

    # sprawdzenie czy czegos nie brakuje
    for filepath in baseline:
        if filepath not in current_files:
            print(f"[usuniete] brakuje pliku: {filepath}")
            alerts += 1

    if alerts == 0:
        print("zero zmian.")
    else:
        print(f"uwaga: znaleziono {alerts} problemow!")


def main():
    # wpisujemy sciezke na sztywno, literka 'r' przed cudzyslowem jest wazna dla sciezekek w windowsie
    directory = "testowe"
    db_file = "hash_db.json"

    # sprawdza czy taki folder w ogole istnieje
    if not os.path.isdir(directory):
        print(f"blad: folder {directory} nie istnieje. utworz go najpierw!")
        return

    # proste menu dla uzytkownika
    print("co chcesz zrobic?")
    print("1 - skanuj i zapisz stan plikow")
    print("2 - sprawdz czy pliki sie zmienily")
    wybor = input("wybierz (1/2): ")

    if wybor == '1':
        create_baseline(directory, db_file)
    elif wybor == '2':
        check_integrity(directory, db_file)
    else:
        print("blad: zly wybor. odpal program jeszcze raz i wpisz 1 lub 2.")


if __name__ == "__main__":
    main()