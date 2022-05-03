// tailwind.config.js
module.exports = {
  mode: 'jit',
  content: [
      './apps/**/*.html',
      './apps/**/*.js',
      '{{cookiecutter.project_app}}/templates/*.html'
    ],
  plugins: [
    require('@tailwindcss/typography'),
  ],
  theme: {
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
      '3xl': '1792px',
      '4xl': '2048px',
    },
    extend: {
      maxWidth: {
        "site-width": "71.75rem",
      },
      height: {
        "footer": "240px",
        "responsive-aspect": "calc(100vw * (9/16))",
      },
      spacing: {
        "caret-sm": "14px",
        "icon-sm": "24px",
        "nav-desktop-min": "320px",
        "nav-mobile-min": "350px",
        "gutter-left": "calc(50vw - 60rem)",
      }
    },
  },
}
