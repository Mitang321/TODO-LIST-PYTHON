import json


class Task:
    def __init__(self, title, description="", deadline="", category=""):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.category = category

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'category': self.category
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description, deadline, category):
        task = Task(title, description, deadline, category)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        for idx, task in enumerate(self.tasks):
            print(
                f"{idx + 1}. {task.title} - {task.description} (Deadline: {task.deadline}, Category: {task.category})")

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
                self.tasks = [Task(**task) for task in tasks]
        except FileNotFoundError:
            pass


def main():
    task_manager = TaskManager()
    while True:
        print("\n1. Add Task")
        print("2. List Tasks")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline: ")
            category = input("Enter task category: ")
            task_manager.add_task(title, description, deadline, category)
        elif choice == '2':
            task_manager.list_tasks()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
