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

    def list_tasks(self, filter_by=None):
        for idx, task in enumerate(self.tasks):
            if filter_by:
                if filter_by == 'completed' and not task.completed:
                    continue
                elif filter_by == 'pending' and task.completed:
                    continue
                elif filter_by == task.category:
                    continue
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


class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def add_user(self, username, password):
        self.users[username] = password
        self.save_users()

    def authenticate_user(self, username, password):
        return self.users.get(username) == password

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            pass


class TaskManagerCLI(Cmd):
    intro = "Welcome to the Task Manager. Type help or ? to list commands.\n"
    prompt = "(task-manager) "

    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.task_manager = TaskManager()
        self.current_user = None

    def do_register(self, arg):
        args = arg.split()
        if len(args) != 2:
            print("Usage: register username password")
            return
        username, password = args
        self.user_manager.add_user(username, password)
        print("User registered successfully!")

    def do_login(self, arg):
        args = arg.split()
        if len(args) != 2:
            print("Usage: login username password")
            return
        username, password = args
        if self.user_manager.authenticate_user(username, password):
            self.current_user = username
            print(f"User {username} logged in successfully!")
        else:
            print("Invalid username or password.")

    def preloop(self):
        print("Please log in or register to continue.")

    def postcmd(self, stop, line):
        if not self.current_user:
            print("Please log in or register to continue.")
        return stop

    def do_add(self, arg):
        if not self.current_user:
            print("You must be logged in to add tasks.")
            return
        args = arg.split()
        if len(args) < 4:
            print("Usage: add title description deadline category")
            return
        title, description, deadline, category = args[0], args[1], args[2], args[3]
        self.task_manager.add_task(title, description, deadline, category)

    def do_list(self, arg):
        if not self.current_user:
            print("You must be logged in to list tasks.")
            return
        if arg in ['completed', 'pending'] or arg:
            self.task_manager.list_tasks(filter_by=arg)
        else:
            self.task_manager.list_tasks()

    def do_edit(self, arg):
        if not self.current_user:
            print("You must be logged in to edit tasks.")
            return
        args = arg.split()
        if len(args) < 5:
            print("Usage: edit task_number title description deadline category")
            return
        index = int(args[0]) - 1
        title, description, deadline, category = args[1], args[2], args[3], args[4]
        self.task_manager.edit_task(
            index, title, description, deadline, category)

    def do_complete(self, arg):
        if not self.current_user:
            print("You must be logged in to complete tasks.")
            return
        index = int(arg) - 1
        self.task_manager.mark_task_completed(index)

    def do_delete(self, arg):
        if not self.current_user:
            print("You must be logged in to delete tasks.")
            return
        index = int(arg) - 1
        self.task_manager.delete_task(index)

    def do_exit(self, arg):
        print("Goodbye!")
        return True


if __name__ == "__main__":
    TaskManagerCLI().cmdloop()
