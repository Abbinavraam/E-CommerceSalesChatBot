# Frontend Styling System

This document outlines the comprehensive styling system for the E-commerce Sales ChatBot frontend application.

## Architecture Overview

The styling system is organized into several layers:

1. **Theme Configuration** (`theme.css`) - CSS custom properties and design tokens
2. **Base Styles** (`index.css`) - Reset, typography, and global styles
3. **Utility Classes** (`utilities.css`) - Atomic utility classes
4. **Animation Library** (`animations.css`) - Reusable animations and transitions
5. **Component Styles** - Page and component-specific styles
6. **Layout Components** - Navbar, Footer, and layout-specific styles

## File Structure

```
src/
├── styles/
│   ├── theme.css          # Design tokens and CSS custom properties
│   ├── utilities.css      # Utility classes
│   ├── animations.css     # Animation library
│   └── README.md         # This documentation
├── pages/
│   ├── Home.css          # Home page styles
│   ├── Chat.css          # Chat page styles
│   ├── Auth.css          # Login/Register pages
│   ├── Products.css      # Products page styles
│   └── Profile.css       # Profile page styles
├── components/
│   ├── Layout/
│   │   ├── Navbar.css    # Navigation bar styles
│   │   └── Footer.css    # Footer styles
│   └── UI/
│       └── LoadingSpinner.css  # Loading spinner styles
├── index.css             # Global styles and imports
└── App.css              # App-level styles
```

## Design System

### Color Palette

The application uses a comprehensive color system with semantic naming:

- **Primary**: Blue tones for main actions and branding
- **Secondary**: Gray tones for secondary elements
- **Success**: Green tones for positive actions
- **Warning**: Yellow/Orange tones for warnings
- **Error**: Red tones for errors and destructive actions
- **Info**: Blue tones for informational content

### Typography

- **Font Family**: System font stack for optimal performance
- **Font Sizes**: 10 predefined sizes from xs (0.75rem) to 6xl (3.75rem)
- **Font Weights**: 8 weights from thin (100) to black (900)
- **Line Heights**: 6 options from none (1) to loose (2)

### Spacing System

Consistent spacing using a 0.25rem (4px) base unit:
- 0, 1 (0.25rem), 2 (0.5rem), 3 (0.75rem), 4 (1rem), etc.

### Border Radius

- **none**: 0
- **sm**: 0.125rem
- **base**: 0.25rem
- **md**: 0.375rem
- **lg**: 0.5rem
- **xl**: 0.75rem
- **2xl**: 1rem
- **3xl**: 1.5rem
- **full**: 9999px (circular)

## Component Styling Guidelines

### Button Components

```css
.btn {
  /* Base button styles */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--btn-padding-y) var(--btn-padding-x);
  border-radius: var(--btn-border-radius);
  transition: var(--btn-transition);
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
}
```

### Card Components

```css
.card {
  background: var(--card-bg);
  border: var(--card-border);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  padding: var(--card-padding);
}
```

### Form Components

```css
.form-input {
  padding: var(--input-padding-y) var(--input-padding-x);
  border: var(--input-border);
  border-radius: var(--input-border-radius);
  background: var(--input-bg);
  transition: var(--input-transition);
}

.form-input:focus {
  border: var(--input-focus-border);
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

## Responsive Design

The system uses a mobile-first approach with the following breakpoints:

- **sm**: 640px and up
- **md**: 768px and up
- **lg**: 1024px and up
- **xl**: 1280px and up
- **2xl**: 1536px and up

### Media Query Usage

```css
/* Mobile first */
.component {
  /* Mobile styles */
}

@media (min-width: 768px) {
  .component {
    /* Tablet styles */
  }
}

@media (min-width: 1024px) {
  .component {
    /* Desktop styles */
  }
}
```

## Dark Mode Support

The system includes comprehensive dark mode support using CSS custom properties and media queries:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: var(--color-gray-900);
    --text-primary: var(--color-gray-50);
    /* ... other dark mode variables */
  }
}
```

## Accessibility Features

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  .component {
    border-width: 2px;
    /* Enhanced contrast styles */
  }
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .component {
    animation: none !important;
    transition: none !important;
  }
}
```

### Focus Management

All interactive elements include proper focus styles:

```css
.interactive-element:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}
```

### Screen Reader Support

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Animation System

### Available Animations

- **Fade**: fadeIn, fadeOut, fadeInUp, fadeInDown, fadeInLeft, fadeInRight
- **Scale**: scaleIn, scaleOut
- **Slide**: slideInUp, slideInDown, slideInLeft, slideInRight
- **Special**: bounce, pulse, shake, rotate, heartbeat, wobble, flash

### Usage

```css
.element {
  animation: fadeInUp 0.6s ease-out;
}

/* Or using utility classes */
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}
```

### Animation Modifiers

- **Delays**: animate-delay-100, animate-delay-200, etc.
- **Durations**: animate-duration-150, animate-duration-300, etc.
- **Fill Modes**: animate-fill-forwards, animate-fill-both
- **Iterations**: animate-infinite, animate-once, animate-twice

## Utility Classes

The system includes comprehensive utility classes for:

- **Layout**: flex, grid, block, inline, hidden
- **Positioning**: relative, absolute, fixed, sticky
- **Spacing**: margin and padding utilities
- **Typography**: text alignment, size, weight, color
- **Colors**: background and text colors
- **Borders**: width, color, radius
- **Shadows**: various shadow levels
- **Transitions**: duration, timing functions

### Example Usage

```html
<div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
  <h2 class="text-xl font-semibold text-gray-900">Title</h2>
  <button class="btn btn-primary">Action</button>
</div>
```

## Best Practices

### 1. Use CSS Custom Properties

Prefer CSS custom properties for consistent theming:

```css
.component {
  color: var(--text-primary);
  background: var(--surface-primary);
}
```

### 2. Mobile-First Responsive Design

Always start with mobile styles and enhance for larger screens:

```css
.component {
  /* Mobile styles */
  padding: 1rem;
}

@media (min-width: 768px) {
  .component {
    /* Tablet and up */
    padding: 2rem;
  }
}
```

### 3. Semantic Class Names

Use descriptive, semantic class names:

```css
/* Good */
.product-card { }
.user-avatar { }
.chat-message { }

/* Avoid */
.blue-box { }
.big-text { }
.left-thing { }
```

### 4. Component Isolation

Keep component styles scoped and avoid global modifications:

```css
/* Component-specific styles */
.chat-page .message {
  /* Styles specific to chat messages */
}
```

### 5. Performance Considerations

- Use `transform` and `opacity` for animations
- Prefer CSS over JavaScript for simple animations
- Use `will-change` sparingly and remove after animations
- Optimize for 60fps animations

## Browser Support

The styling system supports:

- **Modern Browsers**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **CSS Features**: CSS Grid, Flexbox, Custom Properties, CSS Animations
- **Fallbacks**: Graceful degradation for older browsers

## Maintenance

### Adding New Components

1. Create component-specific CSS file
2. Import in the component file
3. Follow naming conventions
4. Include responsive styles
5. Add dark mode support
6. Include accessibility features

### Updating the Design System

1. Update theme.css for design tokens
2. Test across all components
3. Update documentation
4. Verify accessibility compliance
5. Test in different browsers and devices

## Performance Optimization

- CSS is organized for optimal loading
- Critical styles are inlined where necessary
- Non-critical styles are loaded asynchronously
- CSS is minified in production
- Unused styles are purged in build process
