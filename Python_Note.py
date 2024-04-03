import json
import datetime
import argparse

def add_note(title, message):
    notes = load_notes()
    note_id = len(notes) + 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_note = {"id": note_id, "title": title, "message": message, "timestamp": timestamp}
    notes.append(new_note)
    save_notes(notes)
    print("Заметка успешно сохранена")

def load_notes():
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []
    return notes

def save_notes(notes):
    with open('notes.json', 'w') as file:
        json.dump(notes, file)

def read_notes(date_filter=None):
    notes = load_notes()
    if date_filter:
        filtered_notes = [note for note in notes if note["timestamp"].split()[0] == date_filter]
        return filtered_notes
    return notes

def delete_note(note_id):
    notes = load_notes()
    notes = [note for note in notes if note["id"] != note_id]
    save_notes(notes)
    print("Заметка успешно удалена")

def edit_note(note_id, title, message):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["message"] = message
            note["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print("Заметка успешно отредактирована")
            return
    print("Заметка с таким id не найдена")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Управление заметками')
    parser.add_argument('command', type=str, help='Команда (add, read, delete, edit)')
    parser.add_argument('--title', type=str, help='Заголовок заметки')
    parser.add_argument('--msg', type=str, help='Тело заметки')
    parser.add_argument('--id', type=int, help='Идентификатор заметки')
    parser.add_argument('--date', type=str, help='Дата для фильтрации при чтении заметок')

    args = parser.parse_args()

    if args.command == 'add' and args.title and args.msg:
        add_note(args.title, args.msg)
    elif args.command == 'read':
        notes = read_notes(args.date)
        print("Список заметок:")
        for note in notes:
            print(f"{note['id']}. {note['title']} - {note['message']} ({note['timestamp']})")
    elif args.command == 'delete' and args.id:
        delete_note(args.id)
    elif args.command == 'edit' and args.id and args.title and args.msg:
        edit_note(args.id, args.title, args.msg)
    else:
        print("Неверная команда или недостаточно параметров")

