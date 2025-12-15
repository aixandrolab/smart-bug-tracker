# 🐛 Smart Bug Tracker

**Version 1.1.2**  
*Professional task management and bug tracking system*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey)

---

## 🎯 What's New in Version 1.1.2

### ✨ **New Features**

#### **Project Editing**
- **Edit Project Information**: New "Edit Project" menu option in Project menu
- **Comprehensive Editing**: Modify project name, description, author, GitHub URL
- **Team Management**: Add/remove developers and testers
- **Version Management**: Edit version lists directly

#### **Smart Version Selection**
- **Automatic Version Detection**: Automatically selects latest version on startup
- **Developer-Friendly**: Developers can create first version immediately
- **Tester-Optimized**: Testers get informative message when no versions exist
- **Intuitive Workflow**: Reduced clicks to start working

### 🛠️ **Developer Experience Improvements**
- **Enhanced Version Creation**: Smart version name suggestions (v1.0.0 → v1.0.1)
- **Natural Version Sorting**: Versions sorted intelligently (v1.0.0, v1.0.1, v1.1.0)
- **Auto-Refresh**: UI updates automatically after project edits
- **Better Error Handling**: Clear messages for missing versions

### 🧪 **Tester Experience Improvements**
- **Clear Guidance**: Informative messages when actions require developer intervention
- **Streamlined Workflow**: No confusing prompts for version creation
- **Role-Appropriate UI**: Interface adapts to tester capabilities

### 🔧 **Technical Improvements**
- **Code Refactoring**: Improved project model with version sorting
- **Enhanced Data Persistence**: Better handling of project metadata
- **UI Consistency**: Unified editing experience across both modes
- **Bug Fixes**: Various stability improvements

---

## 🎯 What is This?

**Smart Bug Tracker** is a professional desktop application for developers and testers that helps teams efficiently manage software development projects. It combines task management, bug tracking, and project organization in one intuitive tool.

### Perfect For:
- **Development Teams** managing multiple projects
- **QA Engineers** tracking and reporting bugs
- **Project Managers** monitoring progress
- **Individual Developers** organizing their work
- **Open Source Projects** needing structured bug tracking

---

## ✨ Key Features

### 🛠️ **Developer Mode**
- **Create and manage test tasks** with detailed descriptions
- **Track task progress** through customizable statuses
- **Organize by priority** (Critical, High, Medium, Low)
- **Multi-version support** for different project releases
- **Detailed statistics** and progress analytics
- **GitHub integration** for repository linking
- **Export capabilities** for data backup and sharing
- **Project editing** for managing all project details

### 🧪 **Tester Mode**
- **Report bugs** with comprehensive details
- **Attach screenshots** and reproduction steps
- **Link bugs to specific tasks**
- **Add comments** for team collaboration
- **Track bug resolution** through different statuses
- **Filter and search** through reported issues
- **Project viewing** to see team information

### 📊 **For Everyone**
- **Modern dark theme** with comfortable viewing
- **Keyboard shortcuts** for all common actions
- **Real-time statistics** dashboard
- **Data persistence** with automatic saving
- **Context menus** for quick actions
- **Comprehensive search** across all data
- **Role-based interface** tailored to your needs
- **Automatic version selection** on startup

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/aixandrolab/smart-bug-tracker.git
cd smart-bug-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Your First 5 Minutes

1. **Create a new project** - Click "+ New Project" and fill in your project details
2. **Select your role** - Choose between Developer or Tester mode
3. **Create a version** (Developer) - Automatically prompted to create first version
4. **Start working** - Tasks/bugs automatically load for latest version
5. **Explore the interface** - Try out filters, search, and keyboard shortcuts

---

## 📖 Complete Guide

### 🏗️ Project Management

#### Creating Projects
1. Click **"+ New Project"** from the main screen
2. Enter:
   - **Project Name** (required)
   - **Description** (optional)
   - **Author** (your name)
   - **GitHub URL** (optional - for repository linking)
   - **Save Location** (where to store the project file)

#### Editing Projects (Developer Mode)
1. Go to **Project → Edit Project**
2. Modify any project details:
   - Change project name, description, author
   - Update GitHub URL
   - Add/remove versions (comma-separated)
   - Manage developer and tester lists
3. Click **Save Changes** - UI updates automatically

#### Version Management
Each project can have multiple versions (e.g., v1.0.0, v1.1.0, v2.0.0):
- **Automatic selection**: Latest version selected on startup
- **Create new version**: From version dropdown, click "➕ New Version"
- **Smart suggestions**: System suggests next version (v1.0.0 → v1.0.1)
- **Switch versions**: Use dropdown to change between versions
- **Version isolation**: Each version has separate tasks and bugs

### 📋 Task Management (Developer Mode)

#### Adding Tasks
1. Navigate to the **Tasks tab**
2. Click **"📝 Add Test Task"** or press `Ctrl+T`
3. Fill in task details:
   - **Title** (required): Brief description of the task
   - **Description**: Detailed explanation
   - **Priority**: Critical/High/Medium/Low
   - **Test Instructions**: Steps for testers
   - **Assigned To**: Developer responsible

#### Task Statuses
- **Todo**: Task created but not started
- **In Progress**: Currently being worked on
- **Ready for Test**: Completed and ready for testing
- **Testing**: Under testing by QA
- **Done**: Fully completed and tested
- **Blocked**: Cannot proceed due to dependencies

#### Managing Tasks
- **Edit**: Double-click or right-click → "Edit Task"
- **Change Status**: Right-click → select new status
- **Delete**: Right-click → "Delete Task" or press `Delete`
- **Filter**: Use dropdowns to filter by priority/status
- **Search**: Type in the search box to find specific tasks

### 🐛 Bug Tracking (Tester Mode)

#### Reporting Bugs
1. Navigate to the **Bugs tab**
2. Click **"➕ Add Bug"** or press `Ctrl+B`
3. Complete the bug report form:
   - **Title** (required): Short, descriptive bug title
   - **Description** (required): Detailed explanation
   - **Associated Task** (optional): Link to related development task
   - **Priority**: Critical/High/Medium/Low based on impact
   - **Steps to Reproduce**: Clear, numbered steps
   - **Expected vs Actual Results**: What should happen vs what does happen
   - **Screenshot**: Optional image attachment
   - **Author**: Your name

#### Bug Statuses
- **Open**: New bug reported, not yet addressed
- **In Progress**: Developer is working on a fix
- **Fixed**: Bug has been resolved
- **Won't Fix**: Decision made not to fix the issue
- **Duplicate**: Already reported elsewhere
- **Invalid**: Not actually a bug

#### Managing Bugs
- **View Details**: Double-click any bug for full information
- **Add Comments**: Right-click → "Add Comment" for team discussion
- **Change Status**: Update as bugs progress through workflow
- **Filter**: Narrow down bugs by status, priority, or search terms
- **Export**: Save bug reports for sharing or documentation

### 📊 Statistics Dashboard

The Statistics tab provides comprehensive insights into your project:

#### Progress Metrics
- **Task Completion Rate**: Percentage of completed tasks
- **Bug Resolution Rate**: Percentage of fixed bugs
- **Priority Distribution**: Breakdown of task/bug priorities
- **Status Overview**: Current state of all items
- **Project Health**: Overall metrics and ratios

#### Export Options
1. **Statistics Only**: Export just the metrics as JSON
2. **Full Report**: Complete project data with all details
3. **Project Backup**: Entire project file for safekeeping

### ⌨️ Essential Keyboard Shortcuts

#### Developer Mode
| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to Tasks tab |
| `Ctrl+2` | Switch to Bugs tab |
| `Ctrl+3` | Switch to Statistics tab |
| `Ctrl+T` | Add new task |
| `Ctrl+R` | Edit selected item |
| `Delete` | Delete selected item |
| `Ctrl+D` | Mark as Done |
| `Ctrl+P` | Mark as In Progress |
| `Ctrl+S` | Save project |
| `Ctrl+E` | Export data |
| `Ctrl+G` | Open GitHub repository |
| `F5` | Refresh data |

#### Tester Mode
| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to Tasks tab |
| `Ctrl+2` | Switch to Bugs tab |
| `Ctrl+3` | Switch to Statistics tab |
| `Ctrl+B` | Add new bug |
| `Ctrl+R` | Edit selected bug |
| `Delete` | Delete selected bug |
| `Ctrl+D` | Mark bug as Fixed |
| `Ctrl+P` | Mark bug as In Progress |
| `Ctrl+F` | Focus search box |
| `Ctrl+S` | Save project |
| `Ctrl+E` | Export data |
| `F1` | Show help |

### 🔄 Switching Between Modes

You can switch between Developer and Tester modes at any time:
1. Go to **Project → Switch to [Other] Mode**
2. All changes are automatically saved
3. The interface adapts to show role-appropriate features

---

## ❓ Frequently Asked Questions

### General Questions

**Q: Is my data safe?**  
A: Yes! All data is saved locally in JSON format. You control where it's stored and can create backups anytime.

**Q: Can I use this for multiple projects?**  
A: Absolutely! Create separate project files for each of your projects.

**Q: Is there a limit to tasks or bugs I can add?**  
A: No technical limit - add as many as you need.

**Q: Can I import data from other bug trackers?**  
A: Currently, direct import isn't supported, but you can manually create tasks/bugs or modify exported JSON files.

### Version 1.1.2 Questions

**Q: How do I edit project details?**  
A: In Developer mode, go to Project → Edit Project.

**Q: Can testers edit projects?**  
A: No, project editing is a developer-only feature to maintain data integrity.

**Q: What happens if there are no versions?**  
A: Developers are prompted to create one. Testers see an informative message.

**Q: How are versions sorted?**  
A: Versions use natural sorting (v1.0.0, v1.0.1, v1.1.0, v2.0.0).

### Technical Questions

**Q: What Python version do I need?**  
A: Python 3.8 or higher is required.

**Q: Can I run this on my server?**  
A: This is a desktop application designed for local use. For team collaboration, you'll need to share the project file.

**Q: How do I update the application?**  
A: Pull the latest changes from GitHub and reinstall dependencies if needed.

**Q: Where are screenshots stored?**  
A: Screenshots are referenced by file path, not embedded. Keep the image files accessible.

### Usage Questions

**Q: How do I assign tasks to team members?**  
A: Use the "Assigned To" field when creating or editing tasks.

**Q: Can I change bug priorities after creation?**  
A: Yes! Edit any bug to change its priority.

**Q: What's the difference between "Won't Fix" and "Invalid"?**  
A: "Won't Fix" means it's a bug but won't be addressed. "Invalid" means it's not actually a bug.

**Q: How do I track which bugs belong to which tasks?**  
A: When reporting bugs, you can associate them with tasks. Use the task filter to see all related bugs.

---

## 🏗️ Technical Information

### Data Structure

Projects are saved as `.bugtracker.json` files with this structure:
```json
{
  "meta": {
    "name": "Project Name",
    "description": "Project description",
    "author": "Your Name",
    "github_url": "https://github.com/username/repo",
    "versions": ["v1.0.0", "v1.1.0"],
    "developers": ["dev1", "dev2"],
    "testers": ["tester1", "tester2"]
  },
  "versions": {
    "v1.0.0": {
      "tasks": {
        "TASK-ABC123": { ... }
      },
      "bugs": {
        "BUG-DEF456": { ... }
      }
    }
  }
}
```

### Version Sorting Algorithm
Versions are sorted using natural sorting:
- `v1.0.0` → `v1.0.1` → `v1.1.0` → `v2.0.0`
- `dev` → `test` → `v1.0.0` → `v1.1.0`

### File Locations
- **Project Files**: Saved wherever you choose during creation
- **Dependencies**: Installed in your Python environment
- **Temporary Data**: No temporary files created

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (2GB recommended)
- **Storage**: 50MB free space

---

## 🆘 Support

### Getting Help
- **Check this README** - Most questions are answered here
- **Keyboard shortcuts** - Most actions have shortcuts for efficiency
- **In-app help** - Press `F1` in any window for shortcuts reference

### Reporting Issues
Found a bug in the bug tracker? Report it:
1. Check if it's already known
2. Provide clear steps to reproduce
3. Include your OS and Python version
4. Create an issue on GitHub

### Feature Requests
Have an idea to improve Smart Bug Tracker?
1. Check if it's already planned
2. Explain the use case clearly
3. Suggest how it should work
4. Submit on GitHub Issues

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyQt5 Team** for the excellent GUI framework
- **All Contributors** who have submitted issues and suggestions
- **Open Source Community** for inspiration and best practices

---

## 🔄 Changelog

### Version 1.1.2 (Current)
- **Added**: Project editing capabilities for developers
- **Added**: Automatic version selection on startup
- **Added**: Smart version name suggestions
- **Added**: Natural version sorting
- **Added**: Role-specific version creation workflows
- **Improved**: UI consistency across modes
- **Improved**: Error messages and user guidance

---

⭐ **If you find this useful, please star the repository!**  
🐛 **Found a bug? Report it to help improve the tool.**  
🔄 **Have suggestions? We'd love to hear your feedback.**

---

**Happy Developing and Testing!** 🚀✨