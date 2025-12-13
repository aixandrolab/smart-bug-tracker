# 🐛 Smart Bug Tracker <sup>v1.1.0<sup>

A comprehensive desktop application for efficient bug tracking, test management, and project organization built with Python and PyQt5.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey)

## ✨ Features

### 🔧 **Developer Mode**
- **Test Task Management**: Create, edit, and track development tasks
- **Bug Tracking**: Comprehensive bug management with detailed reporting
- **Version Control**: Multi-version project support with data isolation
- **Statistics Dashboard**: Visual analytics and progress tracking
- **GitHub Integration**: Link projects to GitHub repositories
- **Export Capabilities**: Export projects, statistics, and full reports

### 🧪 **Tester Mode**
- **Bug Reporting**: Detailed bug submission with screenshots and reproduction steps
- **Test Execution**: Execute test cases and track results
- **Task Review**: View and interact with developer-created tasks
- **Collaborative Features**: Add comments and update bug statuses
- **Priority Management**: Critical/High/Medium/Low priority classification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PyQt5

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/aixandrolab/smart-bug-tracker.git
cd smart-bug-tracker
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

## 📖 User Guide

### Creating Your First Project

1. Launch the application
2. Click **"+ New Project"**
3. Fill in project details:
   - **Project Title**: Your project name
   - **Description**: Brief project description
   - **Author**: Your name
   - **GitHub URL** (optional): Link to repository
   - **Save Location**: Choose folder to save project file

4. **Select your role:**
   - **👨‍💻 Developer**: For managing tasks and overall project
   - **🧪 Tester**: For reporting bugs and testing

### Working with Versions

Projects support multiple versions (e.g., v1.0.0, v2.0.0). Each version maintains separate:
- Test tasks
- Bug reports
- Statistics

**To create a new version:**
1. Select "Select version..." from dropdown
2. Click **"➕ New Version"**
3. Enter version name (e.g., "v1.2.0")

### 📋 Managing Test Tasks (Developer Mode)

#### Adding a Task:
1. Navigate to Tasks tab
2. Click **"📝 Add Test Task"** or press `Ctrl+T`
3. Fill in task details:
   - Title (required)
   - Description
   - Priority (Critical/High/Medium/Low)
   - Test instructions
   - Assigned developer

#### Task Status Workflow:
```
Todo → In Progress → Ready for Test → Testing → Done
```

### 🐛 Reporting Bugs (Tester Mode)

#### Adding a Bug:
1. Navigate to Bugs tab
2. Click **"➕ Add Bug"** or press `Ctrl+B`
3. Complete bug report:
   - **Title**: Short descriptive title (required)
   - **Description**: Detailed explanation (required)
   - **Associated Task**: Link to existing task (optional)
   - **Priority**: Impact level
   - **Steps to Reproduce**: Clear reproduction steps
   - **Expected vs Actual Results**
   - **Screenshot**: Upload image evidence
   - **Author**: Your name

#### Bug Status Options:
- **Open**: Newly reported bug
- **In Progress**: Being worked on
- **Fixed**: Issue resolved
- **Won't Fix**: Intentional behavior
- **Duplicate**: Already reported
- **Invalid**: Not a bug

### 📊 Statistics Dashboard

Both modes provide comprehensive statistics:

#### Key Metrics:
- **Task Completion Rate**: Percentage of completed tasks
- **Bug Resolution Rate**: Percentage of fixed bugs
- **Priority Distribution**: Breakdown by priority level
- **Status Distribution**: Task/bug status overview
- **Task-to-Bug Ratio**: Overall project health metric

#### Export Options:
- **JSON Export**: Full project data
- **Statistics Export**: Metrics only
- **Full Report**: Comprehensive project report

## ⌨️ Keyboard Shortcuts

### Developer Mode
| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Tasks tab |
| `Ctrl+2` | Bugs tab |
| `Ctrl+3` | Statistics tab |
| `Ctrl+T` | Add new task |
| `Ctrl+R` | Edit selected task |
| `Delete` | Delete selected task |
| `Ctrl+D` | Mark task as Done |
| `Ctrl+P` | Mark task as In Progress |
| `Ctrl+S` | Save project |
| `Ctrl+E` | Export JSON |
| `Ctrl+G` | Open GitHub repository |

### Tester Mode
| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Tasks tab |
| `Ctrl+2` | Bugs tab |
| `Ctrl+3` | Statistics tab |
| `Ctrl+B` | Add new bug |
| `Ctrl+R` | Edit selected bug |
| `Delete` | Delete selected bug |
| `Ctrl+D` | Mark bug as Fixed |
| `Ctrl+P` | Mark bug as In Progress |
| `Ctrl+F` | Focus bug search |
| `Ctrl+Shift+F` | Focus task search |
| `Ctrl+Shift+A` | Show all bugs |
| `Ctrl+Shift+C` | Show critical bugs |

## 🏗️ Project Structure

```
smart-bug-tracker/
├── core/
│   ├── managers/
│   │   ├── bug_manager.py     # Bug management logic
│   │   └── task_manager.py    # Task management logic
│   ├── models/
│   │   ├── bug.py            # Bug data model
│   │   ├── task.py           # Task data model
│   │   └── project.py        # Project data model
│   ├── ui/
│   │   ├── windows/
│   │   │   ├── main_window.py
│   │   │   ├── developer_window.py
│   │   │   ├── tester_window.py
│   │   │   ├── bug_detailed_window.py
│   │   │   └── task_detail_window.py
│   │   └── dialogs/
│   │       ├── projects/
│   │       ├── bugs/
│   │       ├── tasks/
│   │       └── roles/
│   └── utils/
│       ├── project_file_handler.py
│       ├── statistics_generator.py
│       └── dark_theme.py
├── main.py                   # Application entry point
└── README.md                 # This file
```

## 🔧 Technical Architecture

### Data Models

#### **Bug Model** (`Bug` class):
- Unique identifier (BUG-UUID)
- Title and description
- Priority (Critical/High/Medium/Low)
- Status (Open/In Progress/Fixed/etc.)
- Task association
- Reproduction steps
- Expected/Actual results
- Screenshot path
- Comments with timestamps

#### **Task Model** (`Task` class):
- Unique identifier (TASK-UUID)
- Title and description
- Priority and status
- Version association
- Test instructions
- Assigned developer
- Linked bug IDs

#### **Project Model** (`Project` class):
- Name and description
- Author information
- GitHub URL
- Version list
- Developer/Tester lists

### File Format

Projects are saved as `.bugtracker.json` files with structure:
```json
{
  "project": { ... },
  "versions": {
    "v1.0.0": {
      "tasks": { ... },
      "bugs": { ... }
    }
  }
}
```

## 🎨 UI/UX Design

### Modern Dark Theme
- **Primary Color**: `#0e65e5` (Blue accent)
- **Background**: `#121212` (Dark base)
- **Card Background**: `#1e1e1e`
- **Text**: High contrast white/gray
- **Visual Feedback**: Color-coded status indicators

### Responsive Layout
- Tab-based navigation
- Scrollable content areas
- Context menus for quick actions
- Keyboard shortcut support
- Tooltips for all interactive elements

## 🔄 Workflow Examples

### Scenario 1: New Feature Development
1. **Developer** creates task "Implement user authentication"
2. **Developer** adds test instructions
3. **Tester** executes tests based on instructions
4. **Tester** reports bugs if found
5. **Developer** fixes bugs
6. **Tester** verifies fixes
7. Task marked as **Done**

### Scenario 2: Bug Triage Process
1. **Tester** reports bug with reproduction steps
2. Bug assigned **Critical** priority
3. **Developer** investigates and fixes
4. Bug status updated to **In Progress**
5. Fix verified by **Tester**
6. Bug status updated to **Fixed**
7. Statistics updated automatically

## 📈 Advanced Features

### 1. **Priority-Based Filtering**
Filter tasks/bugs by priority to focus on critical issues first.

### 2. **Search Functionality**
Full-text search across:
- Task titles/descriptions
- Bug titles/descriptions
- Task IDs
- Bug IDs

### 3. **Context Menus**
Right-click on any task/bug for:
- Quick status changes
- View details
- Edit/Delete options
- Add comments

### 4. **Real-time Statistics**
Live updates of:
- Completion percentages
- Priority distributions
- Status breakdowns
- Ratios and metrics

### 5. **Import/Export**
- Export full projects
- Export statistics only
- Import existing projects
- Cross-version data management

## 🛠️ Troubleshooting

### Common Issues:

1. **"Select version first!" error**
   - Solution: Choose a version from dropdown before adding tasks/bugs

2. **Screenshot not loading**
   - Solution: Ensure image path is accessible and file exists

3. **Project save failed**
   - Solution: Check file permissions and disk space

4. **Statistics not updating**
   - Solution: Click **Refresh** (`F5`) or reselect version

### Performance Tips:
- Use keyboard shortcuts for common actions
- Filter lists before working with large datasets
- Export data periodically for backup
- Keep screenshot images optimized for size

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup:
```bash
# Clone with submodules (if any)
git clone --recursive https://github.com/aixandrolab/smart-bug-tracker.git

# Set up development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyQt5 Community** - For the excellent GUI framework
- **All Contributors** - For bug reports and feature suggestions

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/aixandrolab/smart-bug-tracker/issues)
- **Documentation**: This README and code comments
- **Email**: Contact through GitHub profile

---

⭐ **Star this repository** if you find it useful!  
🐛 **Report issues** to help improve the application.  
🔄 **Share feedback** to shape future features.

---

**Happy Bug Tracking!** 🐞✨