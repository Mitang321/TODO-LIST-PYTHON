import json
from cmd import Cmd


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

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
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


class TaskManagerCLI(Cmd):
    intro = "Welcome to the Task Manager. Type help or ? to list commands.\n"
    prompt = "(task-manager) "

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()

    def do_add(self, arg):
        args = arg.split()
        if len(args) < 4:
            print("Usage: add title description deadline category")
            return
        title, description, deadline, category = args[0], args[1], args[2], args[3]
        self.task_manager.add_task(title, description, deadline, category)

    def do_list(self, arg):
        self.task_manager.list_tasks()

    def do_edit(self, arg):
        args = arg.split()
        if len(args) < 5:
            print("Usage: edit task_number title description deadline category")
            return
        index = int(args[0]) - 1
        title, description, deadline, category = args[1], args[2], args[3], args[4]
        self.task_manager.edit_task(
            index, title, description, deadline, category)

    def do_complete(self, arg):
        index = int(arg) - 1
        self.task_manager.mark_task_completed(index)

    def do_delete(self, arg):
        index = int(arg) - 1
        self.task_manager.delete_task(index)

    def do_exit(self, arg):
        print("Goodbye!")
        return True


if __name__ == "__main__":
    TaskManagerCLI().cmdloop()
