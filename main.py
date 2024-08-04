class Logger:
    def __init__(self):
        self.messages = {}
        self.max_length = 100
        self.time_threshold = 10

    def shouldPrintMessage(self, timestamp, message):
        self._clean_old_messages(timestamp)

        if message in self.messages and timestamp < self.messages[message]:
            return False

        self.messages[message] = timestamp + self.time_threshold
        return True

    def clean(self, timestamp):
        if len(self.messages) == 0:
            return False

        # Удаляем сообщения, которые уже устарели к данному timestamp
        self._clean_old_messages(timestamp)

        # Если нет сообщений, которые могут быть напечатаны в этот момент, возвращаем True
        if all(ts > timestamp for ts in self.messages.values()):
            self.messages.clear()
            return True

        return False

    def loggerSize(self):
        return len(self.messages)

    def _clean_old_messages(self, current_timestamp):
        # Удаляем все сообщения, которые устарели на данный момент
        self.messages = {msg: ts for msg, ts in self.messages.items() if ts > current_timestamp}


def print_help():
    print("Команды:")
    print("  add <timestamp> <message>  - Добавить сообщение с меткой времени")
    print("  clean <timestamp>          - Очистить лог")
    print("  size                       - Показать размер лога")
    print("  help                       - Показать это сообщение")
    print("  exit                       - Выйти из программы")


def main():
    logger = Logger()
    print("Система логирования запущена. Введите 'help' для получения списка команд.")

    while True:
        command = input("> ").strip()
        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command.startswith("add "):
            try:
                parts = command.split(maxsplit=2)
                timestamp = int(parts[1])
                message = parts[2]
                if logger.shouldPrintMessage(timestamp, message):
                    print(f"Сообщение '{message}' добавлено.")
                else:
                    print(f"Сообщение '{message}' не может быть добавлено.")
            except (IndexError, ValueError):
                print("Неправильный формат команды. Используйте: add <timestamp> <message>")
        elif command.startswith("clean "):
            try:
                parts = command.split()
                timestamp = int(parts[1])
                if logger.clean(timestamp):
                    print("Система очищена.")
                else:
                    print("Систему не удалось очистить.")
            except (IndexError, ValueError):
                print("Неправильный формат команды. Используйте: clean <timestamp>")
        elif command == "size":
            print(f"Размер лога: {logger.loggerSize()}")
        else:
            print("Неизвестная команда. Введите 'help' для получения списка команд.")


if __name__ == "__main__":
    main()