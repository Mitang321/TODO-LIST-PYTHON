import json


class Task:
    def __init__(self, title, description="", deadline="", category="", completed=False):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.category = category
        self.completed = completed

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'category': self.category,
            'completed': self.completed
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
            status = "Completed" if task.completed else "Pending"
            print(f"{idx + 1}. {task.title} - {task.description} (Deadline: {task.deadline}, Category: {task.category}, Status: {status})")

    def edit_task(self, index, title=None, description=None, deadline=None, category=None):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.title = title or task.title
            task.description = description or task.description
            task.deadline = deadline or task.deadline
            task.category = category or task.category
            self.save_tasks()

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()

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
        print("3. Edit Task")
        print("4. Mark Task as Completed")
        print("5. Exit")
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
            index = int(input("Enter task number to edit: ")) - 1
            title = input(
                "Enter new task title (leave blank to keep current): ")
            description = input(
                "Enter new task description (leave blank to keep current): ")
            deadline = input(
                "Enter new task deadline (leave blank to keep current): ")
            category = input(
                "Enter new task category (leave blank to keep current): ")
            task_manager.edit_task(
                index, title, description, deadline, category)
        elif choice == '4':
            index = int(input("Enter task number to mark as completed: ")) - 1
            task_manager.mark_task_completed(index)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
