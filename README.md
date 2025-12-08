# Smart Bug Tracker 🐛

**Professional bug tracking and test management system for development teams**

Smart Bug Tracker is a comprehensive desktop application built with Python and PyQt5 that enables efficient bug tracking, test management, and project organization. It supports role-based workflows for both developers and testers within a version-controlled environment.

---

## ✨ Features

### 🎯 Core Functionality
- **Role-based access**: Developer and Tester modes with tailored interfaces
- **Version management**: Organize work by project versions
- **Test task management**: Create, assign, and track test tasks
- **Bug tracking**: Comprehensive bug reporting with detailed fields
- **Comments system**: Collaborative discussion on bugs and tasks
- **Statistics & reporting**: Real-time project analytics and exports

### 🧑‍💻 Developer Mode
- Create and manage test tasks with priorities (Critical/High/Medium/Low)
- Set task statuses (Todo/In Progress/Ready for Test/Testing/Done/Blocked)
- View all bugs and mark them as Fixed/In Progress
- Add developer comments to bug reports
- Manage project versions
- Export JSON reports and statistics

### 🧪 Tester Mode
- View assigned test tasks with instructions
- Execute test cases and mark tasks as In Progress/Done
- Report bugs with detailed reproduction steps
- Capture expected vs. actual results
- Attach screenshots to bug reports
- Add tester comments and update bug status

### 🎨 User Experience
- Dark theme interface with intuitive navigation
- Tabbed interface (Tasks, Bugs, Statistics)
- Expandable/collapsible detail panels
- Context menus for quick actions
- Filtering and search across all data
- Keyboard shortcuts for common operations

---

## 📥 Installation

### Prerequisites
- Python 3.7+
- PyQt5
- No external database required (uses JSON files)

### Step-by-Step Setup

1. **Clone or download the project**
   ```bash
   git clone https://github.com/aixandrolab/smart-bug-tracker
   cd smart-bug-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

### Alternative: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## 🚀 Usage

### First Launch
1. **Start the application**: Run `python app.py`
2. **Create a new project** or **Open existing project**
3. **Select your role**: Developer or Tester
4. **Choose a version**: Select or create a project version

### Creating a New Project
1. Click "New Project" from the main window
2. Enter project details:
   - Project Name (required)
   - Description (optional)
   - Author (optional)
   - Save location
3. The system creates a `.bugtracker.json` file with your project data

### Working with Tasks (Developer)
1. Select a version from the dropdown
2. Click "Add Test Task" or use Ctrl+Shift+T
3. Fill in task details:
   - Title and description
   - Priority level
   - Test instructions
   - Assignee (optional)
4. Use filters to view tasks by priority/status
5. Update task status as work progresses

### Reporting Bugs (Tester)
1. Select a task from the task list
2. Click "Add Bug for this Task"
3. Provide detailed bug information:
   - Title and description
   - Steps to reproduce
   - Expected vs. Actual results
   - Screenshot (optional)
   - Priority assessment
4. Submit the bug for developer review

---

## 📊 Project Structure

### File Format
Projects are saved as `.bugtracker.json` files with this structure:
```json
{
  "meta": {
    "name": "Project Name",
    "description": "Project description",
    "author": "Author Name",
    "created_at": "2024-01-15T10:30:00",
    "versions": ["v1.0.0", "v1.1.0"],
    "developers": ["Dev1", "Dev2"],
    "testers": ["Tester1", "Tester2"]
  },
  "versions": {
    "v1.0.0": {
      "tasks": {
        "TASK-ABC123": { /* Task data */ }
      },
      "bugs": {
        "BUG-DEF456": { /* Bug data */ }
      }
    }
  }
}
```

### ID Generation
- **Tasks**: `TASK-{8-char-uuid}` (e.g., `TASK-A1B2C3D4`)
- **Bugs**: `BUG-{8-char-uuid}` (e.g., `BUG-X9Y8Z7W6`)

---

## 🧩 Core Modules

### Bug Module (`core/bug.py`)
- **BugStatus**: OPEN, IN_PROGRESS, FIXED, WONT_FIX, DUPLICATE, INVALID
- **BugPriority**: CRITICAL, HIGH, MEDIUM, LOW
- **Features**: Comments system, assignment tracking, screenshot support

### Task Module (`core/task.py`)
- **TaskStatus**: TODO, IN_PROGRESS, READY_FOR_TEST, TESTING, DONE, BLOCKED
- **TaskPriority**: CRITICAL, HIGH, MEDIUM, LOW
- **Features**: Test instructions, bug associations, assignment

### Managers (`core/*_manager.py`)
- **TaskManager**: CRUD operations for tasks, filtering, statistics
- **BugManager**: CRUD operations for bugs, filtering, advanced search

### File Handler (`core/project_file_handler.py`)
- JSON-based persistence
- Version-aware data storage
- Export/import functionality

---

## 👥 Role-Based Workflows

### Developer Workflow
```
Create Project → Select Version → Add Tasks → 
Monitor Bugs → Fix Bugs → Update Status → Export Reports
```

**Developer Permissions:**
- ✅ Create/edit/delete test tasks
- ✅ View all bugs
- ✅ Mark bugs as fixed/in progress
- ✅ Add developer comments
- ✅ Manage project versions
- ✅ Export full project data
- ❌ Cannot edit tester-reported bug details

### Tester Workflow
```
Select Project → Choose Version → View Tasks → 
Execute Tests → Report Bugs → Add Comments → Track Fixes
```

**Tester Permissions:**
- ✅ View assigned test tasks
- ✅ Mark tasks as in progress/done
- ✅ Report new bugs
- ✅ Edit own bug reports
- ✅ Add tester comments
- ✅ View bug statistics
- ❌ Cannot create or delete tasks

---

## 📈 Export & Reporting

### Available Exports
1. **Full Project Export**: Complete project data as JSON
2. **Statistics Export**: Task/bug counts and status breakdowns
3. **Custom Reports**: Filtered data exports

### Export Locations
- JSON files can be saved anywhere
- Recommended naming: `{project_name}_{type}_{date}.json`

### Statistics Include
- Task counts by status and priority
- Bug counts by status and priority
- Open vs. fixed bug ratios
- Version-specific metrics

---

## ⌨ Keyboard Shortcuts

### Global Shortcuts
- `Ctrl+S` - Save project
- `Ctrl+E` - Export JSON
- `Ctrl+F` - Focus search field
- `Ctrl+Shift+F` - Clear all filters

### Developer Mode
- `Ctrl+Shift+T` - Add new task
- `Ctrl+Shift+C` - Filter critical tasks
- `Ctrl+Shift+A` - Show all tasks
- `Enter` - Open selected item details

### Tester Mode
- `Ctrl+B` - Add new bug
- `Tab` - Navigate between tabs
- `Esc` - Close dialog/cancel action

---

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement
- Additional export formats (PDF, CSV)
- Enhanced search capabilities
- Integration with issue trackers (JIRA, GitHub)
- Automated test execution tracking
- Multi-language support

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

### Common Issues
- **"Module not found"**: Ensure PyQt5 is installed: `pip install PyQt5`
- **"File not found"**: Check file path permissions
- **"JSON decode error"**: Verify project file integrity
- **"UI not loading"**: Check Python and PyQt5 versions

### Getting Help
1. Check the in-app help sections
2. Review this README
3. Examine the JSON project structure
4. Contact the development team

---

## 🚀 Quick Start Commands

```bash
# Create a test project
1. Launch app
2. Click "New Project"
3. Name it "TestProject"
4. Select Developer role
5. Add a version "v1.0.0"
6. Create test tasks
7. Switch to Tester role
8. Report bugs
```

---

**Smart Bug Tracker** - Streamline your testing process, track issues efficiently, and improve team collaboration! 🎯
