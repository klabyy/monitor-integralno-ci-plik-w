# Monitor integralności plików
Prosty skrypt w Pythonie, który sprawdza, czy nie zaszła w pliku zmiana.

## Jak działa program?
* **Opcja 1** - Program sprawdza pliki w folderze i oblicza hash, zapisując go do pliku.
* **Opcja 2** - Program porównuje nowy hash z tym zapisanym wcześniej. Jeśli jest on inny, to oznacza zmianę (inny plik, brak pliku, modyfikacja tekstu), wyświetlając ostrzeżenie w konsoli.
