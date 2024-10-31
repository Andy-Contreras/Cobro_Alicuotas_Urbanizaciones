const colors = require('tailwindcss/colors');

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',

        // Descomentar si usas clases de Tailwind en archivos JS y Python
        '../../**/*.js',
        '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                yellow: colors.amber,
                'custom-gray': '#343c44',
                'custom-boton': '#14a4bc',
                'custom-green': '#2ca444',
                'custom-red': '#dc3444',
                'custom-blue': '#087cfc',
            },
            // Opcional: añade pantallas personalizadas
            screens: {
                'xs': '480px',
                '3xl': '1600px',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
};
