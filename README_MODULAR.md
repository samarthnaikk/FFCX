# FFCX Timetable Application - Modular Architecture

## Overview

This document describes the modular architecture of the FFCX Timetable Application after refactoring from monolithic files to a organized, maintainable structure.

## Project Structure

```
FFCX/
├── api/                           # Vercel API endpoints
│   └── index.py
├── config/                        # Configuration modules
│   └── timetable_config.py       # Timetable templates and course info
├── features/                      # Feature modules
│   ├── optimization.py           # Timetable optimization logic
│   └── validation.py            # Priority validation functions
├── helpers/                       # Utility modules
│   ├── data_loader.py            # CSV and file loading utilities
│   └── time_utils.py             # Time parsing and conflict detection
├── models/                        # Data models (future expansion)
├── routes/                        # Flask route modules
│   ├── basic_routes.py           # Basic endpoints (home, timetable)
│   ├── course_management_routes.py # Course CRUD operations
│   ├── course_routes.py          # Course search and suggestions
│   ├── export_import_routes.py   # Export/import functionality
│   ├── optimization_routes.py    # Optimization endpoints
│   └── validation_routes.py      # Validation endpoints
├── static/                        # Frontend assets
│   ├── css/                      # Modular CSS
│   │   ├── dark-mode.css         # Dark mode styles
│   │   ├── interactive.css       # Interactive elements
│   │   ├── layout.css            # Layout and components
│   │   └── timetable.css         # Timetable-specific styles
│   └── js/                       # Modular JavaScript
│       ├── app.js                # Main Vue.js application
│       ├── dark-mode.js          # Dark mode functionality
│       ├── drag-drop.js          # Drag and drop features
│       ├── export-import.js      # Export/import methods
│       ├── vue-computed.js       # Vue computed properties
│       ├── vue-data.js           # Vue data properties
│       └── vue-methods.js        # Vue methods
├── templates/                     # HTML templates
│   ├── components/               # Template components
│   │   ├── course-search.html    # Course search interface
│   │   ├── header.html           # Navigation header
│   │   ├── modals.html           # All modal dialogs
│   │   ├── sidebar.html          # Sidebar navigation
│   │   ├── stats.html            # Statistics dashboard
│   │   └── timetable.html        # Timetable display
│   ├── index.html                # Original monolithic template
│   └── index_new.html            # New modular template
├── app.py                         # Original monolithic backend
├── app_new.py                     # New modular backend
└── README_MODULAR.md             # This documentation
```

## Backend Architecture

### Core Application (`app_new.py`)
- **Purpose**: Main application factory and configuration
- **Features**: Error handling, CORS, logging, CLI commands
- **Pattern**: Factory pattern with modular route registration

### Configuration (`config/`)
- **timetable_config.py**: Centralized configuration for timetable templates and course metadata

### Features (`features/`)
- **optimization.py**: Core timetable optimization algorithms
- **validation.py**: Priority conflict validation and prevention

### Helpers (`helpers/`)
- **data_loader.py**: CSV data loading and processing utilities
- **time_utils.py**: Time parsing, slot conflict detection, and scheduling utilities

### Routes (`routes/`)
Each route module handles a specific domain:
- **basic_routes.py**: Home page, timetable display
- **course_routes.py**: Course search, teacher suggestions
- **course_management_routes.py**: Add, remove, move courses
- **optimization_routes.py**: Timetable optimization endpoints
- **export_import_routes.py**: Export/import functionality
- **validation_routes.py**: Priority validation endpoints

## Frontend Architecture

### CSS Modules (`static/css/`)
- **layout.css**: Base layout, grid system, responsive design
- **timetable.css**: Timetable-specific styling, grid layout
- **interactive.css**: Drag-and-drop, hover effects, animations
- **dark-mode.css**: Dark mode color schemes and transitions

### JavaScript Modules (`static/js/`)
- **vue-data.js**: Vue.js reactive data properties
- **vue-computed.js**: Vue.js computed properties and getters
- **vue-methods.js**: Core Vue.js methods (CRUD operations, API calls)
- **drag-drop.js**: Drag and drop functionality
- **export-import.js**: Export/import features
- **dark-mode.js**: Dark mode toggle and preferences
- **app.js**: Main Vue.js application that combines all modules

### Template Components (`templates/components/`)
- **header.html**: Navigation bar with actions and stats
- **sidebar.html**: Course list, statistics, quick actions
- **timetable.html**: Interactive timetable grid
- **course-search.html**: Course search and add interface
- **stats.html**: Statistics dashboard
- **modals.html**: All modal dialogs (export, import, preferences)

## Key Features

### 1. Priority Validation System
- **Backend**: `features/validation.py` - `validate_priority_conflicts()`
- **Frontend**: `vue-methods.js` - Priority validation methods
- **Feature**: Prevents duplicate priority numbers for courses and teachers

### 2. Modular Route Registration
```python
def register_routes(app):
    """Register all route modules with the Flask app."""
    register_basic_routes(app)
    register_course_routes(app)
    register_validation_routes(app)
    # ... other modules
```

### 3. Vue.js Component System
```javascript
const VueApp = createApp({
    data() { return { ...vueData }; },
    computed: { ...vueComputed },
    methods: { 
        ...vueMethods,
        ...dragDropMethods,
        ...exportImportMethods,
        ...darkModeMethods 
    }
});
```

### 4. CSS Module System
Each CSS module focuses on a specific concern:
- Layout and structure
- Timetable-specific styling
- Interactive elements
- Dark mode theming

## Benefits of Modular Architecture

### 1. **Maintainability**
- Each module has a single responsibility
- Easy to locate and modify specific functionality
- Clear separation of concerns

### 2. **Scalability**
- Easy to add new features as separate modules
- Independent development of different components
- Modular testing and debugging

### 3. **Code Reusability**
- Helper functions can be shared across modules
- Template components can be reused
- CSS modules can be mixed and matched

### 4. **Development Workflow**
- Multiple developers can work on different modules
- Feature development is isolated
- Easier code reviews and testing

## Migration Guide

### From Monolithic to Modular

1. **Backend Migration**:
   ```bash
   # Use the new modular backend
   python app_new.py
   ```

2. **Frontend Migration**:
   ```html
   <!-- Use the new modular template -->
   <!-- All CSS and JS is now externalized -->
   <link rel="stylesheet" href="/static/css/layout.css">
   <script src="/static/js/app.js"></script>
   ```

3. **Feature Addition**:
   - Backend: Add new route module in `routes/`
   - Frontend: Add new method module in `static/js/`
   - Styling: Add new CSS module in `static/css/`
   - Templates: Add new component in `templates/components/`

## Development Guidelines

### 1. **Adding New Features**
```python
# 1. Create feature module
# features/new_feature.py
def new_feature_logic():
    pass

# 2. Create route module  
# routes/new_feature_routes.py
def register_new_feature_routes(app):
    @app.route('/api/new-feature')
    def new_feature_endpoint():
        return new_feature_logic()

# 3. Register in main app
# app_new.py
from routes.new_feature_routes import register_new_feature_routes
register_new_feature_routes(app)
```

### 2. **Adding Frontend Components**
```javascript
// 1. Create method module
// static/js/new-feature.js
const newFeatureMethods = {
    newMethod() { /* implementation */ }
};

// 2. Include in main app
// static/js/app.js
methods: {
    ...vueMethods,
    ...newFeatureMethods
}
```

### 3. **Styling Guidelines**
- Use existing CSS modules where possible
- Create new modules for distinct features
- Follow BEM naming convention
- Support dark mode in all new styles

## Testing Strategy

### 1. **Backend Testing**
- Unit tests for each feature module
- Integration tests for route modules
- End-to-end API testing

### 2. **Frontend Testing**
- Component testing for Vue.js methods
- UI testing for interactive elements
- Cross-browser testing for compatibility

### 3. **Performance Testing**
- Module loading performance
- JavaScript bundle size optimization
- CSS file size and load times

## Future Enhancements

### 1. **Planned Modules**
- **Database Integration**: Move from CSV to database
- **User Authentication**: User accounts and saved timetables
- **Real-time Collaboration**: Multiple users editing same timetable
- **Mobile App**: React Native or Progressive Web App

### 2. **Architecture Improvements**
- **State Management**: Vuex/Pinia for complex state
- **Build Process**: Webpack/Vite for asset optimization
- **API Versioning**: Structured API versioning system
- **Microservices**: Split into smaller services

## Conclusion

The modular architecture provides a solid foundation for the FFCX Timetable Application, making it easier to maintain, extend, and scale. The clear separation of concerns and organized structure will facilitate future development and team collaboration.

For questions or contributions, please refer to the main README.md file or contact the development team.